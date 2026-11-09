"""Mechanical placement study from the Rev D footprint and pad geometry."""
from collections import Counter, defaultdict
from pathlib import Path
import math
import random
from shutil import copy2, copytree

import numpy as np
import pcbnew as pcb

from build import pt, shape, txt

NAME = 'Studium_RevE'
ROOT = Path('outputs')
BASE = ROOT / 'Zasilacz_RevD_JLCPCB' / 'Zasilacz_RevD_JLCPCB.kicad_pcb'
DEST = ROOT / NAME
GRID = .5
EDGE = .75
BARRIER = 8.2
CROSS = {'T1', 'U1', 'CY1'}
# Keep C6 and D7 together on the flyback board, along with the local sensing loop.
SECOND = {
    'U2','U3','U4','C11','C12','C13','C14','C15','J2','J3',
    'R14','R15','R16','R17','R18','R19','R20','R21',
}


def secondary(ref):
    return ref in SECOND or ref.startswith('TP') or (
        ref.startswith(('C','D','R','U')) and ref[1:].isdigit() and int(ref[1:]) >= 100
    )

def box_mm(box, pos):
    return tuple(pcb.ToMM(a-b) for a,b in zip(
        (box.GetLeft(), box.GetTop(), box.GetRight(), box.GetBottom()),
        (pos.x, pos.y, pos.x, pos.y)
    ))


def outline(fp):
    side = pcb.F_Cu if fp.GetLayer() == pcb.F_Cu else pcb.B_Cu
    pol = fp.GetCourtyard(side)
    if pol.OutlineCount():
        return pol.BBox()
    return fp.GetBoundingBox(False, False)


def options(fp):
    side = 0 if fp.GetLayer() == pcb.F_Cu else 1
    ref = fp.GetReference()
    pos = fp.GetPosition()
    start = fp.GetOrientationDegrees()
    result = []
    for delta in (0, 90, 180, 270):
        if ref in CROSS and delta:
            continue
        fp.SetOrientationDegrees(start+delta)
        body = box_mm(outline(fp), pos)
        pads = [(p, box_mm(p.GetBoundingBox(), pos)) for p in fp.Pads()]
        boxes = [(side, body)]
        for p, b in pads:
            if p.GetDrillSize().x:
                boxes.append((1-side, b))
        prim = [b[2] for p, b in pads if p.GetNetname().startswith('/P_')]
        sec = [b[0] for p, b in pads if p.GetNetname() and not p.GetNetname().startswith(('/P_', 'unconnected-'))]
        result.append((start+delta, boxes, max(prim, default=-math.inf), min(sec, default=math.inf)))
    fp.SetOrientationDegrees(start)
    return result


def place(parts, sizes, geometry, seed, fixed, rank_pins):
    w,h,iso = sizes
    grid_w,grid_h = round(w/GRID),round(h/GRID)
    board = np.zeros((2, grid_h, grid_w), dtype=np.uint8)
    yy,xx = np.mgrid[:grid_h+1,:grid_w+1]
    rng = random.Random(seed)
    loc = {}
    nets = defaultdict(list)

    def possible(option, integral):
        angle,boxes,p_right,s_left = option
        allow = np.ones(xx.shape, dtype=bool)
        if iso is not None:
            allow &= (GRID*xx + p_right <= iso-BARRIER/2) & (GRID*xx+s_left >= iso+BARRIER/2)
        contact = np.zeros(xx.shape, dtype=np.int32)
        bounds = []
        for side,(x1,y1,x2,y2) in boxes:
            l,t,r,b = [math.floor(x1/GRID),math.floor(y1/GRID),math.ceil(x2/GRID),math.ceil(y2/GRID)]
            xl,xr,yt,yb = [xx+l,xx+r,yy+t,yy+b]
            allow &= (xx*GRID+x1>=EDGE) & (yy*GRID+y1>=EDGE) & (xx*GRID+x2<=w-EDGE) & (yy*GRID+y2<=h-EDGE)
            xl,xr = xl.clip(0,grid_w),xr.clip(0,grid_w)
            yt,yb = yt.clip(0,grid_h),yb.clip(0,grid_h)
            s = integral[side]
            allow &= s[yb,xr]-s[yb,xl]-s[yt,xr]+s[yt,xl] == 0
            if not bounds:
                pl,pr = (xl-1).clip(0,grid_w),(xr+1).clip(0,grid_w)
                pt,pb = (yt-1).clip(0,grid_h),(yb+1).clip(0,grid_h)
                contact += (s[pb,pr]-s[pb,pl]-s[pt,pr]+s[pt,pl]).astype(np.int32)
                contact += (xl <= 2)*(yb-yt)+(xr >= grid_w-2)*(yb-yt)+(yt <= 2)*(xr-xl)+(yb >= grid_h-2)*(xr-xl)
            bounds.append((side,l,t,r,b))
        return allow,contact,bounds

    def insert(ref, option, point, bounds):
        x,y = point
        for s,l,t,r,b in bounds:
            board[s,y+t:y+b,x+l:x+r] = 1
        loc[ref] = (x*GRID,y*GRID,option[0])
        for net in rank_pins.get(ref, ()):
            nets[net].append((x,y))

    def integral():
        return np.pad(board.cumsum(1,dtype=np.int32).cumsum(2,dtype=np.int32),((0,0),(1,0),(1,0)))

    for ref,(x,y) in fixed.items():
        option = geometry[ref][0]
        allowed,_,bounds = possible(option,integral())
        p = round(x/GRID),round(y/GRID)
        if not allowed[p[1],p[0]]:
            return None
        insert(ref,option,p,bounds)

    def priority(ref):
        box = geometry[ref][0][1][0][1]
        span = max(box[2]-box[0],box[3]-box[1])
        return span * rng.uniform(.82,1.17)

    phase = {ref: rng.random() for ref in sorted(parts)}
    for ref in sorted(sorted(set(parts)-fixed.keys()),key=priority,reverse=True):
        best = None
        ii = integral()
        points = [p for net in rank_pins.get(ref, ()) for p in nets[net]]
        if points:
            tx,ty = [sum(v)/len(v) for v in zip(*points)]
            distance = abs(xx-tx)+abs(yy-ty)
        else:
            distance = (xx if phase[ref]<.55 else grid_w-xx) + (.6*yy if seed%2 else .6*(grid_h-yy))
        for option in geometry[ref]:
            allow,contact,bounds = possible(option,ii)
            if not allow.any():
                continue
            score = distance * (.08 if points else .025) - contact * .20 + (xx*.001 + yy*.0003)
            score = np.where(allow,score,np.inf)
            y,x = np.unravel_index(score.argmin(),score.shape)
            val = score[y,x]
            if best is None or val < best[0]:
                best = val,option,(x,y),bounds
        if best is None:
            return None
        _,option,point,bounds = best
        insert(ref,option,point,bounds)
    return loc


def get_nets(fp):
    return {p.GetNetname() for p in fp.Pads()
            if p.GetNetname() and not p.GetNetname().startswith('unconnected-')}


def make_wire_pair(template, name):
    fp = pcb.Cast_to_FOOTPRINT(template.Duplicate(False))
    fp.SetReference(name)
    fp.SetValue('26 V / RTN')
    fp.SetFPID(pcb.LIB_ID(pcb.UTF8('E27'),pcb.UTF8('Harness_26V_RTN')))
    fp.SetLibDescription('Isolated secondary DC link, pad 1 = S_RAW, pad 2 = S_RTN')
    fp.SetPath(pcb.KIID_PATH())
    for p,net in zip(sorted(fp.Pads(),key=lambda p:p.GetNumber()),('/S_RAW','/S_RTN')):
        bnet = template.GetBoard().FindNet(net)
        assert bnet is not None
        p.SetNet(bnet)
    return fp


def new_layout(all_parts, loc, name, dims):
    w,h,iso = dims
    board = pcb.NewBoard(str(DEST / f'{name}.kicad_pcb'))
    board.SetCopperLayerCount(2)
    board.GetDesignSettings().SetBoardThickness(pcb.FromMM(1.6))
    for ref, (x,y,angle) in loc.items():
        fp = pcb.Cast_to_FOOTPRINT(all_parts[ref].Duplicate(False))
        fp.SetParent(board)
        fp.SetReference(ref)
        fp.SetPosition(pt(75+x,70+y))
        fp.SetOrientationDegrees(angle)
        fp.Reference().SetVisible(False)
        for pad in fp.Pads():
            net = pad.GetNetname()
            if not net:
                continue
            target = board.FindNet(net)
            if target is None:
                target = pcb.NETINFO_ITEM(board,net)
                board.Add(target)
            pad.SetNet(target)
        board.Add(fp)
    corners = [(75,70),(75+w,70),(75+w,70+h),(75,70+h),(75,70)]
    for a,b in zip(corners,corners[1:]):
        shape(board,pcb.Edge_Cuts,a,b)
    if iso is not None:
        for x in (75+iso-BARRIER/2,75+iso+BARRIER/2):
            shape(board,pcb.Dwgs_User,(x,70),(x,70+h))
    if name == 'E_Sterowanie':
        txt(board,'REV E',84,70+h-1.0,1.0)
    else:
        txt(board,'E27 / REV E',75+w/2,70+h-1.0,1.0)
    assert pcb.SaveBoard(str(DEST / f'{name}.kicad_pcb'),board)
    for suffix in ('pro','dru'):
        copy2(BASE.with_suffix(f'.kicad_{suffix}'), DEST/f'{name}.kicad_{suffix}')


def main():
    src = pcb.LoadBoard(str(BASE))
    refs = {fp.GetReference(): fp for fp in src.GetFootprints()}
    groups = {
        'E_Jedna': set(refs),
        'E_Moc': {ref for ref in refs if not secondary(ref)},
        'E_Sterowanie': {ref for ref in refs if secondary(ref)},
    }
    assert groups['E_Moc'] | groups['E_Sterowanie'] == groups['E_Jedna']
    power_nets = set().union(*(get_nets(refs[ref]) for ref in groups['E_Moc']))
    control_nets = set().union(*(get_nets(refs[ref]) for ref in groups['E_Sterowanie']))
    assert power_nets & control_nets == {'/S_RAW', '/S_RTN'}, power_nets & control_nets
    for group,ref in [('E_Moc','J101'),('E_Sterowanie','J102')]:
        refs[ref] = make_wire_pair(refs['J1'],ref)
        groups[group].add(ref)
    geometry = {ref: options(fp) for ref,fp in refs.items()}
    all_nets = {ref:get_nets(fp) for ref,fp in refs.items()}
    counts = Counter(net for ns in all_nets.values() for net in ns)
    ranked = {ref:sorted(n for n in ns if 1 < counts[n] < 9) for ref,ns in all_nets.items()}
    possibilities = {
        'E_Jedna':[(68,31,31),(70,31,32),(72,31,32),(72,32,32),(74,32,32),(76,32,33),(80,32,34)],
        'E_Moc':[(54,31,29),(55,31,30),(56,31,31),(56,32,31),(57,32,32),(58,32,33),(60,32,34),(61,33,35)],
        'E_Sterowanie':[(30,24,None),(30,26,None),(32,26,None),(34,27,None)],
    }
    DEST.mkdir(exist_ok=True)
    copytree(BASE.parent/'E27.pretty', DEST/'E27.pretty', dirs_exist_ok=True)
    copy2(BASE.parent/'fp-lib-table',DEST/'fp-lib-table')
    text = (BASE.parent/'E27.pretty'/'Mains_L_N.kicad_mod').read_text(encoding='utf8')
    text = text.replace('Mains_L_N','Harness_26V_RTN').replace(
        'Insulated wire harness, pads 1=L 2=N, 7 mm spacing',
        'Isolated secondary DC link, pad 1 = S_RAW, pad 2 = S_RTN'
    )
    (DEST/'E27.pretty'/'Harness_26V_RTN.kicad_mod').write_text(text,encoding='utf8')
    for name,sizes in possibilities.items():
        for dims in sizes:
            w,h,iso = dims
            fixed = {'T1':(iso,9),'U1':(iso,20.5),'CY1':(iso,h-4.0)} if iso else {}
            for seed in range(55):
                loc = place(groups[name],dims,geometry,seed,fixed,ranked)
                if loc:
                    break
            if loc:
                print(f'{name}: {w}x{h}, iso axis {iso}, {len(loc)} footprints, seed {seed}',flush=True)
                new_layout(refs,loc,name,dims)
                break
            print(f'{name}: no packing at {w}x{h}',flush=True)
        else:
            raise SystemExit(f'No placement for {name}')


if __name__ == '__main__':
    main()

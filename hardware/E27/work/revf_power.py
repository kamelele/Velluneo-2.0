"""Derive the Rev F flyback board from the verified Rev D power routing."""
from dataclasses import replace
from math import ceil, dist
from pathlib import Path
from shutil import copy2
import re
import pcbnew as p

import build as k
import power
import revb
import route
from revd_jlc import SELECTED_PARTS
from revd_integrate import blocks,kind
from studium_e import secondary
from revf_control import BLOCKS

NAME='Zasilacz_RevF_Moc'
D=Path('outputs/Zasilacz_RevD_JLCPCB')
E=Path('outputs/Studium_RevE')
DEST=Path('outputs')/NAME
ORIGIN=(75,70)
SIZE=(55.5,34)
PORT=(127.4,91.2)
SHARED={'/S_RAW','/S_RTN'}


def devices():
    result=[replace(d,part=SELECTED_PARTS.get(d.ref,d.part)) for d in revb.circuit() if not secondary(d.ref)]
    return result+[power.Device('J101','26 V / RTN','E27:Harness_26V_RTN',
                  {1:'S_RAW',2:'S_RTN'},(0,0),(129.54,202.565),'LINK')]


def write_schematic(parts):
    sheet=k.uid()
    symbols,items,paths={},{},{}
    for d in parts:
        sid=k.uid()
        paths[d.ref]='/'+sheet+'/'+sid
        lib='E27:Flyback_'+d.kind
        x,y=(round(round(v/1.27)*1.27,3) for v in d.schematic)
        if d.kind in ('C','CP','D','Z','R','L','F','MOV'):
            graphic,pins=power.two(d.kind)
            ends=[(1,-3.81,0),(2,3.81,0)]
            gap=3.81
        else:
            half,h,defs=BLOCKS.get(d.kind) or power.complex_pins(d.kind)
            graphic=k.box(-half,h,half,-h,'background')
            if d.kind=='LYT': graphic+=k.poly([(0,-h),(0,h)])
            pins=[k.pin(n,label,xx,yy,orient) for n,label,xx,yy,orient in defs]
            ends=[(n,xx,yy) for n,_,xx,yy,_ in defs]
            gap=h+2.54
        symbols[lib]=k.symbol(lib,d.ref.rstrip('0123456789'),graphic,pins,d.kind not in ('C','CP','D','Z','R','L','F','MOV'))
        instance=k.placed(lib,d.ref,d.val,d.footprint,x,y,sid,NAME,sheet,list(d.connection))
        instance=instance.replace(k.prop('Reference',d.ref,x,y-3.81),k.prop('Reference',d.ref,x,y-gap))
        instance=instance.replace(k.prop('Value',d.val,x,y+3.81),k.prop('Value',d.val,x,y+gap))
        content=[instance]
        for n,dx,dy in ends:
            x1,y1=x+dx,y-dy
            x2=x1+(2.54 if dx>0 else -2.54)
            content.extend((k.wire(x1,y1,x2,y1),k.label(d.connection[n],x2,y1,0 if dx>0 else 180)))
        items[d.ref]=content
    notes=[
        k.note('E27 / REV F / PŁYTKA MOCY 230 V AC → 26 V DC',18,18),
        k.note('01   WEJŚCIE, PROSTOWNIK I FILTR',18,28),
        k.note('02   FLYBACK I BARIERA IZOLACJI',155,28),
        k.note('03   PROSTOWNIK I REGULACJA WTÓRNA',276,28),
        k.note('04   POŁĄCZENIE Z PŁYTKĄ STEROWANIA',18,183),
        k.note('J101-1 do J102-1 (S_RAW). J101-2 do J102-2 (S_RTN).',18,228),
        k.note('Pętla prostownika D7 i kondensatora C6 pozostaje na płytce mocy.',18,237),
    ]
    k.schematic(DEST,NAME,sheet,'Velluneo E27 Rev F / płytka mocy',list(symbols.values()),
                [*notes,*(i for row in items.values() for i in row)],'A3','F')
    return sheet,paths


def set_libraries(parts):
    (DEST/'E27.pretty').mkdir(parents=True,exist_ok=True)
    for d in parts:
        if not d.footprint.startswith('E27:'): continue
        name=d.footprint.split(':')[1]
        source=(E if d.ref=='J101' else D)/'E27.pretty'/f'{name}.kicad_mod'
        copy2(source,DEST/'E27.pretty'/source.name)
        model=E/f'{name}.wrl'
        if model.exists(): copy2(model,DEST/model.name)
    for f in ('fp-lib-table','sym-lib-table'):
        copy2(D/f,DEST/f)
    name=D.name
    for ext in ('pro','dru'):
        data=(D/f'{name}.kicad_{ext}').read_text(encoding='utf8').replace(name,NAME)
        (DEST/f'{NAME}.kicad_{ext}').write_text(data,encoding='utf8')


def tracks_for_router(board):
    for t in board.GetTracks():
        net=t.GetNetname().lstrip('/')
        a,c=route.rel(t.GetStart()),route.rel(t.GetEnd())
        if isinstance(t,p.PCB_VIA):
            yield net,None,a,c,p.ToMM(t.GetWidth(p.F_Cu))
        else:
            yield net,route.LAYERS.index(t.GetLayer()),a,c,p.ToMM(t.GetWidth())


def related_anchors(board,pad,field):
    nodes={}
    for item in board.GetConnectivity().GetConnectedItems(pad):
        if isinstance(item,p.PCB_VIA):
            points=[route.rel(item.GetPosition())]
            layers=(0,1)
        elif isinstance(item,p.PCB_TRACK):
            a,c=route.rel(item.GetStart()),route.rel(item.GetEnd())
            samples=max(1,ceil(dist(a,c)/.20))
            points=[tuple(a[i]+(c[i]-a[i])*j/samples for i in range(2)) for j in range(samples+1)]
            layers=(route.LAYERS.index(item.GetLayer()),)
        elif isinstance(item,p.PAD):
            points=[route.rel(item.GetPosition())]
            layers=[i for i,l in enumerate(route.LAYERS) if item.IsOnLayer(l)]
        else:
            continue
        for pt in points:
            x,y=route.grid_coord(*pt)
            for k in layers:
                if not field[k,x,y]:
                    nodes.setdefault((x,y,k),pt)
    return nodes


def add_output_track(board, fps, port, source):
    board.BuildConnectivity()
    net=port.GetNetname().lstrip('/')
    width=.50
    pads=route.get_pad_data(fps)
    block,via=route.fields(net,pads,list(tracks_for_router(board)),width)
    x,y=route.grid_coord(*route.rel(port.GetPosition()))
    starts=[(x,y,i) for i in range(2) if not block[i,x,y]]
    ends=related_anchors(board,source,block)
    path=route.search(starts,list(ends),block,via)
    if not path:
        raise RuntimeError(f'Unable to route J101 pad {port.GetNumber()} {net}')
    def grid(q): return (q[0]*route.STEP,q[1]*route.STEP)
    def draw(a,b,k_index):
        if dist(a,b)>1e-6:
            k.track(board,port.GetNet(),[route.abspt(*a),route.abspt(*b)],width,route.LAYERS[k_index])
    points=route.squish(path)
    draw(route.rel(port.GetPosition()),grid(points[0]),points[0][2])
    for a,c in zip(points,points[1:]):
        if a[2]==c[2]:
            draw(grid(a),grid(c),a[2])
        else:
            route.via(board,port.GetNet(),*grid(a))
    draw(grid(points[-1]),ends[points[-1]],points[-1][2])
    print(f'J101-{port.GetNumber()} {net}, {len(path)} steps')


def board_from_d(parts,sheet,paths):
    source=(D/f'{D.name}.kicad_pcb').read_text(encoding='utf8')
    kept={q.ref for q in parts}
    nets={'/'+n for q in parts for n in q.connection.values()}
    max_x=ORIGIN[0]+SIZE[0]
    elements=[]
    for item in blocks(source):
        tag=kind(item)
        if tag=='footprint':
            ref=re.search(r'\(property "Reference" "([^"]+)"',item)[1]
            if ref not in kept:
                continue
            item=re.sub(r'\(path "[^"]+"\)',lambda _:f'(path "{paths[ref]}")',item,count=1)
        elif tag in ('segment','via'):
            net=re.search(r'\(net "([^"]+)"\)',item)[1]
            if net not in nets:
                continue
            if net in SHARED:
                locations=[float(x) for x in re.findall(r'\((?:start|end|at) ([\d.]+) [\d.]+\)',item)]
                if max(locations)>(124 if net=='/S_RTN' else max_x-1):
                    continue
        elif tag=='zone':
            if '(net "/P_0")' not in item:
                continue
        elif tag.startswith('gr_') and ('"Edge.Cuts"' in item or
                (tag=='gr_text' and re.match(r'\(gr_text "(?:TP10|E27 / REV)',item))):
            continue
        elements.append(item)
    boardfile=DEST/f'{NAME}.kicad_pcb'
    boardfile.write_text('(kicad_pcb\n'+'\n'.join(elements)+'\n)\n',encoding='utf8')
    board=p.LoadBoard(str(boardfile))
    fps={fp.GetReference():fp for fp in board.GetFootprints()}
    ox,oy=ORIGIN
    w,h=SIZE
    outline=[(ox,oy),(ox+w,oy),(ox+w,oy+h),(ox,oy+h),(ox,oy)]
    for a,b in zip(outline,outline[1:]):
        k.shape(board,p.Edge_Cuts,a,b)
    board.GetDesignSettings().SetAuxOrigin(k.pt(ox,oy+h))
    k.txt(board,'E27 / REV F MOC',117.5,71.5,.8,p.Dwgs_User)
    connect=k.footprint(board,DEST,'E27:Harness_26V_RTN','J101','26 V / RTN',*PORT,0,
                        paths['J101'].split('/')[-1],sheet,
                        {str(i):board.FindNet(n) for i,n in [(1,'/S_RAW'),(2,'/S_RTN')]})
    fps['J101']=connect
    route.ORIGIN=ORIGIN
    route.NX,route.NY=[round(s/route.STEP)+1 for s in SIZE]
    route.BOUNDARY=30
    route.MAINS_ACROSS=True
    add_output_track(board,fps,connect.FindPadByNumber('1'),fps['C6'].FindPadByNumber('1'))
    add_output_track(board,fps,connect.FindPadByNumber('2'),fps['R9'].FindPadByNumber('1'))
    assert p.SaveBoard(str(DEST/f'{NAME}.kicad_pcb'),board)


if __name__=='__main__':
    parts=devices()
    set_libraries(parts)
    board_from_d(parts,*write_schematic(parts))

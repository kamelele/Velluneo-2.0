"""Create the Rev F secondary control board from the Rev D circuit and Rev E split."""
from collections import Counter
from dataclasses import replace
from math import dist
from pathlib import Path
from shutil import copy2
import argparse
import csv

import build as k
import power
import revb
import revb2_guard as guard
from revd_integrate import ref_name
from revd_jlc import CATALOG, SELECTED_PARTS
import route
import studium_e
from studium_e import SECOND, options, place
from revb1_thermal import add_zone

NAME = 'Zasilacz_RevF_Sterowanie'
ORIGIN = (75, 70)
BASE = Path('outputs/Zasilacz_RevD_JLCPCB')
STUDY = Path('outputs/Studium_RevE')
R = guard.R
C = guard.C
F = k.p.F_Cu
EXCLUDED = {'U4','U5','D1','C10','TP2','TP3','TP5'}
SOURCE_FPS = {'PWP0016A','E27_Al5812_MSOP','Harness_4pos','Harness_3pos','TPS7A16_DGN'}


def block(half, left, right):
    h = 1.27*(max(len(left),len(right))+1)
    pins = []
    for side,group in ((-1,left),(1,right)):
        for i,(n, name) in enumerate(group):
            pins.append((n,name,side*(half+2.54),1.27*(len(group)-1-2*i),0 if side<0 else 180))
    return half,h,pins


BLOCKS = {
    'LINK': block(7.62,((1,'26 V'),(2,'RTN')),()),
    'LOCK': block(10.16,((1,'1A'),(2,'1B'),(4,'2A'),(5,'2B'),(9,'3A'),(10,'3B'),
                        (12,'4A'),(13,'4B'),(14,'VCC'),(7,'GND')),((3,'1Y'),(6,'2Y'),(8,'3Y'),(11,'4Y'))),
    'SWITCH': block(8.89,((2,'B1'),(1,'E1'),(5,'B2'),(4,'E2')),((6,'C1'),(3,'C2'))),
    'PG_FET': block(6.35,((1,'G'),(2,'S')),((3,'D'),)),
    'HARNESS': block(8.89,((1,'S1 feed'),(2,'S1 return'),(3,'eFuse out'),(4,'LED A+')),()),
}


def device_from_guard(p):
    return power.Device(ref_name(p.ref),p.value,p.fp,
        {n:{'S_K1':'S_LED_KA','S_K2':'S_LED_KB','CLR_N':'FAULT_N'}.get(net,net) for n,net in p.pins.items()},
        p.xy,p.sch,'G_'+p.kind,p.rotation,p.mpn)


def circuit():
    parts = {p.ref:p for p in revb.circuit() if p.ref in SECOND}
    for ref in ('J2',):
        parts[ref] = replace(parts[ref],connection={1:'S_ENFEED',2:'S1_RETURN',3:'S_FUSED',4:'S_LED_PLUS'},kind='HARNESS')
    parts['J102'] = power.Device('J102','26 V / RTN','E27:Harness_26V_RTN',
                                   {1:'S_RAW',2:'S_RTN'},(0,0),(35,47),'LINK')
    for p in guard.PARTS:
        if p.ref != 'J1' and p.ref not in EXCLUDED:
            part = device_from_guard(p)
            parts[part.ref] = part

    def change(ref, **kw):
        parts[ref] = replace(parts[ref],**kw)

    change('U103',val='74LVC132A',part='74LVC132APW,118',kind='LOCK',schematic=(326,53.34),
           connection={1:'FAULT_N',2:'LATCH_OK',3:'FAULT_LATCH',4:'PG',5:'FAULT_LATCH',6:'LATCH_OK',
                       7:'S_RTN',8:'INHIBIT',9:'PG',10:'LATCH_OK',11:'PERMIT',12:'INHIBIT',13:'INHIBIT',14:'V3V3'})
    change('R110',val='10k 1%',part='ERJ-3EKF1002V',kind='R',connection={1:'PERMIT',2:'RELEASE_B'},schematic=(325,110))
    change('R111',val='100k 1%',part='ERJ-3EKF1003V',kind='R',connection={1:'RELEASE_B',2:'S_RTN'},schematic=(325,125))
    change('R112',kind='R',connection={1:'S1_RETURN',2:'S_EN'},schematic=(333,147.32))
    change('C108',kind='C',connection={1:'RELEASE_B',2:'S_RTN'},schematic=(373,125))
    change('C109',schematic=(375,80))
    change('R109',schematic=(300,95))
    change('TP104',val='FAULT_N',schematic=(177,147.32))
    change('TP106',schematic=(247,147.32))
    change('TP101',schematic=(84,147.32))
    parts['R113'] = power.Device('R113','100k 1%',R,{1:'S_RAW',2:'HOLD_B'},(0,0),(373,147.32),'R',part='ERJ-3EKF1003V')
    parts['Q101'] = power.Device('Q101','MMDT3904','Package_TO_SOT_SMD:SOT-363_SC-70-6',
              {1:'S_RTN',2:'HOLD_B',3:'HOLD_B',4:'PG_RETURN',5:'RELEASE_B',6:'S_EN'},
              (0,0),(374.65,103),'SWITCH',part='MMDT3904-7-F')
    parts['Q102'] = power.Device('Q102','2N7002BK','Package_TO_SOT_SMD:SOT-23',
              {1:'PG',2:'S_RTN',3:'PG_RETURN'},(0,0),(277,125),'PG_FET',part='2N7002BK,215')

    for ref, part in list(parts.items()):
        if ref in SECOND:
            continue
        pn = SELECTED_PARTS.get(ref,part.part)
        if ref in {'R105','R107'}:
            pn = 'RT0603BRD07330KL'
        if ref in {'D102','D103'}:
            pn = 'PMEG6010CEH-QX'
        if ref in {'R110','R111','R112','R113'}:
            pn = part.part if ref != 'R112' else 'ERJ-3EKF1003V'
        parts[ref] = replace(part,part=pn)
    return parts


def symbol(part):
    kind = part.kind
    if kind.startswith('G_') and kind[2:] not in ('R','C','D'):
        probe = guard.Part(part.ref,part.val,part.footprint,kind[2:],part.connection,part.schematic,part.xy,part.part)
        return guard.symbol_for(probe)
    if kind.removeprefix('G_') in ('R','C','D'):
        art, pins = power.two(kind.removeprefix('G_'))
        return art,pins,[(1,-3.81,0),(2,3.81,0)],3.81
    half,h,defs = BLOCKS.get(kind) or power.complex_pins(kind)
    pins = [k.pin(n,name,x,y,orientation) for n,name,x,y,orientation in defs]
    ends = [(n,x,y) for n,_,x,y,_ in defs]
    return k.box(-half,h,half,-h,'background'),pins,ends,h+2.54


def assemble():
    dest,board,sheet = k.begin(NAME,'Secondary only',.16,.50)
    project = dest/f'{NAME}.kicad_pro'
    content = project.read_text(encoding='utf8')
    for old,new in (('"min_track_width": 0.2','"min_track_width": 0.18'),
                    ('"min_through_hole_diameter": 0.3','"min_through_hole_diameter": 0.2'),
                    ('"min_via_diameter": 0.55','"min_via_diameter": 0.45')):
        content = content.replace(old,new)
    k.save(project,content)
    board.SetCopperLayerCount(4)
    for lib in SOURCE_FPS:
        copy2(BASE/'E27.pretty'/f'{lib}.kicad_mod',dest/'E27.pretty'/f'{lib}.kicad_mod')
        model = STUDY/f'{lib}.wrl'
        if model.exists():
            copy2(model,dest/model.name)
    copy2(STUDY/'E27.pretty'/'Harness_26V_RTN.kicad_mod',dest/'E27.pretty'/'Harness_26V_RTN.kicad_mod')

    old = k.p.LoadBoard(str(STUDY/'E_Sterowanie.kicad_pcb'))
    old_fps = {fp.GetReference():fp for fp in old.GetFootprints()}
    parts = circuit()
    assert set(parts) == set(old_fps)-{ref_name(ref) for ref in EXCLUDED} | {'Q101','Q102','R113'}
    nets = k.nets_for(board, (net for p in parts.values() for net in p.connection.values() if net))
    items,definitions,footprints = [],{},{}
    for part in parts.values():
        ref = part.ref
        x,y = (round(round(v/1.27)*1.27,3) for v in part.schematic)
        art,pins,ends,spacing = symbol(part)
        sid = k.uid()
        kind = part.kind.removeprefix('G_')
        lib_id = 'E27:RevF_'+kind
        definitions[lib_id] = k.symbol(lib_id,ref.rstrip('0123456789'),art,pins,kind not in ('R','C','D'))
        placed = k.placed(lib_id,ref,part.val,part.footprint,x,y,sid,NAME,sheet,list(part.connection))
        placed = placed.replace(k.prop('Reference',ref,x,y-3.81),k.prop('Reference',ref,x,y-spacing))
        placed = placed.replace(k.prop('Value',part.val,x,y+3.81),k.prop('Value',part.val,x,y+spacing))
        if kind == 'TP':
            placed = placed.replace('(in_bom yes)','(in_bom no)')
        items.append(placed)
        pin_nets = {}
        for n,dx,dy in ends:
            net = part.connection[n]
            xx,yy = x+dx,y-dy
            if net is None:
                items.append(f'(no_connect (at {k.fmt(xx)} {k.fmt(yy)}) (uuid "{k.uid()}"))')
                names = guard.PIN_NAMES[kind]
                nc = k.p.NETINFO_ITEM(board,f'unconnected-({ref}-{names[n-1]}-Pad{n})')
                board.Add(nc)
                pin_nets[str(n)] = nc
            else:
                end = xx+(-2.54 if dx < 0 else 2.54)
                items.extend([k.wire(xx,yy,end,yy),k.label(net,end,yy,180 if dx<0 else 0)])
                pin_nets[str(n)] = nets[net]
        fp = k.footprint(board,dest,part.footprint,ref,part.val,*ORIGIN,0,sid,sheet,pin_nets)
        prior = old_fps.get(ref)
        if (prior and prior.GetLayer() != F) or ref == 'R113':
            fp.Flip(fp.GetPosition(),k.p.FLIP_DIRECTION_LEFT_RIGHT)
        footprints[ref] = fp
    for label,x,y in [
        ('E27 REV F / STEROWANIE WTÓRNE 26 V',18,15),
        ('01   WEJŚCIE DC I SZYNA 3V3',18,27),
        ('02   NIEZALEŻNA DETEKCJA K1 I K2',146,27),
        ('03   PAMIĘĆ AWARII I WYMUSZENIE SHDN',278,27),
        ('04   eFUSE, S1/TH1, S2 I REGULACJA PRĄDU',18,164),
        ('J2-1 > S1 (NO) > TH1 (NC) > J2-2. J2-3 > S2 (NO) > J2-4.',211,232),
        ('Q101A zwiera S_EN przy braku zezwolenia. Q102 blokuje zwolnienie przy PG = 0.',270,154),
    ]:
        items.append(k.note(label,x,y))
    k.schematic(dest,NAME,sheet,'E27 Rev F / płytka sterowania i zabezpieczeń',list(definitions.values()),items,'A3','F')
    return dest,board,parts,footprints,nets


def fanout(board,footprints,nets):
    """Reserve short routes from dense SMD pads to through-vias before global routing."""
    pads = route.get_pad_data(footprints)
    refs = {'U2','U101','U102','U103'}
    first = {('Q101','5'),('R111','1'),('D102','1'),('D103','1'),('U4','8'),('U103','7')}
    critical = {('U2','7'),('Q102','1'),('C105','1'),('R107','2'),('R108','1'),('C103','1'),
                ('C11','1'),('R17','1'),('R14','1'),('D102','2'),('U103','4')} | first
    centers = {ref:route.rel(fp.GetPosition()) for ref,fp in footprints.items()}
    selected = [p for p in pads if p[2] in nets and len(p[6])==1 and (p[0] in refs or p[2]=='S_RTN' or p[:2] in critical)]
    selected.sort(key=lambda p:(p[:2] not in first, p[:2] not in critical, dist(p[3:5],centers[p[0]])>1, p[0],int(p[1])))
    routes,ports,escaped = [],{},set()
    step = route.STEP
    for ref,num,net,x,y,_,(layer,) in selected:
        width = route.SIGNAL_WIDTH
        block,via_bad = route.fields(net,pads,routes,width)
        cx,cy = centers[ref]
        # A package pin normally escapes radially. A centre pad can take either end.
        dx,dy = x-cx,y-cy
        if abs(dx)>=abs(dy) and abs(dx)>.8:
            dy = 0
        elif abs(dy)>.8:
            dx = 0
        length = max((dx*dx+dy*dy)**.5, .1)
        ox,oy = route.grid_coord(x,y)
        if block[layer,ox,oy]:
            continue
        opts = []
        for i in range(max(1,ox-38),min(route.NX-1,ox+39)):
            for j in range(max(1,oy-38),min(route.NY-1,oy+39)):
                if via_bad[i,j] or block[layer,i,j]:
                    continue
                a,b = i*step-x,j*step-y
                distance = (a*a+b*b)**.5
                if distance>.55 and distance<=4.1:
                    score = distance - .56*(a*dx+b*dy)/length
                    opts.append((score,i,j))
        # Restrict the escape itself to the pad's copper layer.
        for side in range(len(block)):
            if side != layer:
                block[side,:,:] = True
        for _,i,j in sorted(opts)[:18]:
            path = route.search([(ox,oy,layer)],[(i,j,layer)],block,via_bad)
            if not path or len(path)>58:
                continue
            points = [(x,y)]+[(u*step,v*step) for u,v,_ in route.squish(path)]
            for a,b in zip(points,points[1:]):
                if dist(a,b)>1e-5:
                    k.track(board,nets[net],[route.abspt(*a),route.abspt(*b)],width,route.LAYERS[layer])
                    routes.append((net,layer,a,b,width))
            v = i*step,j*step
            route.via(board,nets[net],*v)
            routes.append((net,None,v,v,route.VIA_D))
            via_layers = tuple(i for i,l in enumerate(route.LAYERS) if l!=k.p.In1_Cu or net=='S_RTN')
            ports.setdefault(net,[]).append((ref,num,net,*v,(v[0],v[1],v[0],v[1]),via_layers))
            escaped.add((ref,num))
            break
    print(f'Fanout of {len(escaped)}/{len(selected)} critical pads',flush=True)
    return routes,ports,escaped


def make(seed, width, height, placement_only, order):
    dest,board,parts,footprints,nets = assemble()
    studium_e.EDGE = 1.2
    geom = {ref:options(fp) for ref,fp in footprints.items()}
    ns = {ref:set(p.connection.values())-{None} for ref,p in parts.items()}
    counts = Counter(net for subset in ns.values() for net in subset)
    ranked = {ref:sorted(n for n in subset if 1<counts[n]<10) for ref,subset in ns.items()}
    links = {
        'U2': {'C11':4,'C13':4,'R14':2,'R15':2,'R16':2,'C12':2,'R18':2,'J102':2},
        'U3': {'C14':4,'R20':2},
        'U4': {'C15':4,'R21':2},
        'U101': {'C101':4,'C102':4,'C103':2,'R101':2},
        'U102': {'C104':2,'C105':2,'C107':4},
        'U103': {'C109':4,'Q101':2},
        'Q101': {'Q102':3,'C108':2},
    }
    for ref,relatives in links.items():
        for other in relatives:
            edge = f'layout-{ref}-{other}'
            ranked[ref].extend((edge,edge))
            ranked[other].extend((edge,edge))
    candidates = []
    for test_seed in range(seed,seed+14):
        loc = place(parts,(width,height,None),geom,test_seed,{},ranked)
        if loc:
            score = sum(cost*dist(loc[ref][:2],loc[other][:2]) for ref,relatives in links.items()
                        for other,cost in relatives.items())
            candidates.append((score,test_seed,loc))
    if not candidates:
        raise SystemExit(f'No placement for {width}x{height} from seed {seed}')
    _,test_seed,loc = min(candidates)
    print(f'Placement seed {test_seed}, {len(loc)} footprints in {width}x{height}',flush=True)
    ox,oy = ORIGIN
    for ref,(x,y,angle) in loc.items():
        fp = footprints[ref]
        fp.SetPosition(k.pt(ox+x,oy+y))
        fp.SetOrientationDegrees(angle)
    edges = [(ox,oy),(ox+width,oy),(ox+width,oy+height),(ox,oy+height),(ox,oy)]
    for a,b in zip(edges,edges[1:]):
        k.shape(board,k.p.Edge_Cuts,a,b)
    board.GetDesignSettings().SetAuxOrigin(k.pt(ox,oy+height))
    k.txt(board,'E27 / REV F',ox+width/2,oy+height-1,1,k.p.Dwgs_User)
    if not placement_only:
        route.ORIGIN = ORIGIN
        route.NX,route.NY = [round(v/route.STEP)+1 for v in (width,height)]
        route.FRONT_ESCAPE = {}
        route.LAYERS = [k.p.F_Cu,k.p.B_Cu,k.p.In2_Cu,k.p.In1_Cu]
        route.DEFAULT_CLEARANCE = .16
        route.SIGNAL_WIDTH = .18
        route.VIA_D,route.VIA_DRILL = .45,.20
        route.RESERVED_LAYER = k.p.In1_Cu,'S_RTN'
        route.BOUNDARY = -4.25
        sequences = [
            ['RELEASE_B','LDO_IN','S_LED_KB','S_EN','K2_F','K1_F','PG','DELAY','S_RAW',
             'INHIBIT','FAULT_LATCH','LATCH_OK','FAULT_N','HOLD_B','PG_RETURN','PERMIT','REF','S_OVP','S_ILIM','S_SLEW'],
            ['K1_F','K2_F','REF','S_EN','S_OVP','S_ILIM','S_SLEW','DELAY','HOLD_B','PG_RETURN','RELEASE_B',
             'PERMIT','INHIBIT','LATCH_OK','FAULT_LATCH','FAULT_N','PG','LDO_IN'],
        ]
        route.EARLY = sequences[order]
        seed_routes,ports,escaped = fanout(board,footprints,nets)
        route.route_board(board,footprints,nets,controller_fanout=False,
                          seed_routes=seed_routes,anchors=ports,
                          term_filter=lambda ref,num: (ref,num) not in escaped)
        for layer in (k.p.F_Cu,k.p.B_Cu,k.p.In1_Cu):
            add_zone(board,'RTN','/S_RTN',(ox+.55,oy+.55,ox+width-.55,oy+height-.55),layer)
    assert k.p.SaveBoard(str(dest/f'{NAME}.kicad_pcb'),board)
    catalog = {**CATALOG,'74LVC132APW,118':'Nexperia-74LVC132APW118/C548102','MMDT3904-7-F':'C83572','2N7002BK,215':'C282405'}
    with (dest/'BOM_RevF.csv').open('w',encoding='utf8',newline='') as f:
        writer = csv.writer(f,lineterminator='\n')
        writer.writerow(('Ref','Wartość','MPN','Footprint','LCSC Part #','Źródło'))
        for ref,p in parts.items():
            if ref.startswith('TP'):
                continue
            value = catalog.get(p.part,'')
            code = value.split('/')[-1]
            src = ('https://jlcpcb.com/partdetail/'+value if '/' in value else
                   ('https://www.lcsc.com/product-detail/'+code+'.html' if code else ''))
            writer.writerow((ref,p.val,p.part,p.footprint,code,src))


if __name__ == '__main__':
    cli = argparse.ArgumentParser()
    cli.add_argument('--seed',type=int,default=0)
    cli.add_argument('--width',type=float,default=30)
    cli.add_argument('--height',type=float,default=24)
    cli.add_argument('--placement',action='store_true')
    cli.add_argument('--order',type=int,choices=(0,1),default=0)
    args = cli.parse_args()
    make(args.seed,args.width,args.height,args.placement,args.order)

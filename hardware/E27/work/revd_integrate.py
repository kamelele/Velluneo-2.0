"""Integrate the Rev B1 flyback and Rev B2 guard on one PCB."""
import re
from pathlib import Path
from shutil import copy2, copytree

import build as k
import pcbnew as pcb
import route

MAIN = 'Zasilacz_RevB1'
GUARD = 'Zasilacz_RevB2_Ochrona'
NAME = 'Zasilacz_RevD_JLCPCB'
OUT = Path('outputs')
DEST = OUT / NAME
ORIGIN = (75, 70)
SIZE = (96, 34)
GUARD_X = 66.5
GUARD_Y = 257.81
ALIASES = {'S_K1':'S_LED_KA','S_K2':'S_LED_KB'}
GUARD_POS = {
    'U1':(5.4,7.0),'D2':(2.8,2.7),'D3':(8.4,2.5),
    'C1':(3.4,11.3),'C2':(11.2,6.0),'C3':(10.1,8.1),'R1':(9.8,11.0),'R2':(10.3,13.6),
    'U2':(9.0,20.7),'R5':(2.8,16.5),'R6':(4.0,16.5),'C4':(7.2,16.5),
    'R7':(2.8,22.1),'R8':(4.0,22.1),'C5':(7.2,22.1),
    'R3':(8.6,16.5),'R4':(9.2,25.3),'C6':(13.2,25.3),'C7':(13.0,18.1),
    'U3':(17.4,12.2),'D1':(15.0,20.2),'R9':(15.4,8.3),'R10':(12.9,10.6),
    'C8':(12.8,13.2),'C9':(18.3,6.2),
    'U4':(24.4,10.8),'C10':(24.5,6.6),
    'U5':(24.0,21.3),'R11':(23.0,16.8),'R12':(18.2,23.9),
    'TP1':(4.0,30.0),'TP2':(8.0,30.0),'TP3':(12.0,30.0),
    'TP4':(16.0,30.0),'TP5':(20.0,30.0),'TP6':(24.0,30.0),
}


def ref_name(ref):
    match = re.fullmatch(r'([A-Z]+)(\d+)', ref)
    assert match, ref
    return match[1]+str(100+int(match[2]))


def blocks(expression):
    """Yield immediate child lists of a KiCad S-expression."""
    depth = 0
    quoted = False
    escaped = False
    for i,c in enumerate(expression):
        if quoted:
            if escaped:
                escaped = False
            elif c == '\\':
                escaped = True
            elif c == '"':
                quoted = False
        elif c == '"':
            quoted = True
        elif c == '(':
            if depth == 1:
                start = i
            depth += 1
        elif c == ')':
            depth -= 1
            if depth == 1:
                yield expression[start:i+1]
    assert depth == 0


def kind(block):
    return re.match(r'\(([^\s()]+)',block)[1]


def coordinate(item):
    match = re.search(r'\((?:at|xy) (-?[\d.]+) (-?[\d.]+)',item)
    return (float(match[1]),float(match[2])) if match else None


def copy_project():
    DEST.mkdir(exist_ok=True)
    for base in (MAIN, GUARD):
        source = OUT / base
        copytree(source/'E27.pretty',DEST/'E27.pretty',dirs_exist_ok=True)
        for model in source.glob('*.wrl'):
            copy2(model,DEST/model.name)
    for filename in ('fp-lib-table','sym-lib-table'):
        copy2(OUT/MAIN/filename,DEST/filename)
    for suffix in ('pro','dru'):
        original = (OUT/MAIN/f'{MAIN}.kicad_{suffix}').read_text(encoding='utf-8')
        if suffix == 'dru':
            for side in ('A', 'B'):
                primary = f"{side}.NetName =~ '/P_*'"
                secondary = f"{side}.NetName != '' && {side}.NetName !~ 'unconnected-*' && !({primary})"
                original = original.replace(f"{side}.NetName =~ '/S_*'", f"({secondary})")
        (DEST/f'{NAME}.kicad_{suffix}').write_text(original.replace(MAIN,NAME),encoding='utf-8')


def make_schematic():
    mains = list(blocks((OUT/MAIN/f'{MAIN}.kicad_sch').read_text(encoding='utf-8')))
    guard = list(blocks((OUT/GUARD/f'{GUARD}.kicad_sch').read_text(encoding='utf-8')))
    mains_uuid = next(item.split('"')[1] for item in mains if kind(item)=='uuid')
    guard_uuid = next(item.split('"')[1] for item in guard if kind(item)=='uuid')
    lib_defs = [symbol for sheet in (mains,guard) for item in sheet if kind(item)=='lib_symbols'
                for symbol in blocks(item)]
    lib_defs = [s.replace('"SHDN" (effects', '"S1 return" (effects') if s.startswith('(symbol "E27:J4"') else s
                for s in lib_defs]
    parts = []
    changed = 0
    allowed = {'symbol','wire','label','text','no_connect'}
    for item in mains:
        tag = kind(item)
        if tag not in allowed:
            continue
        if tag == 'label' and item.startswith('(label "S_EN"') and coordinate(item)==(222.25,182.88):
            item = item.replace('"S_EN"','"S1_RETURN"',1)
            changed += 1
        if tag == 'text':
            item = item.replace('/ Rev B1','/ Rev D')
            item = item.replace('PROTOTYP LABORATORYJNY.', 'PLYTKA ZINTEGROWANA - PRZEGLAD PRZED URUCHOMIENIEM.')
        parts.append(item.replace(f'"{MAIN}"',f'"{NAME}"'))
    assert changed == 1, changed
    for item in guard:
        tag = kind(item)
        if tag not in allowed:
            continue
        if tag == 'symbol':
            ref = re.search(r'\(property "Reference" "([^"]+)"',item)[1]
            if ref == 'J1':
                continue
            new = ref_name(ref)
            item = item.replace(f'(property "Reference" "{ref}"',f'(property "Reference" "{new}"')
            item = item.replace(f'(reference "{ref}")',f'(reference "{new}")')
        if tag in {'wire','label'}:
            x,y = coordinate(item)
            if x < 27 and 36 < y < 53:
                continue
            if tag == 'label':
                for old,new in ALIASES.items():
                    item = item.replace(f'(label "{old}"',f'(label "{new}"')
        if tag == 'text':
            if any(text in item for text in ('J1-5:', 'Otwarty PhotoMOS', '01   WIAZKA')):
                continue
            item = item.replace('E27 REV B2 / MODUL PROB OCHRONY ZWARCIOWEJ / TYLKO STRONA WTORNA',
                                'E27 REV D / OCHRONA ZWARCIOWA NA PCB ZASILACZA')
        item = re.sub(r'(\((?:at|xy) -?[\d.]+ )(-?[\d.]+)',
                      lambda m: m[1]+k.fmt(float(m[2])+GUARD_Y),item)
        parts.append(item.replace(f'"{GUARD}"',f'"{NAME}"').replace('/'+guard_uuid,'/'+mains_uuid))
    parts.extend([
        k.note('ZASILANIE 3V3 I WYKRYWANIE ZWARCIA',18,GUARD_Y+28),
        k.note('J2-2: powrot S1/TH1 do PhotoMOS. R112 ogranicza poziom SHDN.',18,GUARD_Y+155),
        k.note('Wykrycie K1/K2 zeruje PERMIT. Reset wymaga zaniku PG.',18,GUARD_Y+164),
    ])
    contents = '\n'.join(parts)
    (DEST/'E27.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor")\n'
        +'\n'.join(item.replace('"E27:','"',1) for item in lib_defs)+'\n)',encoding='utf-8')
    (DEST/f'{NAME}.kicad_sch').write_text(
        f'(kicad_sch (version 20250114) (generator "eeschema") (uuid "{mains_uuid}") '
        '(paper "A2" portrait) (title_block (title "Velluneo E27 / zintegrowany zasilacz Rev D") (rev "D"))\n'
        +'(lib_symbols '+'\n'.join(lib_defs)+')\n'+contents+'\n)',encoding='utf-8')
    return mains_uuid,guard_uuid


def point(x,y):
    return k.pt(x,y)


def net_for(board, name):
    net = board.FindNet(name)
    if net is None:
        net = pcb.NETINFO_ITEM(board,name)
        board.Add(net)
    return net


def guard_net(name,old_ref,new_ref):
    if name.startswith('unconnected-'):
        return name.replace('('+old_ref+'-','('+new_ref+'-',1)
    return '/'+ALIASES.get(name[1:],name[1:])


def keep_enable_branch(board):
    end = point(139.1,74.4)
    short = point(139.05,74.43)
    cut = point(137.7,75.8)
    old = [item for item in board.GetTracks() if item.GetNetname()=='/S_EN'
           and item.GetLayer()==pcb.B_Cu and end in (item.GetStart(),item.GetEnd())]
    assert len(old)==2
    for item in old:
        if short in (item.GetStart(),item.GetEnd()):
            board.Remove(item)
        elif item.GetStart()==end:
            item.SetStart(cut)
        else:
            item.SetEnd(cut)
    return cut


def wire_obstacles(board):
    for item in board.GetTracks():
        a,c = route.rel(item.GetStart()),route.rel(item.GetEnd())
        if isinstance(item,pcb.PCB_VIA):
            yield item.GetNetname().lstrip('/'),None,a,c,pcb.ToMM(item.GetWidth(pcb.F_Cu))
        else:
            yield item.GetNetname().lstrip('/'),route.LAYERS.index(item.GetLayer()),a,c,pcb.ToMM(item.GetWidth())


def anchor(net,point,layers):
    x,y = route.rel(point)
    return [(f'#{net}','0',net,x,y,(x,y,x,y),layers)]


def make_board(mains_uuid,guard_uuid):
    board = pcb.LoadBoard(str(OUT/MAIN/f'{MAIN}.kicad_pcb'))
    old_guard = pcb.LoadBoard(str(OUT/GUARD/f'{GUARD}.kicad_pcb'))
    footprints = {fp.GetReference():fp for fp in board.GetFootprints()}
    cut = keep_enable_branch(board)
    footprints['J2'].FindPadByNumber('2').SetNet(net_for(board,'/S1_RETURN'))
    for old in old_guard.GetFootprints():
        ref = old.GetReference()
        if ref=='J1':
            continue
        new_ref = ref_name(ref)
        fp = pcb.Cast_to_FOOTPRINT(old.Duplicate(False))
        fp.SetParent(board)
        fp.SetReference(new_ref)
        fp.SetPath(pcb.KIID_PATH(old.GetPath().AsString().replace(guard_uuid,mains_uuid)))
        x,y = GUARD_POS[ref]
        fp.SetPosition(point(ORIGIN[0]+GUARD_X+x,ORIGIN[1]+y))
        for pad in fp.Pads():
            if pad.GetNetname():
                pad.SetNet(net_for(board,guard_net(pad.GetNetname(),ref,new_ref)))
        board.Add(fp)
        footprints[new_ref] = fp

    for item in list(board.GetDrawings()):
        if item.GetLayer()==pcb.Edge_Cuts or (isinstance(item,pcb.PCB_TEXT) and item.GetText().startswith('E27 / REV')):
            board.Remove(item)
    x,y = ORIGIN
    w,h = SIZE
    outline = [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
    for a,c in zip(outline,outline[1:]):
        k.shape(board,pcb.Edge_Cuts,a,c)
    k.txt(board,'E27 / REV D',x+79,y+2.1,.88)
    for old_ref,(px,py) in GUARD_POS.items():
        if old_ref.startswith('TP'):
            k.txt(board,ref_name(old_ref),x+GUARD_X+px,y+py+1.8,.81)
    board.GetDesignSettings().SetAuxOrigin(point(x,y+h))
    route.NX,route.NY = [round(n/route.STEP)+1 for n in SIZE]
    route.FRONT_ESCAPE = {('U101','7'):1.3,('U103','14'):1.4,('U104','3'):-1.25}
    route.BOUNDARY = 30
    route.EARLY = ['DELAY','CLK','K1_F','K2_F','REF','PG','CLR_N','PERMIT',
                   'S1_RETURN','S_EN','S_LED_KA','S_LED_KB','S_RAW','LDO_IN','V3V3','S_RTN']
    anchors = {
        'S_EN': anchor('S_EN',cut,(1,)),
        'S_RAW': anchor('S_RAW',point(128.0,80.2),(0,1)),
        'S_RTN': anchor('S_RTN',point(136.3,83.6),(0,1)),
    }
    selected = {('J2','2'),('J3','2'),('J3','3')}
    added = {ref_name(ref) for ref in GUARD_POS}
    nets = {p.GetNetname()[1:]:p.GetNet() for ref in added for p in footprints[ref].Pads()
            if p.GetNetname().startswith('/')}
    # Old filled copper is regenerated by KiCad around the new traces.
    route.route_board(board,footprints,nets,controller_fanout=False,seed_routes=wire_obstacles(board),
                      term_filter=lambda ref,pin: ref in added or (ref,pin) in selected,anchors=anchors)
    assert pcb.SaveBoard(str(DEST/f'{NAME}.kicad_pcb'),board)


if __name__ == '__main__':
    copy_project()
    make_board(*make_schematic())

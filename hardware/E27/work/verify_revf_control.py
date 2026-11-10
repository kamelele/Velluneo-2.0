"""Check saved Rev F board pins against the reference and KiCad schematic netlist."""
from pathlib import Path
from xml.etree import ElementTree as ET
import argparse
import re

import pcbnew as pcb

from revf_control import BASE, NAME, circuit

DEST = Path('outputs')/NAME


def pins(board):
    return {(fp.GetReference(),p.GetNumber()):p.GetNetname() for fp in board.GetFootprints()
            for p in fp.Pads() if p.GetNetname()}


def main(netlist):
    base = pcb.LoadBoard(str(BASE/'Zasilacz_RevD_JLCPCB.kicad_pcb'))
    board = pcb.LoadBoard(str(DEST/f'{NAME}.kicad_pcb'))
    actual = pins(board)
    xml = ET.parse(netlist).getroot()
    schematic = {(node.get('ref'),node.get('pin')):net.get('name')
                 for net in xml.findall('./nets/net') for node in net.findall('node')}
    assert actual==schematic, (actual.items()-schematic.items(),schematic.items()-actual.items())
    expected = {(ref,str(n)):'/'+net for ref,p in circuit().items() for n,net in p.connection.items() if net}
    assert expected == {pin:net for pin,net in actual.items() if not net.startswith('unconnected-')}
    old = pins(base)
    refs = {'U2','U3','U4','C11','C12','C13','C14','C15','R14','R15','R16',
            'R17','R18','R19','R20','R21','J2','J3'}
    assert {k:v for k,v in old.items() if k[0] in refs} == {k:v for k,v in actual.items() if k[0] in refs}
    assert not any(n.startswith('/P_') for n in actual.values())
    assert actual['J102','1']=='/S_RAW' and actual['J102','2']=='/S_RTN'
    expected_switch = ['/S_RTN','/HOLD_B','/HOLD_B','/PG_RETURN','/RELEASE_B','/S_EN']
    assert [actual['Q101',str(n)] for n in range(1,7)] == expected_switch
    assert [actual['Q102',str(n)] for n in range(1,4)] == ['/PG','/S_RTN','/PG_RETURN']
    footprints = list(board.GetFootprints())
    assert len(footprints)==51 and sum(f.GetReference().startswith('TP') for f in footprints)==3
    edges = [x for x in board.GetDrawings() if x.GetLayer()==pcb.Edge_Cuts]
    points = {tuple(p) for s in edges for p in (s.GetStart(),s.GetEnd())}
    assert len(edges)==4 and points=={(pcb.FromMM(x),pcb.FromMM(y)) for x in (75,105) for y in (70,95)}
    assert board.GetCopperLayerCount()==4
    erc=(DEST/'ERC.rpt').read_text(encoding='utf8')
    drc=(DEST/'DRC.rpt').read_text(encoding='utf8')
    assert 'Errors 0  Warnings 0' in erc
    assert 'Found 0 Footprint errors' in drc
    errors=re.search(r'Found (\d+) DRC violations',drc)[1]
    unconnected=re.search(r'Found (\d+) unconnected pads',drc)[1]
    inner=[t for t in board.GetTracks() if not isinstance(t,pcb.PCB_VIA) and t.GetLayer()==pcb.In1_Cu]
    assert {t.GetNetname() for t in inner}=={'/S_RTN','/REF'}
    ref_len=sum(pcb.ToMM(t.GetLength()) for t in board.GetTracks()
                if not isinstance(t,pcb.PCB_VIA) and t.GetNetname()=='/REF')
    inner_ref=sum(pcb.ToMM(t.GetLength()) for t in inner if t.GetNetname()=='/REF')
    plane,=[z for z in board.Zones() if z.GetLayer()==pcb.In1_Cu]
    assert plane.GetNetname()=='/S_RTN' and plane.IsFilled() and plane.GetFilledPolysList(pcb.In1_Cu).OutlineCount()==1
    area=plane.GetFilledArea()/1e12
    assert ref_len<30 and inner_ref<12 and area>560
    assert errors=='0' and unconnected=='0'
    report=f"""# Kontrola Rev F

- KiCad ERC wykazał zero naruszeń. Porównano niezależnie {len(actual)} przypisań pin–sieć w schemacie i PCB. Potwierdzono przypisanie wyprowadzeń Q101/Q102 oraz zgodność obwodów eFuse, blokad i obu regulatorów prądu z Rev D.
- Obrys 30 × 25 mm, cztery warstwy, 48 części i trzy pola pomiarowe. Interfejs J102 ma wyłącznie S_RAW i S_RTN. Warstwa In1.Cu ma jedno połączone wypełnienie S_RTN o powierzchni {area:.1f} mm² i lokalne odcinki REF o łącznej długości {inner_ref:.1f} mm. Cała sieć REF na czterech warstwach ma {ref_len:.1f} mm ścieżek.
- Raport DRC z porównaniem schematu zawiera {errors} naruszeń reguł i {unconnected} niepołączonych padów. [Szczegóły](DRC.rpt)
- Model i kontrola plików stanowią weryfikację projektu. Próby fizyczne wymagają prototypu.
"""
    (DEST/'Weryfikacja_RevF.md').write_text(report,encoding='utf8')
    print(f'{len(actual)} pin-to-net entries, {errors} DRC violations, {unconnected} unrouted')


if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('netlist',type=Path)
    args=ap.parse_args()
    main(args.netlist)

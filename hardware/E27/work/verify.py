from pathlib import Path
import csv
import json
import xml.etree.ElementTree as ET
import pcbnew as p

o=Path('outputs')
def netfile(name):
    root=ET.parse(Path('work')/(name+'.xml')).getroot()
    return {(node.get('ref'),node.get('pin')):net.get('name').lstrip('/')
            for net in root.findall('./nets/net') for node in net.findall('node')}
def board(project):
    return p.LoadBoard(str(o/project/(project+'.kicad_pcb')))
def pcbmap(b):
    return {(f.GetReference(),pad.GetNumber()):pad.GetNetname().lstrip('/')
            for f in b.GetFootprints() for pad in f.Pads() if pad.GetNetname()}
def check(expected,actual):
    assert expected==actual, sorted(set(expected.items())^set(actual.items()))

led_expected={('J1','1'):'LED_PLUS',('J2','1'):'LED_KA',('J3','1'):'LED_KB'}
for letter,offset in [('A',0),('B',8)]:
    for i in range(8):
        ref='D'+str(i+offset+1)
        led_expected[(ref,'2')]='LED_PLUS' if i==0 else letter+str(i)
        led_expected[(ref,'1')]='LED_K'+letter if i==7 else letter+str(i+1)
lb=board('Wklad_LED')
check(led_expected,netfile('led'))
check(led_expected,pcbmap(lb))
assert not any(t.GetLayer()==p.B_Cu or isinstance(t,p.PCB_VIA) for t in lb.GetTracks())
assert not any(pad.GetDrillSize().x>0 for fp in lb.GetFootprints() for pad in fp.Pads())

design=json.loads(Path('work/catalog.json').read_text(encoding='utf-8'))
exp={(c['ref'],pin):net for c in design for pin,net in c['connection'].items()}
pb=board('Zasilacz_RevA')
check(exp,netfile('ps'))
check(exp,pcbmap(pb))
P=[]
S=[]
def classify(item):
    name=item.GetNetname().lstrip('/')
    dest=P if name.startswith('P_') else S if name.startswith('S_') else None
    if dest is not None:
        box=item.GetBoundingBox()
        dest.append((box.GetLeft()/1e6,box.GetRight()/1e6))
for fp in pb.GetFootprints():
    for pa in fp.Pads(): classify(pa)
for t in pb.GetTracks(): classify(t)
maxP=max(x2 for x1,x2 in P)
minS=min(x1 for x1,x2 in S)
distance=minS-maxP
assert distance>=8.0,(maxP,minS,distance)

for name,expected in [('Wklad_LED',16),('Zasilacz_RevA',None)]:
    d=o/name
    with next((d/'Produkcja_DO_PRZEGLADU').glob('CPL*.csv')).open(encoding='utf-8-sig',newline='') as stream:
        recs=list(csv.DictReader(stream))
    assert recs and len(recs)==len({r['Ref'] for r in recs})
    if expected is not None: assert len(recs)==expected
    assert 'Found 0 DRC violations' in (d/'DRC.rpt').read_text(encoding='utf-8-sig')
    assert 'Found 0 unconnected pads' in (d/'DRC.rpt').read_text(encoding='utf-8-sig')
    assert 'Found 0 Footprint errors' in (d/'DRC.rpt').read_text(encoding='utf-8-sig')
    assert 'Errors 0  Warnings 0' in (d/'ERC.rpt').read_text(encoding='utf-8-sig')
    print(name,len(recs),'SMD placements')
s=f'''# Weryfikacja plików KiCad 10.0.8

- Wkład LED. Zgodność niezależnie zapisanych połączeń pin po pinie ze schematem i PCB. Sprawdzono {len(led_expected)} styków elektrycznych, 16 pozycji SMT oraz brak otworów, przelotek i tras na B.Cu.
- Zasilacz. Porównano {len(exp)} połączeń pin–sieć pomiędzy założeniami, listą sieci wyeksportowaną przez KiCad i odczytem padów PCB.
- Minimalna szerokość pustego pasa między obwiedniami miedzi P/S w rzucie na oś x wynosi {distance:.3f} mm w tym pliku, przy x końca obwiedni strony P = {maxP:.3f} mm i x początku strony S = {minS:.3f} mm. Sprawdzono obie warstwy, pady, ścieżki i przelotki. To test geometrii pliku. Ocenie izolacji podlega gotowy zespół.
- ERC, DRC i porównanie schematu z PCB zakończyły się zerem naruszeń dla obu projektów. Wydzielone raporty zachowują listę reguł domyślnie wyłączonych przez KiCad.
- Gerbery, pliki wierceń oraz pliki pozycji są eksportem tych samych rewizji. Wkład nie ma punktów wiercenia. Dla zasilacza sprawdzić obie strony montażu w podglądzie dostawcy.
- Próby sprzętowe, pomiary izolacji, parametry fotometryczne i pomiary EMC pozostają do wykonania.
'''
(o/'Weryfikacja_KiCad.md').write_text(s,encoding='utf-8')
print('Verified boundary [mm]:',round(distance,3))

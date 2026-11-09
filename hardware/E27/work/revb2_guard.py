"""Build the secondary-side Rev B2 short-circuit test adapter in KiCad."""
from dataclasses import dataclass
import csv
import sys

import build as k
import power
import route

NAME = 'Zasilacz_RevB2_Ochrona'
SIZE = (50, 30)
ORIGIN = (75, 70)
R = 'Resistor_SMD:R_0603_1608Metric'
C = 'Capacitor_SMD:C_0603_1608Metric'
BACK = {'C3','C4','C5','C6','C7','C8','C9','C10','R4','R6','R8','R9','R10','D1','D3'}


@dataclass(frozen=True)
class Part:
    ref: str
    value: str
    fp: str
    kind: str
    pins: dict
    sch: tuple
    xy: tuple
    mpn: str = ''
    rotation: int = 0


def pair(ref, value, a, b, sch, xy, fp=None, mpn='', rotation=0):
    kind = ref[0]
    return Part(ref, value, fp or (R if kind == 'R' else C), kind, {1:a, 2:b}, sch, xy, mpn, rotation)


PIN_NAMES = {
    'LDO': ('OUT', 'DNC', 'PG', 'GND', 'EN', 'NC', 'DELAY', 'IN', 'EP'),
    'CMP': ('OUT1', 'IN1-', 'IN1+', 'GND', 'IN2+', 'IN2-', 'OUT2', 'VCC'),
    'FF': ('CLR1', 'D1', 'CLK1', 'PRE1', 'Q1', 'nQ1', 'GND',
           'nQ2', 'Q2', 'PRE2', 'CLK2', 'D2', 'CLR2', 'VCC'),
    'NAND': ('A', 'B', 'GND', 'Y', 'VCC'),
    'PHOTO': ('LED A', 'LED K', 'OUT 3', 'OUT 4'),
    'PORT': ('S_RAW', 'S_RTN', 'K1', 'K2', 'S1 return', 'SHDN out'),
    'TP': ('Pad',),
}
SIDES = {
    'LDO': ((8,5,4,9,7), (1,3,2,6)),
    'CMP': ((2,3,6,5,8,4), (1,7)),
    'FF': ((1,2,3,4,13,12,11,10), (5,6,9,8,14,7)),
    'NAND': ((1,2,5,3), (4,)),
    'PHOTO': ((1,2), (4,3)),
    'PORT': ((1,2,3,4,5,6), ()),
    'TP': ((1,), ()),
}

PARTS = [
    Part('J1','Wiazka prob 6p','Connector_JST:JST_XH_B6B-XH-A_1x06_P2.50mm_Vertical','PORT',
         {1:'S_RAW',2:'S_RTN',3:'S_K1',4:'S_K2',5:'S1_RETURN',6:'S_EN'},(34,44),(4,4),'B6B-XH-A(LF)(SN)'),
    Part('U1','TPS7A1633','E27:TPS7A16_DGN','LDO',
         {1:'V3V3',2:None,3:'PG',4:'S_RTN',5:'LDO_IN',6:None,7:'DELAY',8:'LDO_IN',9:'S_RTN'},
         (91,47),(8.5,13),'TPS7A1633DGNR'),
    Part('U2','TLV1702','Package_SO:MSOP-8_3x3mm_P0.65mm','CMP',
         {1:'CLR_N',2:'K1_F',3:'REF',4:'S_RTN',5:'REF',6:'K2_F',7:'CLR_N',8:'V3V3'},
         (220,47),(19.8,13.5),'TLV1702AIDGKR'),
    Part('U3','SN74HCS74','Package_SO:TSSOP-14_4.4x5mm_P0.65mm','FF',
         {1:'CLR_N',2:'V3V3',3:'CLK',4:'V3V3',5:'PERMIT',6:None,7:'S_RTN',8:None,9:None,
          10:'V3V3',11:'S_RTN',12:'S_RTN',13:'S_RTN',14:'V3V3'},(330,48),(29.9,14),'SN74HCS74PWR'),
    Part('U4','SN74LVC1G132','Package_TO_SOT_SMD:SOT-23-5','NAND',
         {1:'PG',2:'PERMIT',3:'S_RTN',4:'LED_SINK',5:'V3V3'},(330,132),(37.4,13.5),'SN74LVC1G132DBVR'),
    Part('U5','AQY212GS','E27:AQY212GS_SOP4','PHOTO',
         {1:'LED_A',2:'LED_SINK',3:'EN_SERIES',4:'S1_RETURN'},(330,167),(41.7,20.0),'AQY212GS'),
    pair('D1','BAT54WS','PG','CLR_N',(325,97),(28.3,22.8),'Diode_SMD:D_SOD-323','BAT54WS'),
    pair('D2','PMEG6010CEH','LDO_IN','S_RAW',(91,78),(4.2,9.1),'Diode_SMD:D_SOD-123F','PMEG6010CEH,115'),
    pair('D3','PMEG6010CEH','LDO_IN','V3V3',(91,91),(9.1,8.7),'Diode_SMD:D_SOD-123F','PMEG6010CEH,115'),
    pair('R1','22k','V3V3','PG',(105,112),(10.6,20.2)),
    pair('R2','2.2k','V3V3','S_RTN',(105,126),(12.5,23.4)),
    pair('R3','133k 0.1%','V3V3','REF',(163,48),(16.2,16.5),mpn='ERA-3AEB1333V'),
    pair('R4','22k 0.1%','REF','S_RTN',(163,61),(16.2,18.4),mpn='ERA-3AEB223V'),
    pair('R5','330k 0.1%','S_K1','K1_F',(163,87),(15.9,9.2),mpn='ERA-3AEB3303V'),
    pair('R6','22k 0.1%','K1_F','S_RTN',(163,100),(15.9,11.1),mpn='ERA-3AEB223V'),
    pair('R7','330k 0.1%','S_K2','K2_F',(227,87),(22.8,8.4),mpn='ERA-3AEB3303V'),
    pair('R8','22k 0.1%','K2_F','S_RTN',(227,100),(24.2,10.5),mpn='ERA-3AEB223V'),
    pair('R9','22k','V3V3','CLR_N',(325,84),(26.0,18.8)),
    pair('R10','100k','PG','CLK',(325,110),(24.6,21.6)),
    pair('R11','249R 1%','V3V3','LED_A',(376,153),(42.1,15.8)),
    pair('R12','100k 1%','EN_SERIES','S_EN',(376,167),(44.3,24.3)),
    pair('C1','2.2u / 100V','LDO_IN','S_RTN',(36,81),(4.1,17.4),'Capacitor_SMD:C_1210_3225Metric','C3225X7R2A225K230AB'),
    pair('C2','10u / 25V','V3V3','S_RTN',(36,94),(12.7,16.7),'Capacitor_SMD:C_0805_2012Metric','GRM21BC71E106KE11L'),
    pair('C3','10n','DELAY','S_RTN',(36,107),(8.5,17.2)),
    pair('C4','220n / 50V X7R 10%','K1_F','S_RTN',(163,113),(15.9,13.0)),
    pair('C5','220n / 50V X7R 10%','K2_F','S_RTN',(227,113),(25.0,12.8)),
    pair('C6','10n','REF','S_RTN',(163,74),(19.5,20.4)),
    pair('C7','100n','V3V3','S_RTN',(227,66),(21.2,17.4)),
    pair('C8','10n','CLK','S_RTN',(376,110),(24.8,24.1)),
    pair('C9','100n','V3V3','S_RTN',(376,84),(33.5,9.1)),
    pair('C10','100n','V3V3','S_RTN',(376,132),(37.5,9.7)),
]
for i,(net,x) in enumerate((('S_RTN',5.0),('V3V3',17.0),('PG',20.5),('CLR_N',29.0),('PERMIT',33.0),('S_EN',39.0)), 1):
    PARTS.append(Part('TP'+str(i),net,'TestPoint:TestPoint_Pad_D1.5mm','TP',
                      {1:net},(33+(i-1)*67,207),(x,26.0)))


def libraries(d):
    pads = ''.join(k.smd(n, -2.2 if n < 5 else 2.2, .65*((n-1) if n < 5 else (8-n))-.975, 1.4, .45)
                   for n in range(1,9))
    power.custom(d,'TPS7A16_DGN','DGN0008C land with 1.6 x 1.92 mm exposed pad',3,3,
                 pads+k.smd(9,0,0,1.6,1.92,True,-.15),model=(1.1,'0.14 0.14 0.15'))
    pads = ''.join(k.smd(n,x,y,1.2,.8) for n,x,y in
                   [(1,-3,-1.27),(2,-3,1.27),(3,3,1.27),(4,3,-1.27)])
    power.custom(d,'AQY212GS_SOP4','Panasonic pad centers 6.0 x 2.54 mm',4.4,4.3,pads,
                 k.fp_line(-2.3,-2.35,-1.1,-2.35,'F.SilkS'), (2.0,'0.13 0.14 0.16'))
    for name,width in [('TPS7A16_DGN',6.2),('AQY212GS_SOP4',7.7)]:
        import re
        file = d / 'E27.pretty' / (name+'.kicad_mod')
        text = file.read_text(encoding='utf-8')
        text = re.sub(r'\(fp_rect \(start [^\n]+?\(layer "F.CrtYd"\)\)',
                      k.fp_rect(-width/2,-2.45,width/2,2.45,'F.CrtYd',.05),text,count=1)
        k.save(file,text)


def symbol_for(part):
    kind = part.kind
    if kind in {'R','C','D'}:
        art, pins = power.two(kind)
        return art, pins, [(1,-3.81,0),(2,3.81,0)], 3.81
    left, right = SIDES[kind]
    half_width = 8.89 if kind == 'PORT' else 6.35
    height = 1.27*(max(len(left),len(right))+1)
    pins, ends = [], []
    for side, numbers in [(-1,left),(1,right)]:
        x = side*(half_width+2.54)
        for i,n in enumerate(numbers):
            y = 1.27*(len(numbers)-1-2*i)
            pins.append(k.pin(n,PIN_NAMES[kind][n-1],x,y,0 if side < 0 else 180))
            ends.append((n,x,y))
    return k.box(-half_width,height,half_width,-height,'background'), pins, ends, height+2.54


def make():
    d,b,sheet = k.begin(NAME,'Secondary only',.19,.4)
    libraries(d)
    nets = k.nets_for(b, (n for part in PARTS for n in part.pins.values() if n))
    definitions, contents, footprints = {}, [], {}
    for part in PARTS:
        sid = k.uid()
        lib_id = 'E27:Guard_'+part.kind
        x,y = (round(round(v/1.27)*1.27,3) for v in part.sch)
        art, pins, ends, spacing = symbol_for(part)
        definitions[lib_id] = k.symbol(lib_id,part.ref.rstrip('0123456789'),art,pins,part.kind not in {'R','C','D'})
        placed = k.placed(lib_id,part.ref,part.value,part.fp,x,y,sid,NAME,sheet,list(part.pins))
        placed = placed.replace(k.prop('Reference',part.ref,x,y-3.81),k.prop('Reference',part.ref,x,y-spacing))
        placed = placed.replace(k.prop('Value',part.value,x,y+3.81),k.prop('Value',part.value,x,y+spacing))
        if part.kind == 'TP':
            placed = placed.replace('(in_bom yes)', '(in_bom no)')
        contents.append(placed)
        for n,dx,dy in ends:
            net = part.pins[n]
            xx,yy = x+dx,y-dy
            if not net:
                contents.append(f'(no_connect (at {k.fmt(xx)} {k.fmt(yy)}) (uuid "{k.uid()}"))')
                continue
            end = xx+(-2.54 if dx < 0 else 2.54)
            contents.extend([k.wire(xx,yy,end,yy),k.label(net,end,yy,180 if dx < 0 else 0)])
        xx,yy = (a+b for a,b in zip(ORIGIN,part.xy))
        pin_nets = {str(n):nets[net] for n,net in part.pins.items() if net}
        for n,net in part.pins.items():
            if net is None:
                nc = k.p.NETINFO_ITEM(b, f'unconnected-({part.ref}-{PIN_NAMES[part.kind][n-1]}-Pad{n})')
                b.Add(nc)
                pin_nets[str(n)] = nc
        fp = k.footprint(b,d,part.fp,part.ref,part.value,xx,yy,part.rotation,sid,sheet,pin_nets)
        if part.ref in BACK:
            fp.Flip(fp.GetPosition(),k.p.FLIP_DIRECTION_LEFT_RIGHT)
        footprints[part.ref] = fp

    for title,x,y in [
        ('E27 REV B2 / MODUL PROB OCHRONY ZWARCIOWEJ / TYLKO STRONA WTORNA',18,18),
        ('01   WIAZKA I ZASILANIE 3V3',18,28), ('02   POMIAR K1 / K2',147,28),
        ('03   PAMIEC BLEDU I ODCIECIE SHDN',295,28), ('04   PUNKTY POMIAROWE',18,190),
        ('J1-5: powrot S1/TH1. J1-6: wejscie SHDN na J2-2 Rev B1.',18,155),
        ('Otwarty PhotoMOS pozostawia R18 w Rev B1 jako wymuszenie wylaczenia.',18,164),
        ('Cel 7.49 V na K1/K2 wzgledem S_RTN; filtr ok. 4.54 ms.',18,173),
    ]:
        contents.append(k.note(title,x,y))
    k.schematic(d,NAME,sheet,'Modul prob ochrony zwarciowej E27 Rev B2',list(definitions.values()),contents,'A3','B2')
    x,y = ORIGIN
    w,h = SIZE
    outline = [(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
    for a,c in zip(outline,outline[1:]):
        k.shape(b,k.p.Edge_Cuts,a,c)
    k.txt(b,'E27 B2 / TYLKO DC',x+35.9,y+3.0,.85)
    for part in PARTS:
        if part.kind == 'TP':
            k.txt(b,part.ref,x+part.xy[0],y+28.1,.83)
    if '--placement' not in sys.argv:
        route.ORIGIN = ORIGIN
        route.NX,route.NY = [round(v/route.STEP)+1 for v in SIZE]
        route.BOUNDARY = -4.25
        route.FRONT_ESCAPE = {('U4','3'):-1.6}
        route.EARLY = ['CLK','K1_F','K2_F','REF','PG','CLR_N','DELAY','PERMIT','S_RAW','LDO_IN','V3V3','S_RTN']
        route.route_board(b,footprints,nets,controller_fanout=False)
    assert k.p.SaveBoard(str(d/(NAME+'.kicad_pcb')),b)
    with (d/'BOM_RevB2.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(('Ref','Wartość','MPN','Footprint'))
        writer.writerows((p.ref,p.value,p.mpn,p.fp) for p in PARTS if p.kind != 'TP')


if __name__ == '__main__':
    make()

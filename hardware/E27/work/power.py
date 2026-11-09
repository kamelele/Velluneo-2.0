from build import *
from dataclasses import dataclass

PRIMARY='P_'
SIZE=(75,40)
ORIGIN=(75,70)
BOUNDARY=32
LYT='LYT6073C-TL'

def th(n,x,y,d=1.8,h=0.9):
    return f'(pad "{n}" thru_hole circle (at {x} {y}) (size {d} {d}) (drill {h}) (layers "*.Cu" "*.Mask"))'
def custom(d,name,desc,w,h,pads,silk='',model=None,attr='smd'):
    mods=''
    if model:
        save(d/(name+'.wrl'),'#VRML V2.0 utf8\n'+vrml_box(w,h,*model))
        mods=f'(model "${{KIPRJMOD}}/{name}.wrl" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))'
    body=fp_rect(-w/2,-h/2,w/2,h/2,'F.Fab')+fp_rect(-w/2-.25,-h/2-.25,w/2+.25,h/2+.25,'F.CrtYd',.05)
    save(d/f'E27.pretty/{name}.kicad_mod',fpdef(name,desc,pads,body,silk,mods,attr))

def declare_lib(d):
    leads=smd(24,5.65,-4.125,2.30,.45)
    for n in [13,14,15,16,17,18,19]:
        leads+=smd(n,5.12,4.125-(n-13)*.75,1.56,.40)
    for n in range(1,13):
        leads+=smd(n,-5.12,-4.125+(n-1)*.75,1.56,.40)
    custom(d,'InSOP_24D','LYTSwitch-6 17 leads; verify package / review land pattern',9.4,9.4,leads,
           fp_line(-4.25,-4.83,-3.5,-4.83,'F.SilkS'),(1.55,'0.12 0.12 0.13'))
    tpad=''.join(th(n,-6.5,y) for n,y in [(1,4.8),(2,-4.8),(3,-1.6),(4,1.6)])
    tpad+=''.join(th(n,6.5,y) for n,y in [(5,-4.8),(6,4.8)])
    custom(d,'EE16_6pins_RFQ','RFQ bobbin: 13 mm row spacing. Inner P joint. No pins 7/8.',
           16.6,15.6,tpad,model=(15.5,'0.20 0.19 0.17'),attr='through_hole')
    custom(d,'Mains_L_N','Insulated wire harness, pads 1=L 2=N, 7 mm spacing',4,10,
           th(1,0,-3.5,2.5,1.25)+th(2,0,3.5,2.5,1.25),attr='through_hole')
    custom(d,'Fuse_TE5','Radial fuse, 5.08 mm pitch; verify selected outline',8.5,4.3,
           th(1,-2.54,0,2,1)+th(2,2.54,0,2,1),model=(8.0,'0.15 0.16 0.16'),attr='through_hole')
    custom(d,'TMOV14','Thermally protected MOV, straight leads, 7.5 mm pitch',
           17.5,8.2,th(1,-3.75,0,2.1,1.2)+th(2,3.75,0,2.1,1.2),model=(15,'0.16 0.36 0.55'),attr='through_hole')
    custom(d,'CY1_10mm','Y1 safety capacitor only; 10 mm lead pitch',
           13,5.8,th(1,-5,0,1.8,1.05)+th(2,5,0,1.8,1.05),model=(11,'0.20 0.37 0.57'),attr='through_hole')
    custom(d,'E27_Al5812_MSOP','Diodes MSOP-8EP; pad 9 exposed ground',3,3,
           ''.join(smd(n,-2.0,-.975+.65*(n-1),1.35,.45) for n in range(1,5))+
           ''.join(smd(n,2.0,.975-.65*(n-5),1.35,.45) for n in range(5,9))+
           smd(9,0,0,1.7,2.0,True,-.22),fp_line(-2.9,-1.52,-1.45,-1.52,'F.SilkS'),(1.05,'0.11 0.12 0.12'))
    # TI PWP0016A pattern: 1.50 x 0.45; mask-defined exposed pad.
    custom(d,'PWP0016A','TI PWP0016A; land pattern page 53',4.4,5,
           ''.join(smd(n,-2.9,-2.275+.65*(n-1),1.50,.45) for n in range(1,9))+
           ''.join(smd(n,2.9,2.275-.65*(n-9),1.50,.45) for n in range(9,17))+
           smd(17,0,0,3.4,5,True,-.25),fp_line(-3.55,-2.83,-2.27,-2.83,'F.SilkS'),(1.2,'0.10 0.11 0.12'))
    # Add actual outline to courtyards for protruding leads.
    for n,w,h in [('InSOP_24D',14.0,9.9),('E27_Al5812_MSOP',5.85,3.6),('PWP0016A',7.8,5.6)]:
        file=d/f'E27.pretty/{n}.kicad_mod'
        st=file.read_text()
        st=__import__('re').sub(r'\(fp_rect \(start [^\n]+?\(layer "F.CrtYd"\)\)',fp_rect(-w/2,-h/2,w/2,h/2,'F.CrtYd',.05),st,count=1)
        save(file,st)
def two(kind):
    if kind=='R':
        return box(-1.5,.75,1.5,-.75),[pin(1,'1',-3.81,0,0,2.31),pin(2,'2',3.81,0,180,2.31)]
    if kind in ('C','CP'):
        g=poly([(-.65,-1.4),(-.65,1.4)],width=.32)+poly([(.65,-1.4),(.65,1.4)],width=.32)
        if kind=='CP': g+=poly([(-1.9,1.27),(-1.9,2.07)])+poly([(-2.3,1.67),(-1.5,1.67)])
        return g,[pin(1,'1',-3.81,0,0,3.16),pin(2,'2',3.81,0,180,3.16)]
    if kind in ('D','Z'):
        g=poly([(1.27,-1.27),(1.27,1.27),(-1.27,0),(1.27,-1.27)])+poly([(-1.27,1.27),(-1.27,-1.27)])
        if kind=='Z': g+=poly([(-1.9,1.55),(-1.27,1.27)])+poly([(-1.27,-1.27),(-.65,-1.55)])
        return g,[pin(1,'K',-3.81,0,0),pin(2,'A',3.81,0,180)]
    g=box(-1.27,.82,1.27,-.82)
    if kind=='F': g+=poly([(-1.27,0),(1.27,0)])
    if kind=='L': g=poly([(-1.27,0),(-.85,.8),(-.42,0),(0,.8),(.42,0),(.85,.8),(1.27,0)])
    if kind=='MOV': g+=poly([(-1.8,-1.3),(1.2,1.3)])
    return g,[pin(1,'1',-3.81,0,0),pin(2,'2',3.81,0,180)]

@dataclass
class Device:
    ref: str
    val: str
    footprint: str
    connection: dict
    xy: tuple
    schematic: tuple
    kind: str
    rot: int = 0
    part: str = ''
    maker: str = ''
    function: str = ''
    notes: str = ''

RF='Resistor_SMD:R_'
CF='Capacitor_SMD:C_'
R60=RF+'0603_1608Metric'
R80=RF+'0805_2012Metric'
R12=RF+'1206_3216Metric'
R20=RF+'2010_5025Metric'
C60=CF+'0603_1608Metric'
C80=CF+'0805_2012Metric'
C12=CF+'1206_3216Metric'
SMA='Diode_SMD:D_SMA'
SMB='Diode_SMD:D_SMB'
SOD='Diode_SMD:D_SOD-123'
JST3='Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical'
JST4='Connector_JST:JST_XH_B4B-XH-A_1x04_P2.50mm_Vertical'
def catalog():
    a=[]
    def add(ref,val,fp,pins,xy,sch,kind,rot=0,part='',maker='',function='',notes=''):
        if isinstance(pins,str): pins=dict(enumerate(pins.split(),1))
        a.append(Device(ref,val,fp,pins,xy,sch,kind,rot,part,maker,function,notes))
    add('J1','230 VAC','E27:Mains_L_N','P_L P_N',(3.0,7.0),(29.21,48.26),'AC',part='',function='Przewody L i N z E27',notes='Stałe lutowanie i odciążenie przewodów.')
    add('F1','T 1 A / 300 VAC','E27:Fuse_TE5','P_L P_LF',(8.6,3),(64.77,48.26),'F',part='36911000000',maker='Littelfuse',function='Bezpiecznik zwłoczny',notes='Sprawdź zdolność wyłączania, I²t, charakterystykę przeciążenia i koordynację z MOV.')
    add('RV1','275 VAC','E27:TMOV14','P_LF P_N',(10.6,9.7),(102.87,48.26),'MOV',part='TMOV14RP275E',maker='Littelfuse',function='Ogranicznik przepięć z odcięciem termicznym')
    add('R1','22R pulse','Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P10.16mm_Horizontal','P_LF P_LR',(3.25,15.15),(139.7,48.26),'R',part='',function='Ograniczenie prądu udarowego',notes='RFQ 22 Ω 1 W, odporny na impuls, flameproof. Dopasować do obudowy, potwierdzić I²t.')
    for i,(n,xy,sch) in enumerate([
      ('P_BR P_LR',(5.0,20.5),(38.1,68.58)),('P_BR P_N',(12,20.5),(76.2,68.58)),
      ('P_LR P_0',(5.0,25),(38.1,81.28)),('P_N P_0',(12,25),(76.2,81.28))],1):
        add('D'+str(i),'US1M',SMA,n,xy,sch,'D',part='US1M-13-F',maker='Diodes Inc.',function='Prostownik mostkowy 1 kV',notes='Sprawdzić IFSM i orientację.')
    add('C1','100n / 630V',CF+'1210_3225Metric','P_BR P_0',(8.8,30.2),(111.76,68.58),'C',part='C3225X7T2J104KT000N',maker='TDK',function='Bocznik HF za mostkiem',notes='X7T, sprawdzić pojemność pod napięciem DC.')
    add('L1','1mH','Inductor_SMD:L_Bourns-SRR1005','P_BR P_BULK',(19,27.9),(147.32,68.58),'L',part='SRR1005-102K',maker='Bourns',function='Dławik filtra różnicowego',notes='Sprawdzić Isat, temperaturę oraz izolację węzła DC.')
    add('C2','15u / 450V','Capacitor_THT:CP_Radial_D10.0mm_P5.00mm','P_BULK P_0',(17.6,12.5),(111.76,81.28),'CP',90,part='450BXF15M10X20',maker='Rubycon',function='Magazyn energii na szynie HV')
    add('R2','510k HV',R20,'P_BULK P_BLEED',(20.8,4.2),(39.37,99.06),'R',part='',function='Rozładowanie szyny HV',notes='Dwa rezystory szeregowe, potwierdzić napięcie pracy, dobrać tolerancję i udar.')
    add('R3','510k HV',R20,'P_BLEED P_0',(20.8,7.9),(76.2,99.06),'R',part='',function='Rozładowanie szyny HV')
    add('T1','EE16 84:23:13','E27:EE16_6pins_RFQ',{1:'P_D',2:'P_BULK',3:'P_AUX',4:'P_0',5:'S_RAW',6:'S_SW'},(BOUNDARY,9.6),(205.74,59.69),'T',part='',function='Transformator flyback 1.2 mH ±8%',notes='RFQ. Potwierdzić karkas, pinout, TIW, odstępy i badania. Zwroty w raporcie.')
    add('C3','1.5n / 200V',C80,'P_CL P_BULK',(24.1,20.2),(176.53,83.82),'C',90,part='08052C152KAT2A',maker='KYOCERA AVX',function='Kondensator ogranicznika RCD')
    add('R4','1M',R12,'P_CL P_BULK',(21.6,20.2),(213.36,83.82),'R',90,part='ERJ-8GEYJ105V',maker='Panasonic',function='Rezystor ogranicznika RCD')
    add('D5','US1J',SMA,'P_CL P_D',(25.25,16.75),(250.19,83.82),'D',part='US1J-13-F',maker='Diodes Inc.',function='Dioda ogranicznika RCD',notes='Potwierdzić impulsy, temperaturę i rzeczywiste VDS.')
    add('D6','DFLU1200', 'Diode_SMD:D_PowerDI-123','P_BIAS P_AUX',(24.8,6.35),(176.53,99.06),'D',90,'DFLU1200-7','Diodes Inc.','Prostownik uzwojenia pomocniczego')
    add('C4','22u / 35V',C12,'P_BIAS P_0',(24.55,2.55),(213.36,99.06),'C',part='C3216X5R1V226M160AC',maker='TDK',function='Zasobnik zasilania BPP')
    add('R5','10k',R80,'P_BIAS P_BPP',(23.3,30.9),(250.19,99.06),'R',part='ERJ-6ENF1002V',maker='Panasonic',function='Ograniczenie prądu zasilania BPP')
    add('R6','2.2M HV',R20,'P_BULK P_VMID',(16.8,17.1),(176.53,114.3),'R',part='',function='Pomiar napięcia szyny V')
    add('R7','2.2M HV',R20,'P_VMID P_V',(16.8,20.7),(213.36,114.3),'R',part='',function='Pomiar napięcia szyny V')
    add('C5','470n / 50V',C80,'P_BPP P_0',(24.2,27.85),(250.19,114.3),'C',90,'GRM21BR71H474KA88L','Murata','Odprzęganie BPP')
    lyt={1:'S_RTN',2:'S_GND',3:'S_FB',4:'S_BPS',5:'S_GND',6:'S_VO',7:'S_FWD',13:'P_V',14:'P_BPP',
         16:'P_0',17:'P_0',18:'P_0',19:'P_0',24:'P_D'}
    add('U1',LYT,'E27:InSOP_24D',lyt,(BOUNDARY,25.6),(201.93,143.51),'LYT',part=LYT,maker='Power Integrations',function='Flyback CV/CC, FluxLink, MOSFET 725 V')
    add('CY1','2.2n Y1','E27:CY1_10mm','P_BULK S_RAW',(BOUNDARY,18.15),(260.35,141),'C',part='440LD22-R',maker='Vishay',function='Tłumienie zakłóceń wspólnych',notes='Y1, rozstaw 10 mm, sprawdzić obudowę, dostępność i prąd dotykowy. Można pominąć podczas pierwszej serii pomiarów.')
    add('D7','SK3200B',SMB,'S_SW S_GND',(42.3,15.9),(288.29,48.26),'D',90,'SK3200B-LTP','MCC','Prostownik po stronie niskiej 200 V')
    add('C6','470u / 50V','Capacitor_THT:CP_Radial_D12.5mm_P5.00mm','S_RAW S_GND',(46.3,7.8),(328.93,48.26),'CP',part='EEU-FR1H471',maker='Panasonic',function='Kondensator wyjściowy')
    add('R8','47R',R80,'S_SW S_FWD',(40.6,26.85),(369.57,48.26),'R',90,'ERJ-6GEYJ470V','Panasonic','Pomiar sygnału FWD')
    add('C7','68p / 200V',C60,'S_FWD S_GND',(40.6,29.8),(288.29,60.96),'C',part='C0603C680J2GACTU',maker='KEMET',function='Filtr FWD')
    add('R9','0.11R',R80,'S_RTN S_GND',(40.4,21.3),(328.93,60.96),'R',90,'RL0805FR-070R11L','Yageo','Limit sumy prądów ~318 mA')
    add('D8','US1B',SMA,'S_GND S_RTN',(44.9,20.8),(369.57,60.96),'D',part='US1B-13-F',maker='Diodes Inc.',function='Ochrona wejścia IS',notes='Potwierdzić polaryzację z referencją oraz amplitudę impulsów na IS.')
    add('R10','110k 1%',R60,'S_RAW S_FB',(43.3,23.55),(288.29,73.66),'R',part='ERJ-3EKF1103V',maker='Panasonic',function='Górna gałąź CV')
    add('R11','5.62k 1%',R60,'S_FB S_GND',(43.3,25.65),(328.93,73.66),'R',part='ERJ-3EKF5621V',maker='Panasonic',function='Dolna gałąź CV')
    add('C8','330p',C60,'S_FB S_GND',(43.3,27.75),(369.57,73.66),'C',part='CC0603KRX7R9BB331',maker='Yageo',function='Odprzęganie FB')
    add('C9','2.2u / 25V',C12,'S_BPS S_GND',(43.9,30.25),(288.29,86.36),'C',part='TMK316B7225KL-T',maker='Taiyo Yuden',function='Odprzęganie BPS')
    add('R12','2.2k',R80,'S_RAW S_Z18',(50.4,21.2),(328.93,86.36),'R',part='ERJ-6ENF2201V',maker='Panasonic',function='Prąd polaryzacji zenera VO')
    add('ZD1','18V',SOD,'S_Z18 S_GND',(54.2,23.5),(369.57,86.36),'Z',90,'BZT52C18-7-F','Diodes Inc.','Ograniczenie zasilania pinu VO')
    add('Q1','MMBT5551','Package_TO_SOT_SMD:SOT-23',{1:'S_Z18',2:'S_VO',3:'S_RAW'},(50.9,25.1),(288.29,101.6),'Q',part='MMBT5551LT1G',maker='onsemi',function='Wtórnik zasilający pin VO')
    add('C10','100n / 50V',C80,'S_VO S_GND',(47.5,25.65),(328.93,101.6),'C',90,'GRM21BR71H104KA01L','Murata','Odprzęganie VO')
    add('ZD2','27V',SOD,'S_RAW S_OVA',(52.6,29.4),(369.57,101.6),'Z',part='BZT52C27-7-F',maker='Diodes Inc.',function='Wtórne wykrywanie przepięcia')
    add('R13','100R',R80,'S_OVA S_OVB',(50.0,31.1),(328.93,116.84),'R',part='ERJ-6ENF1000V',maker='Panasonic',function='Ograniczenie prądu wstrzykiwanego do BPS')
    add('D9','BAV21W',SOD,'S_BPS S_OVB',(46.4,31.05),(369.57,116.84),'D',part='BAV21W-7-F',maker='Diodes Inc.',function='Odcięcie BPS przy zaniku VRAW')
    ef={1:'S_RAW',2:'S_RAW',3:'S_RTN',5:'S_OVP',7:'S_EN',8:'S_RTN',9:'S_RTN',11:'S_ILIM',12:'S_SLEW',15:'S_FUSED',16:'S_FUSED',17:'S_RTN'}
    add('U2','TPS26600PWPR','E27:PWP0016A',ef,(57.8,11.7),(82.55,192.405),'EF',part='TPS26600PWPR',maker='Texas Instruments',function='Niezależne OVP, soft-start, odcięcie zwarcia',notes='MODE otwarty, wyłącznik nadprądowy z auto-retry.')
    add('C11','100n / 50V',C80,'S_RAW S_RTN',(53.15,8.0),(143.51,172.72),'C',90,'GRM21BR71H104KA01L','Murata','Kondensator wejścia eFuse')
    add('R14','232k 1%',R60,'S_RAW S_OVP',(53.15,12.6),(143.51,186.69),'R',90,part='ERJ-3EKF2323V',maker='Panasonic',function='Górna gałąź OVP')
    add('R15','10k 1%',R60,'S_OVP S_RTN',(53.15,15.0),(143.51,200.66),'R',part='ERJ-3EKF1002V',maker='Panasonic',function='Dolna gałąź OVP, ~28.8 V typ.')
    add('R16','30.1k 1%',R60,'S_ILIM S_RTN',(62.45,13.35),(143.51,214.63),'R',part='ERJ-3EKF3012V',maker='Panasonic',function='Wyłącznik nadprądowy ok. 0.37 A typ.')
    add('C12','47n',C60,'S_SLEW S_RTN',(62.45,10.9),(143.51,228.6),'C',part='CC0603KRX7R9BB473',maker='Yageo',function='Rampa wyjścia ~10 ms')
    add('R17','10k',R60,'S_RAW S_ENFEED',(53.2,18.0),(181.61,172.72),'R',part='ERJ-3EKF1002V',maker='Panasonic',function='Zasilanie pętli S1 i termostatu')
    add('R18','10k',R60,'S_EN S_RTN',(55.8,17.5),(181.61,186.69),'R',part='ERJ-3EKF1002V',maker='Panasonic',function='Domyślne wyłączenie SHDN')
    add('R19','10k',R80,'S_LED_PLUS S_RTN',(65.45,23.0),(181.61,200.66),'R',part='ERJ-6ENF1002V',maker='Panasonic',function='Rozładowanie dostępnej anody')
    add('C13','100n / 50V',C80,'S_FUSED S_RTN',(62.65,7.55),(181.61,214.63),'C',part='GRM21BR71H104KA01L',maker='Murata',function='Odprzęganie wyjścia eFuse')
    add('J2','S1+TH / S2',JST4,'S_ENFEED S_EN S_FUSED S_LED_PLUS',(62.1,3.0),(234.95,184.15),'J4',part='B4B-XH-A(LF)(SN)',maker='JST',function='Wiązka dwóch blokad i termostatu')
    add('J3','A+ / KA / KB',JST3,'S_LED_PLUS S_LED_KA S_LED_KB',(65.45,30.0),(234.95,211.455),'J3',part='B3B-XH-A(LF)(SN)',maker='JST',function='Wiązka do trzech sprężynujących styków')
    for i,(led_k,rs,x) in enumerate([('S_LED_KA','S_SET_A',60.7),('S_LED_KB','S_SET_B',70.2)]):
        n=i+3
        sx=304.8+66.04*i
        add('U'+str(n),'AL5812MP-13','E27:E27_Al5812_MSOP',{1:'S_LED_PLUS',4:rs,5:'S_RTN',8:led_k,9:'S_RTN'},(x,25.3),(sx,182.88),'AL',part='AL5812MP-13',maker='Diodes Inc.',function='Niezależny prąd szeregu LED')
        add('R'+str(i+20),'5.90k 1%',R60,rs+' S_RTN',(x-3.55,27.6),(sx,205.74),'R',90,part='ERJ-3EKF5901V',maker='Panasonic',function='Prąd typ. 127 mA')
        add('C'+str(i+14),'100n / 50V',C80,'S_LED_PLUS S_RTN',(x-3.7,22.9),(sx,219.71),'C',90,part='GRM21BR71H104KA01L',maker='Murata',function='Odprzęganie lokalnego źródła prądu')
    return a

RULES='''(version 1)
(rule "Primary to secondary — engineering target"
    (constraint clearance (min 8.0mm))
    (constraint creepage (min 8.0mm))
    (condition "(A.NetName =~ '/P_*' && B.NetName =~ '/S_*') || (A.NetName =~ '/S_*' && B.NetName =~ '/P_*')"))
(rule "Mains lines separated"
    (constraint clearance (min 1.5mm))
    (condition "(A.NetName == '/P_N' && B.NetName =~ '/P_L*') || (A.NetName =~ '/P_L*' && B.NetName == '/P_N')"))
(rule "HV nodes to primary return"
    (constraint clearance (min 1.1mm))
    (condition "(A.NetName == '/P_0' && (B.NetName == '/P_D' || B.NetName == '/P_BULK' || B.NetName == '/P_BR' || B.NetName == '/P_CL')) || (B.NetName == '/P_0' && (A.NetName == '/P_D' || A.NetName == '/P_BULK' || A.NetName == '/P_BR' || A.NetName == '/P_CL'))"))
'''
def complex_pins(kind):
    if kind=='LYT':
        left=[(13,'V'),(14,'BPP'),(16,'S'),(17,'S'),(18,'S'),(19,'S'),(24,'D')]
        right=[(1,'IS'),(2,'GND'),(3,'FB'),(4,'BPS'),(5,'SR'),(6,'VO'),(7,'FWD')]
    elif kind=='EF':
        left=[(1,'IN'),(2,'IN'),(3,'UVLO'),(5,'OVP'),(7,'SHDN'),(8,'RTN'),(9,'GND'),(17,'EP')]
        right=[(16,'OUT'),(15,'OUT'),(11,'ILIM'),(12,'dVdT')]
    elif kind=='AL':
        left=[(1,'VCC'),(4,'RSET'),(5,'GND'),(9,'EP')]
        right=[(8,'LED')]
    elif kind=='T':
        left=[(2,'P dot'),(1,'P'),(4,'B dot'),(3,'B')]
        right=[(6,'S dot'),(5,'S')]
    elif kind=='Q':
        left=[(1,'B')]
        right=[(3,'C'),(2,'E')]
    elif kind=='BR':
        left=[(3,'AC1'),(4,'AC2')]
        right=[(1,'+'),(2,'-')]
    else:
        labels={'AC':['L','N'],'J3':['A+','KA','KB'],'J4':['S1 feed','SHDN','eFuse out','LED A+']}[kind]
        left=list(enumerate(labels,1))
        right=[]
    half=10.16 if kind in ('LYT','EF') else 7.62 if kind=='J4' else 5.08
    h=max(len(left),len(right))*1.27+1.27
    pins=[]
    for side, group in [(-1,left),(1,right)]:
        for i,(n,nm) in enumerate(group):
            pins.append((n,nm,side*(half+2.54),round((len(group)-1)*1.27-i*2.54,3),0 if side==-1 else 180))
    return half,h,pins

def pwr(name='Zasilacz_RevA', data=None, layout=None, more_footprints=None):
    rev=name[-1]
    d,b,sheet=begin(name,'Power',.19,.55,RULES)
    declare_lib(d)
    if more_footprints:
        more_footprints(d)
    data=catalog() if data is None else data
    aliases=set(n for c in data for n in c.connection.values())
    nt=nets_for(b,aliases)
    fx={}
    defs={}
    items=[note(f'E27 / FLYBACK 26 V + DWA KANALY 127 mA / Rev {rev}',19.05,23.495,2.5),
       note('PROTOTYP LABORATORYJNY. PRZED URUCHOMIENIEM SPRAWDZIC IZOLACJE, T1, OVP I PRZEPIECIA.',19.05,30.48,1.35),
       note('01   WEJSCIE, PROSTOWNIK I FILTR',19.05,39.37,1.55),
       note('02   FLYBACK I BARIERA IZOLACJI',168.91,39.37,1.55),
       note('03   PROSTOWANIE, CV, CC I OVP',279.4,39.37,1.55),
       note('04   ODCIECIE I LAGODNY START',19.05,159.0,1.55),
       note('05   BLOKADA I REGULACJA PRADU',218.44,159.0,1.55),
       note('J2-1 — S1 NO — termostat NC — J2-2',216,232),
       note('J2-3 — S2 NO — J2-4. S2 zamyka sie przed S1.',216,237.5),
       note('J3 do glowicy: A+ / K1 / K2. Wyjscie plywajace.',216,243)]
    positions={
        'F1':(10.2,3),'RV1':(14.3,10.1),'R1':(3.3,17.2),
        'D1':(4.3,22),'D2':(11.7,22),'D3':(4.3,27),'D4':(11.7,27),'C1':(9,32),'L1':(18.3,34.8),
        'C2':(20.7,25.4),'R2':(10.7,37.7),'R3':(3.6,37.7),'T1':(32,8.8),
        'D5':(21.0,13.7),'C3':(23.3,17.8),'R4':(17.5,19.15),'D6':(21,3.0),'C4':(17,3.2),
        'R5':(23.5,32.7),'R6':(16.9,27.7),'R7':(16.9,31.2),'C5':(23.5,28.0),'U1':(32,23.5),'CY1':(32,33.6),
        'D7':(44.6,18.2),'C6':(50.75,6.9),'R8':(40.8,24.1),'C7':(43.8,24.1),
        'R9':(41.2,19.8),'D8':(46.9,20.2),'R10':(41.4,27.1),'R11':(41.4,29.5),'C8':(41.4,31.9),
        'C9':(45.2,33.7),'R12':(50.4,24.2),'ZD1':(54.2,24.5),'Q1':(49.7,28.1),'C10':(49.1,31),
        'ZD2':(53.3,33.8),'R13':(50,36),'D9':(45.6,36.7),
        'U2':(60.0,12),'C11':(56,5.8),'R14':(54.4,12.5),'R15':(54.4,15.3),
        'R16':(65.4,14.0),'C12':(65.4,11.3),'R17':(54.0,18.7),'R18':(57.6,18.7),
        'R19':(65.45,23.0),'C13':(68,8.3),'J2':(63.0,3.35),'J3':(65.45,35.5),
        'U3':(60.7,28.3),'U4':(70.2,28.3),'R20':(57.15,32.15),'R21':(66.65,31.35),
        'C14':(56.7,24.4),'C15':(69.4,24.5)}
    backside={'R2','R3','D5','C3','R4','R5','R6','R7','C5','U1','R8','C7','R9','D8','R10','R11','C8','C9','C10','R21'}
    rotations={'C6':180}
    if layout:
        positions,backside,rotations=layout
    for c in data:
        sid=uid()
        id2=f'E27:{c.kind}'
        x,y=[round(round(v/1.27)*1.27,3) for v in c.schematic]
        if c.kind in ('EF','AL','T','LYT','J4','J3','AC','Q','BR'):
            half,h,pp=complex_pins(c.kind)
            if any(round((y-dy)/1.27,4)%1 for n,nm,dx,dy,ori in pp):
                raise RuntimeError(c.ref)
        ends=[]
        if c.kind in ('C','CP','D','Z','R','L','F','MOV'):
            g,pins=two(c.kind)
            ends=[(1,-3.81,0),(2,3.81,0)]
            defn=symbol(id2,c.ref.rstrip('0123456789'),g,pins)
        else:
            half,h,pin_data=complex_pins(c.kind)
            g=box(-half,h,half,-h,'background')
            if c.kind=='LYT': g+=poly([(0,-h),(0,h)])
            ends=[(n,xx,yy) for n,nm,xx,yy,ori in pin_data]
            defn=symbol(id2,c.ref.rstrip('0123456789'),g,[pin(n,nm,xx,yy,ori) for n,nm,xx,yy,ori in pin_data],True)
        defs[id2]=defn
        ins=placed(id2,c.ref,c.val,c.footprint,x,y,sid,name,sheet,list(c.connection))
        if c.kind not in ('C','CP','D','Z','R','L','F','MOV'):
            ins=ins.replace(prop('Reference',c.ref,x,y-3.81),prop('Reference',c.ref,x,y-h-3))
            ins=ins.replace(prop('Value',c.val,x,y+3.81),prop('Value',c.val,x,y+h+2.2))
        items.append(ins)
        for n,dx,dy in ends:
            net=c.connection[n]
            xx=x+dx
            yy=y-dy
            x2=xx+(2.54 if dx>0 else -2.54)
            items.extend([wire(xx,yy,x2,yy),label(net,x2,yy,0 if dx>0 else 180)])
        xx,yy=(a0+b0 for a0,b0 in zip(positions.get(c.ref,c.xy),ORIGIN))
        fp=footprint(b,d,c.footprint,c.ref,c.val,xx,yy,rotations.get(c.ref,c.rot),sid,sheet,{str(n):nt[v] for n,v in c.connection.items()})
        if c.ref in backside:
            fp.Flip(fp.GetPosition(),p.FLIP_DIRECTION_LEFT_RIGHT)
        fx[c.ref]=fp
    x,y=ORIGIN
    w,h=SIZE
    edge=[(x,y),(x+w,y),(x+w,y+h),(x,y+h),(x,y)]
    for e,f in zip(edge,edge[1:]): shape(b,p.Edge_Cuts,e,f)
    if rev=='A':
        txt(b,'230 VAC',x+5.8,y+14.4,1)
        txt(b,'ZASILACZ REV A',x+68,y+18.6,1)
    else:
        txt(b,'E27 / REV B',x+w-8.2,y+h-1.35,.85)
    txt(b,'PRZEGLAD PRZED URUCHOMIENIEM',x+BOUNDARY,y+h-1.4,1,p.Cmts_User)
    # Mark the barrier on drawings, keeping all routed copper on its own side.
    shape(b,p.Dwgs_User,(x+BOUNDARY,y),(x+BOUNDARY,y+h))
    schematic(d,name,sheet,f'Zasilacz E27 / rewizja {rev} laboratoryjna',list(defs.values()),items,'A3',rev)
    return d,b,data,fx,nt

if __name__=='__main__':
    d,b,data,fx,nt=pwr()
    p.SaveBoard(str(d/'Zasilacz_RevA.kicad_pcb'),b)
    save(ROOT/'work'/'catalog.json',json.dumps([vars(c) for c in data],ensure_ascii=False,indent=2))

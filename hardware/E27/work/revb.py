from dataclasses import replace
import power as a

a.SIZE=(66,34)
a.BOUNDARY=30
import route
route.MAINS_WIDTH=.65
route.MAINS_ACROSS=True
route.EARLY=['P_D','P_CL','P_V','S_EN','S_OVP','S_FWD','S_SW','S_GND','S_BPS','S_Z18','S_VO','S_RAW','S_RTN']
route.FRONT_ESCAPE={('BR1','3'):2.2,('BR1','4'):2.2}
a.RULES+='''(rule "Functional spacing across fuse and input resistor"
 (constraint clearance (min 1.5mm))
 (condition "A.NetName != B.NetName && A.NetName =~ '/P_L*' && B.NetName =~ '/P_L*'"))
'''

NAME='Zasilacz_RevB'

def libraries(d):
    a.custom(d,'Schurter_UMT_H','UMT-H 16 mm ceramic; compare land pattern with vendor ECAD before assembly',
             18.4,5.9,a.smd(1,-6.875,0,3.75,5.6)+a.smd(2,6.875,0,3.75,5.6),
             model=(5.35,'0.86 0.83 0.71'))
    a.custom(d,'AC01_CS_WSZ','Vishay AC01-CS WSZ Z-form. Review exact lead bend and vendor pattern.',
             18.3,5.5,a.smd(1,-7.1,0,4.0,4.0)+a.smd(2,7.1,0,4.0,4.0),
             model=(5,'0.31 0.47 0.44'))
    a.custom(d,'UCM_12p5','Nichicon UCM 50 V 470 uF; 13.6 mm base envelope',
             13.6,13.6,a.smd(1,-4.15,0,4.0,2.9)+a.smd(2,4.15,0,4.0,2.9),
             a.fp_line(-5.6,-6.89,-3.9,-6.89,'F.SilkS'),(13.5,'0.09 0.17 0.24'))
    a.custom(d,'Wurth_TI_HV_8','WE-TI HV 768772102, raster 5 mm / hole 1.2 mm',
             8.35,8.35,a.th(1,-2.5,0,2.1,1.2)+a.th(2,2.5,0,2.1,1.2),
             model=(10,'0.26 0.21 0.20'),attr='through_hole')
    for count in (3,4):
        h=2.54*(count-1)+2.6
        pads=''.join(a.th(i+1,0,round(2.54*(i-(count-1)/2),3),1.83,.95) for i in range(count))
        a.custom(d,f'Harness_{count}pos','Insulated keyed harness, separate mechanical strain relief',
                 3.2,h,pads,attr='through_hole')

def circuit():
    parts={c.ref:c for c in a.catalog()}
    def ch(ref,**kw):
        parts[ref]=replace(parts[ref],**kw)
    ch('F1',val='T 500 mA / 277 VAC',footprint='E27:Schurter_UMT_H',part='3403.0271.23',maker='Schurter',
       notes='UMT-H. 1,5 kA przy 277 VAC UL albo przy 250 VAC IEC, warunki z karty. Wymaga testu zdolności wyłączania całego zespołu.')
    ch('R1',val='22R / 1.1W fusible',footprint='E27:AC01_CS_WSZ',part='AC01000902209JBMCS',maker='Vishay',
       notes='AC01-CS WSZ. Potwierdzić obrys, impuls rozruchowy, temperaturę i koordynację z F1.')
    ch('RV1',connection={1:'P_LR',2:'P_N'},notes='Umieszczony za R1. Sprawdzić surge, ciągłe przepięcie i rozłączenie termiczne.')
    for ref in ('D1','D2','D3','D4'):
        del parts[ref]
    parts['BR1']=a.Device('BR1','MB10S','Package_SO:OnSemi_751EP_SOIC-4_3.9x4.725mm_P2.54mm',
                          {1:'P_BR',2:'P_0',3:'P_LR',4:'P_N'},(10,30),(70.485,73.66),'BR',
                          part='MB10S',maker='onsemi',function='Mostek 0,5 A / 1 kV',notes='Porównać znaki na obudowie i wynik testu diod przed montażem.')
    ch('C2',val='10u / 450V',part='450BXW10MEFR10X16',notes='Ø10 mm × 16 mm nominalnie. 18 mm maks. nad PCB, raster 5 mm. 10 000 h przy 105°C.')
    ch('L1',footprint='E27:Wurth_TI_HV_8',part='768772102',maker='Würth Elektronik',
       notes='1 mH, 0,5 A, Isat 0,55 A typ. Brak ekranu. Sprawdzić EMI, udar i rozgrzanie w rzeczywistym układzie.')
    ch('C6',footprint='E27:UCM_12p5',part='UCM1H471MNJ1MS',maker='Nichicon',
       notes='470 µF/50 V, Ø12,5 × 13,5 mm nominalnie. 5 000 h przy 105°C. Zweryfikować lutowanie reflow i nagrzewanie.')
    ch('J2',footprint='E27:Harness_4pos',part='',maker='',notes='Przewody do S1/TH1 i S2 lutowane, odciążone w korpusie. Złącze serwisowe poza PCB.')
    ch('J3',footprint='E27:Harness_3pos',part='',maker='',notes='Przewody A+/K1/K2 lutowane, odciążone w korpusie. Złącze serwisowe poza PCB.')
    ch('R10',val='110k 0.1%',part='ERA-3AEB114V',notes='Dzielnik CV, ±25 ppm/K.')
    ch('R11',val='5.62k 0.1%',part='ERA-3AEB5621V',notes='Dzielnik CV, ±25 ppm/K.')
    ch('R14',val='226k 0.1%',part='ERA-3AEB2263V',notes='OVP typ. 28,08 V, uwzględnić skrajne progi komparatora.')
    ch('R15',val='10k 0.1%',part='ERA-3AEB103V',function='Dolna gałąź OVP',notes='Dzielnik OVP, ±25 ppm/K.')
    ch('C1',schematic=(111.76,68.58))
    return list(parts.values())

POSITIONS={
 'J1':(3.15,23.0),'F1':(11,10.2),'RV1':(11.1,4.85),'R1':(11.4,13.45),
 'BR1':(8.8,30.55),'C1':(17.35,31.3),'L1':(21.55,22.5),'C2':(11.65,24.5),
 'R2':(4.1,16.2),'R3':(11.45,16.2),'T1':(30,8.7),
 'D5':(19.35,15.95),'C3':(20.2,22.4),'R4':(17.4,19.65),'D6':(19.5,5.45),'C4':(17.3,2.1),
 'R5':(17.4,25.6),'R6':(14.9,29.3),'R7':(21.55,30.0),'C5':(21.4,30.25),'U1':(30,21.8),'CY1':(30,30.4),
 'C6':(46.0,7.4),'D7':(41.4,18.25),'R8':(38.8,22.4),'C7':(43.0,24.15),
 'R9':(38.4,16.0),'D8':(44.9,18.8),'R10':(39.45,25.0),'R11':(39.45,27.15),'C8':(39.45,29.3),
 'C9':(39.4,24.2),'R12':(46.8,21.55),'ZD1':(46.65,29.25),'Q1':(46.2,24.7),'C10':(46.8,28.5),
 'ZD2':(51.7,31.55),'R13':(53.0,31.4),'D9':(48.4,32.35),
 'U2':(57.15,11.55),'C11':(55.15,7.1),'R14':(50.75,15.95),'R15':(51.5,18.4),
 'R16':(63.05,13.8),'C12':(61.9,10.6),'R17':(47.6,17.6),'R18':(55.0,16.55),
 'R19':(55.8,30.6),'C13':(60.25,6.15),'J2':(64.05,5.7),'J3':(64.05,28.15),
 'U3':(52.65,25.25),'U4':(59.1,25.25),'R20':(49.5,28.75),'R21':(59.1,30.3),
 'C14':(51.4,21.25),'C15':(58.5,21.25)}
BACK={'F1','R2','R3','D5','C3','R4','R5','D6','C4','R6','R7','U1','R8','R9','D8','R10','R11','C8','C10','R21','R13','D9','C12'}
ROT={'BR1':0,'D5':0,'C6':180,'D6':0,'C3':0,'R4':0,'C11':0,'R15':0,'L1':90,'R7':90,'C7':90,'R9':270}

if __name__=='__main__':
    import sys
    d,b,parts,fx,nt=a.pwr(NAME,circuit(),(POSITIONS,BACK,ROT),libraries)
    if '--placement' not in sys.argv:
        route.route_board(b,fx,nt)
    a.p.SaveBoard(str(d/(NAME+'.kicad_pcb')),b)
    a.save(a.ROOT/'work'/'catalog_b.json',a.json.dumps([vars(c) for c in parts],ensure_ascii=False,indent=2))

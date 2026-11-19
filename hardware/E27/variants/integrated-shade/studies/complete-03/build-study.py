from pathlib import Path
import json,math,hashlib,sys
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else (Path(__file__).resolve().parents[6] if Path(__file__).resolve().parent.name=='complete-03' else Path(__file__).resolve().parent/'Velluneo-2.0')
S=ROOT/'hardware/E27/variants/integrated-shade/studies/complete-03'
W=ROOT/'hardware/E27/workflow/integrated-shade/complete-03'
OUT=Path(sys.argv[2]).resolve() if len(sys.argv)>2 else ROOT.parent.parent/'outputs'
OUT.mkdir(parents=True,exist_ok=True)
S.mkdir(parents=True,exist_ok=True);W.mkdir(parents=True,exist_ok=True)
def save(p,o):p.write_text(json.dumps(o,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
parts=[]
def part(ref,mpn,role,w,d,h,source,qualified=False,qty=1,notes=''):
    parts.append(dict(ref=ref,mpn=mpn,role=role,quantity=qty,envelope_mm=[w,d,h],dimension_kind='Conservative body/pad/lead-forming reservation; not a verified KiCad footprint',source=source,design_qualified=qualified,notes=notes))
part('U1','LYT0006D-TL','700V integrated driver',8,7,1.75,'https://www.power.com/sites/default/files/documents/lytswitch-0_family_datasheet.pdf',notes='Selected for prototype investigation. SO8C seven leads; exact package/padmap still due. C567677 base MPN has zero stock; -TL/C394206 procurement unconfirmed.')
part('BR1','MB10S-13','1000V bridge',8.5,6,2.7,'https://www.diodes.com/datasheet/download/MB10S.pdf',notes='Exact Diodes MPN; C460887 identified, stock unconfirmed/unavailable.')
part('RF1','FWFU2W10RJ / TE 3-2176792-3','10ohm2W fusible input resistor',24,7,6.5,'https://www.te.com/en/product-3-2176792-3.html',notes='16x5.5mm body;24x7mm reservation includes proposed22mm forming pitch. Pulse/fusing verification due.')
part('RV1','V275LA4P','275VAC MOV',10,6.6,12,'https://www.littelfuse.com/assetdocs/littelfuse_varistor_la_datasheet.pdf?assetguid=f7c547ce-c2fa-4789-86cc-ec39a5060afb',notes='9mm maximum disc, not nominal7mm.710V@10A clamp does NOT establish700V switch protection; surge coordination remains blocking.')
part('C1','ECWFD2W104JQ','100nF450V postbridge film',13.6,5.5,13.9,'https://industrial.panasonic.com/ww/products/pt/film-cap-electroequip/models/ECWFD2W104JQ',notes='DC postbridge only, not X2 across-line. ModelQ leadheight retained.')
part('C2','ECWFD2W334JQ','330nF450V postbridge film',13.6,6.6,15.4,'https://industrial.panasonic.com/ww/products/pt/film-cap-electroequip/models/ECWFD2W334JQ')
part('L1','RFB1010-103L','10mH differential input-filter candidate',12,12,11.5,'https://www.coilcraft.com/getmedia/aee5a84a-474c-4ccb-9d99-e17757a0098a/rfb.pdf',notes='Isat0.19A; input pulse/RMS waveform must qualify this value; otherwise larger part and new sizing needed.')
part('L2','RFB1010-152L','1.5mH power inductor starting candidate',12,12,11.5,'https://www.coilcraft.com/getmedia/aee5a84a-474c-4ccb-9d99-e17757a0098a/rfb.pdf',notes='Isat0.50A at10%typLdrop25C,Irms0.44A+20C. Worst currentlimit/temp/saturation/loss check due;1.5mH inherited starting point, not solved8Wmagnetics.')
part('D1','STTH1R06A','600V1A ultrafast freewheel diode',6.5,4,2.6,'https://www.st.com/resource/en/datasheet/stth1r06.pdf',notes='Chosen over US1J75ns because AN60 recommends faster diode. Verify actual pulse/thermal/recovery limit at temperature.')
part('C3,C8','GRM21BR71H104KA01L','100nF50V X7R bypass/gate RC',3,2.3,1.5,'https://www.murata.com/en-us/products/productdetail?partno=GRM21BR71H104KA01%23',qty=2,notes='0805 reservation; exact supplier suffix/landpattern to verify.')
part('C4','CL21A226MOCLRNC','22uF16V feedback hold capacitor',3,2.3,1.5,'https://product.samsungsem.com/mlcc/CL21A226MOCLRNC.do',notes='0805 candidate; DC bias/effective capacitance/reflow verification due.')
part('R1','RC1206FR-074K7L','4.7kohm input choke damping',4.2,2.6,1,'https://www.yageo.com/en/Product/Index/rchip',notes='Exact family/value candidate; pulse and power verification due.')
part('R2,R3','RC1206FR-0746R4L','46.4ohm1% sense resistors',4.2,2.6,1,'https://www.yageo.com/en/Product/Index/rchip',qty=2,notes='Parallel23.2ohm starting estimate scales82mA/26.8ohm reference toward94.7mA; not a proven current setting.')
part('Q1','X0202NN5BA4','800V sensitive-gate SCR latch',8,8,1.8,'https://www.st.com/resource/en/datasheet/x02.pdf',notes='ST active family.200uA gate,5mA holding/6mA latching25C specifiedconditions; fullcorner verification due.')
part('D2','DL4005-13-F','SCR latch source/BP diode',6,3.5,2.7,'https://www.diodes.com/datasheet/download/DL4001.pdf',notes='Use AN60Fig8 topology; not substituted with freewheel diode.')
part('R6','CRCW2010100RFKEF','100ohm latch discharge resistor',6.2,3.5,1,'https://www.vishay.com/docs/20035/dcrcwe3.pdf',notes='2010 reservation for pulse margin; pulse energy/continuous fault power still unresolved.')
part('R4,R5','RC0805FR-071KL','1kohm SCR gate network',3,2.3,1,'https://www.yageo.com/en/Product/Index/rchip',qty=2)
part('VR1','1N4764A','100V detector Zener',13,4,3.2,'https://services.taiwansemi.com/storage/resources/datasheet/1N4740A%20SERIES_O2104.pdf',notes='95–105V at2.5mA only; actual~1mA triggerwindow NOT established.13mm includes axial forming, not body only.')
part('CB','GRM31CR72E104KW03L','100nF250V base output candidate',4.2,3.5,2,'https://www.murata.com/en-us/products/productdetail?partno=GRM31CR72E104KW03%23',notes='Only for reservoir-on-module option; effectiveC/OVP transient behavior unqualified.')
part('RB1,RB2','RC1206FR-0722KL','22kohm1% module/base reservoir discharge',4.2,2.6,1,'https://www.yageo.com/en/Product/Index/rchip',qty=2,notes='Series44kohm;two resistors. Single-open fault defeats discharge; not certified accessible-contact protection.')
part('COUT','EEUED2C680','68uF160V output reservoir',13.5,13.5,20,'https://industrial.panasonic.com/ww/products/pt/aluminum-cap-lead/models/EEUED2C680',notes='ActualbodyØ12.5x20mm,5mmpitch.160V qualification envelope/overshoot still due. Ripple/endurance source discrepancy unresolved.')
part('JAC','Unspecified: solder-pad reservation','mains wire interface space only',10,6,2,'Owner mechanical interface deferred',notes='Not a selected connector; access/insulation/padintent approval still required.')
part('JLED','Unspecified: solder-pad reservation','LED-module interface space only',10,6,2,'Owner mechanical interface deferred',notes='Not a selected touchsafe connector; physical mating/mechanics must be defined.')
save(S/'candidate-bom.json',dict(revision='IS-COMPLETE-03-1',selection='LYT0006D-TL high-side buck with SCR latch OVP requiring AC reset; reservoir-on-module is preferred sizing variant, pending electrical qualification',estimated_total_driver_output_w=8,illustrative_led_voltage_v=85,illustrative_total_output_current_ma=95,parts=parts,qualification='All are engineering selections for review, not an approved/procurement-ready productionBOM. Interfaces deliberately unidentified. Not a complete physical-pin contract.'))

def items(module):
    out=[]
    for p in parts:
        if module and p['ref'] in ['COUT','RB1,RB2']:continue
        if not module and p['ref']=='CB':continue
        for i in range(p['quantity']):out.append(dict(ref=p['ref'] if p['quantity']==1 else p['ref'].split(',')[i],w=p['envelope_mm'][0]+1,d=p['envelope_mm'][1]+1,h=p['envelope_mm'][2],body_w=p['envelope_mm'][0],body_d=p['envelope_mm'][1],role=p['role']))
    # Three tooling/test keepout reservations, not a finished mounting pattern.
    for i in range(3):out.append(dict(ref='TOOL'+str(i+1),w=4,d=4,h=0,body_w=3,body_d=3,role='provisional tooling keepout'))
    return out

def pack(rects,w,d):
    free=[(1,1,w-2,d-2)];placed=[]
    for r in sorted(rects,key=lambda r:r['w']*r['d'],reverse=True):
        choices=[]
        for k,(x,y,fw,fd) in enumerate(free):
            for rw,rd,rot in [(r['w'],r['d'],False),(r['d'],r['w'],True)]:
                if rw<=fw and rd<=fd:choices.append((min(fw-rw,fd-rd),max(fw-rw,fd-rd),k,rw,rd,rot))
        if not choices:return None
        _,_,k,rw,rd,rot=min(choices);x,y,fw,fd=free.pop(k)
        placed.append(dict(**r,x=x,y=y,packed_w=rw,packed_d=rd,rotated=rot))
        # Guillotine split: disjoint cells.
        if fw-rw>0:free.append((x+rw,y,fw-rw,rd))
        if fd-rd>0:free.append((x,y+rd,fw,fd-rd))
    return placed
cases=[]
for module,label in [(True,'Reservoir on LED module'),(False,'Reservoir in base')]:
    rs=items(module);area=sum(x['w']*x['d'] for x in rs);poss=[]
    for w in range(40,71,2):
        for d in range(26,43,2):
            if area/(w*d)>.70:continue
            p=pack(rs,w,d)
            if p:poss.append((w*d,w+d,w,d,p))
    assert poss
    _,_,w,d,p=min(poss)
    # Explicit geometry checks, not ERC/DRC or safety checks.
    assert all(x['x']>=1 and x['y']>=1 and x['x']+x['packed_w']<=w-1+1e-9 and x['y']+x['packed_d']<=d-1+1e-9 for x in p)
    for i,a in enumerate(p):
        for b in p[i+1:]:assert a['x']+a['packed_w']<=b['x']+1e-9 or b['x']+b['packed_w']<=a['x']+1e-9 or a['y']+a['packed_d']<=b['y']+1e-9 or b['y']+b['packed_d']<=a['y']+1e-9
    cases.append(dict(variant=label,board_experiment_mm=[w,d],single_side=True,highest_part_mm=max(x['h'] for x in p),board_thickness_proposal_mm=1.6,rectangle_fill_fraction=area/(w*d),placed=p,module_reservoir=module))
save(S/'fit-study.json',dict(revision='IS-COMPLETE-03-1',kind='Unrouted rectangle-reservation experiment, NOT KiCad placement or manufacturable PCB',assumptions=['1mm added to each envelope width/depth,1mm boardedge reserve are packing assumptions, NOT approved electrical/safety distances.','Maximum70% envelope occupancy is only a routing-space heuristic.','No switching loops, copper routing, creepage/clearance, PCBthermal analysis, footprint pin/padmap or enclosure fit has been verified.','Lead forming, connector size and actual process tooling need approval.','Singleface reservation means space only; exactpart availability and Economic eligibility unresolved.','No physical ability to hotplug is implied by moving reservoir.'],cases=cases))
fontpath=r'C:\Windows\Fonts\arial.ttf';font=ImageFont.truetype(fontpath,20);small=ImageFont.truetype(fontpath,13);title=ImageFont.truetype(fontpath,28)
im=Image.new('RGB',(1350,950),'#f6f5f1');draw=ImageDraw.Draw(im)
draw.text((36,22),'VELLUNEO / propozycja gabarytow IS-03',font=title,fill='#182c30')
draw.text((36,62),'Rezerwacje miejsca dla konkretnych czesci. Bez sciezek i potwierdzenia izolacji.',font=font,fill='#515c5e')
for ix,c in enumerate(cases):
    ox=45+ix*660;oy=170;scale=10;w,d=c['board_experiment_mm']
    lab='Kondensator w module LED' if c['module_reservoir'] else 'Kondensator w bazie'
    draw.text((ox,110),lab,font=font,fill='#182c30')
    draw.text((ox,138),f'{w} x {d} mm | elementy do {c["highest_part_mm"]:g} mm wysokosci',font=small,fill='#515c5e')
    draw.rectangle((ox,oy,ox+w*scale,oy+d*scale),fill='#e0e9e3',outline='#304f47',width=2)
    for p in c['placed']:
        x=ox+p['x']*scale;y=oy+p['y']*scale;rw=p['packed_w']*scale;rd=p['packed_d']*scale
        draw.rectangle((x+2,y+2,x+rw-2,y+rd-2),fill='#f9faf8',outline='#71867c',width=1)
        label=p['ref'].replace(',','/')
        draw.text((x+4,y+4),label,font=small,fill='#1e3730')
    txt=['Wariant wybrany do dalszej weryfikacji.','Na module: 68 uF / 160 V + 2 rezystory.'] if c['module_reservoir'] else ['Wieksza baza; pozostaje ochrona przed','rozladowaniem kondensatora przy podlaczeniu.']
    for n,line in enumerate(txt):draw.text((ox,oy+d*scale+20+n*24),line,font=font,fill='#182c30')
draw.text((36,760),'Co ten podglad potwierdza',font=font,fill='#182c30')
for n,line in enumerate(['Prostokaty czesci i rezerwy nie nakladaja sie w tym eksperymencie.', 'To wstepny budzet gabarytow do sprawdzenia: nie wynik trasowania ani optimum.', 'Wysokosc zestawu wymaga doliczenia PCB, odstepow od obudowy i wyprowadzen.', 'Zrodla: karty producentow w candidate-bom.json; obliczenia i uklad: IS-COMPLETE-03.']):draw.text((36,795+n*26),line,font=font,fill='#515c5e')
im.save(OUT/'Velluneo_IS03_gabaryty.png');im.save(S/'fit-preview.png')
print(json.dumps([dict(variant=c['variant'],board=c['board_experiment_mm'],height=c['highest_part_mm'],fill=c['rectangle_fill_fraction']) for c in cases]))

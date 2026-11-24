from pathlib import Path
import json,hashlib,re,math
H=Path(__file__).resolve().parent;C=H/'candidate'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save=lambda p,d:p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
mpn='PR02FS0201000KR500';url='https://www.vishay.com/docs/28915/pr02fs.pdf'
def block(s,start):
 depth=0;quoted=False;esc=False
 for i in range(start,len(s)):
  c=s[i]
  if quoted:
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':quoted=False
  elif c=='"':quoted=True
  elif c=='(':depth+=1
  elif c==')':
   depth-=1
   if depth==0:return i+1
 raise ValueError('unbalanced')
def change(s):
 return s.replace('768772332',mpn).replace('https://www.we-online.com/components/products/datasheet/'+mpn+'.pdf',url).replace('3m3 / EMI','100R / RC DAMPER')
p=C/'SC09_compact.kicad_pcb';s=p.read_text();m=re.search(r'\(footprint\s+"E27SC09:SC09_L1"',s);assert m
end=block(s,m.start());b=s[m.start():end];assert '768772332'in b
b=change(b);b=re.sub(r'\(descr\s+"[^"]*"\)', '(descr "SB01-R2 ECO: legacy L1 position populated with Vishay PR02FS 100ohm RC damper; original pads/courtyard retained; vertical formed leads <=16mm planning")',b)
s=s[:m.start()]+b+s[end:];p.write_text(s)
p=C/'SC09_compact.kicad_sch';s=change(p.read_text());s=s.replace('Fused input / MOV / bridge / EMI filter','Fused input / MOV / bridge / RC input filter')
s=s.replace('Catalogue T1/L1/HVR25 and manufacturer lands; manual lead forming for RF1/R7/C6. Stock/thermal/fault qualification remain separate.','SB01-R2: L1 legacy position = PR02FS 100R RC damper, NOT a choke. Manual lead forming <=16mm; EMI/hot/fault qualification open.')
s=s.replace('(rev "SC09-CAT01 engineering")','(rev "SC09-SB01-R2 RC engineering")');p.write_text(s)
p=C/'E27SC09.kicad_sym';p.write_text(change(p.read_text()))
p=C/'E27SC09.pretty/SC09_L1.kicad_mod';s=p.read_text();s=re.sub(r'\(descr\s+"[^"]*"\)','(descr "Legacy L1 slot: PR02FS100 RC resistor; unchanged copper/pads/courtyard; vertically formed leads <=16mm planning")',s);p.write_text(s)
for name in ['bom-build.json']:
 p=C/name;d=json.loads(p.read_text());d['revision']='SC09-SB01-R2';d['status']='RC startup correction candidate; physical legacy position L1 retained. No new manufacturing/powered approval.'
 for row in d['components']:
  if row['ref']=='L1':
   row.update(value='100ohm 10% 2W RC damper (legacy L1 position)',mpn=mpn,kind='pulse-rated flameproof non-inductive resistor',source=url,package='axial PR02-FS, vertical manual forming on existing 5.0038mm TH pair',body_or_reservation_mm=[3.9,10,16],notes='Analysis designation R10 maps to physical legacy L1. Removes intentional input LC resonance; RF1 remains47ohm. Standard inductor substitution forbidden. Original copper, pads, courtyard and outline unchanged.',assembly='Body center above pad1; >=2mm PCB standoff; <=16mm planned total height including bent return lead. Inspect sample/lead forming before assembly; body90C provisional stop.')
  if row['ref']=='RF1':row['notes']='Protective FW20A47R0JA retained. R2 replaces downstream L1 with a resistor; obsolete LC overshoot screen is historical, not the new RC result.'
 save(p,d)
p=C/'README.SB01-R2.md';p.write_text('''# SB01 R2 — same-board RC startup correction candidate

The physical legacy **L1** position is now populated with **PR02FS0201000KR500,
100 ohm, 10%, 2 W**. It is called R10 in the engineering calculations only.
Its L1 reference, local-library identifier and original two pads are deliberately
retained to match the existing PCB/silkscreen and manual assembly location.
The custom two-terminal zigzag symbol now shows the resistor value and datasheet.
Do not fit the old 768772332 choke at this position in the R2 assembly.

RF1 remains the selected 47 ohm protective fusible resistor. No net, pin, copper,
via, outline, mask or legend change is intended. The new resistor body/model is
an engineering assembly representation, not a manufacturer-qualified fit model.
The <=16mm formed-resistor height stays within the retained19.5mm module envelope;
actual lead forming/support and hot clearance still require a sample inspection.

The passive RC model removes the original deliberate LC energy exchange.
It does not model silicon switching, parasitic inductance, EMC or finished faults.
New source and assembly evidence invalidate prior exact-source release acceptance.
Native checks and artifact comparisons must be rerun; existing Gerbers may be
retained only if full copper/mask/outline/drill identity is proved.

Cold normal startup pulse support is based on the exact PR02-FS primary curve.
Full hot pulse capability, operating RMS/temperature, surge, output OVP dynamics,
LED current, MOSFET-short consequences and EMC remain measurement gates.
This candidate does not authorize a supplier order, powered testing or product use.
''',encoding='utf-8')
p=C/'README.md';p.write_text('Current startup correction candidate: [SB01-R2](README.SB01-R2.md). Earlier R1 release files and descriptions below are historical.\n\n'+p.read_text(),encoding='utf-8')
def cylinder(x,y,z0,z1,r,color,n=32):
 pts=[(x+r*math.cos(2*math.pi*i/n),y+r*math.sin(2*math.pi*i/n),z)for z in [z0,z1]for i in range(n)]
 coords=', '.join(' '.join(f'{v/2.54:.7f}'for v in p)for p in pts);faces=[]
 for i in range(n):faces.append(f'{i}, {(i+1)%n}, {(i+1)%n+n}, {i+n}, -1')
 faces.extend([', '.join(map(str,range(n-1,-1,-1)))+', -1',', '.join(map(str,range(n,2*n)))+', -1'])
 return 'Shape { appearance Appearance { material Material { diffuseColor '+color+' } } geometry IndexedFaceSet { solid FALSE coord Coordinate { point [ '+coords+' ] } coordIndex [ '+', '.join(faces)+' ] } }\n'
model='#VRML V2.0 utf8\n# R2 illustrative PR02FS upright resistor, 1 unit=2.54mm; no vendor fit qualification\n'
model+=cylinder(-2.5019,0,3,13,1.95,'.65 .12 .08')
for z,col in [(5,'.25 .10 .04'),(6,'0 0 0'),(7,'.25 .10 .04'),(9,'.7 .7 .7'),(11,'0 0 0')]:model+=cylinder(-2.5019,0,z,z+.35,1.97,col)
model+=cylinder(-2.5019,0,-1.6,3,.39,'.7 .7 .7')+cylinder(2.5019,0,-1.6,16,.39,'.7 .7 .7')
(C/'Models/SC09_L1.wrl').write_text(model)
# Preserve every historical record; add a truthful superseding engineering decision.
save(C/'startup-correction.SB01-R2.json',{'revision':'SC09-SB01-R2','status':'engineering_candidate_NOT_approved','physical_position':'L1','calculation_designation':'R10','old_mpn':'768772332','selected_mpn':mpn,'RF1_retained':'FW20A47R0JA','reason':'Replace intentional input LC resonance with a passive RC input branch; retain topology node membership and PCB artwork','new_component_or_net_count':False,'no_new_board':True,'manual_forming_height_planning_mm':16,'provisional_body_stop_C':90,'normative_or_powered_approval':False,'order_submitted':False,'prototype_scope':'Normal207-253VAC/50Hz lab prototype; surge/abnormal/hot behavior remain explicitly unqualified'})
files={p.relative_to(C).as_posix():sha(p)for p in C.rglob('*')if p.is_file()}
before=json.loads((H/'before.json').read_text())['files'];diff=[n for n,h in files.items()if before.get(n)!=h]
save(H/'candidate-edit-handoff.json',{'writer':'/root','scope':'Only candidate copy; canonical source still unchanged','changed_files':diff,'no_pin_or_net_or_numeric_rule_change_intended':True,'physical_measurements_performed':False,'human_approval':False})
print(json.dumps({'changed':diff,'canonical_untouched':True}))

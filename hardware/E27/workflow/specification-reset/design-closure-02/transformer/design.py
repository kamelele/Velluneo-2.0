"""T1 construction candidate and 1D air-energy screening, not FEA/measurement.
Run with standard Python; optional --png requires Pillow in external PYTHONPATH.
No native source STEP is fabricated, imported or claimed checked by this script.
"""
from pathlib import Path
import math,json,hashlib,argparse,xml.etree.ElementTree as ET
D=Path(__file__).resolve().parent;P=D.parents[1]
ap=argparse.ArgumentParser();ap.add_argument('--png',action='store_true');ap.add_argument('--material-source-dir',type=Path);args=ap.parse_args()
inputs=['pcb-readiness-01/isolation/construction-candidate.json','pcb-readiness-01/isolation/sources.json','electrical-integration/magnetics/winding-results.json','electrical-integration/magnetics/window-results.json','transformer-footprint/source-step-faces.json','transformer-footprint/source-step-findings.json','transformer-footprint/geometry-contract.json','schematic-intent/intended-connectivity.json','electrical-integration/proposed-parts.json']
reg=json.loads((D/'sources.json').read_text())
for r in reg['repository_inputs']:
 assert hashlib.sha256((P/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
material_checked=[]
if args.material_source_dir:
 for r in reg['retained_material_bytes']:
  b=(args.material_source_dir/r['filename']).read_bytes();assert hashlib.sha256(b).hexdigest()==r['sha256'],r['filename']
  material_checked.append({'filename':r['filename'],'sha256':r['sha256'],'bytes':len(b)})
c0=json.loads((P/inputs[0]).read_text());assert c0['turns']=={'P':120,'A':22,'S':30}
assert c0['winding_pins']=={'P':['1','5'],'A':['2','4'],'S':['6','10']}
tp=next(x for x in json.loads((P/'electrical-integration/proposed-parts.json').read_text()) if x['ref']=='T1')
assert tp['pins']=={'1':'BULK_POS','2':'PRIMARY_GND','3':None,'4':'AUX_RAW','5':'DRAIN','6':'OUTPUT_NEG','7':None,'8':None,'9':None,'10':'SECONDARY_RAW'}
faces=json.loads((P/inputs[4]).read_text());rawbox=[min(f['box'][j] for f in faces) if j%2==0 else max(f['box'][j] for f in faces) for j in range(6)]
assert len(faces)==430 and abs(rawbox[0]+12.5)<1e-5 and abs(rawbox[4]+13)<1e-5
# A segment has a homogeneously distributed axial current sheet across its OD.
# P1/P2 are one continuous series primary, no extra physical pin or external net.
baseline=[('P',40,.217),('P',40,.217),('P',40,.217),('T',0,.154),('A',22,.217),('T',0,.077),('S',15,.520),('S',15,.520),('T',0,.077)]
selected=[('P',60,.217),('T',0,.154),('A',22,.217),('T',0,.077),('S',15,.520),('T',0,.077),('S',15,.520),('T',0,.077),('P',60,.217),('T',0,.077)]
aoutside=[('P',60,.217),('T',0,.077),('S',15,.520),('T',0,.077),('S',15,.520),('T',0,.077),('P',60,.217),('T',0,.154),('A',22,.217),('T',0,.077)]
MU0=4*math.pi*1e-7; p0=(2*(13.1+6.9)-8*2+2*math.pi*2)/1000
def inductance(segments,width_mm,curr,steps=None,extra_sep_mm=0):
 x=F=total=0.;rows=[]
 for k,(w,n,mm) in enumerate(segments):
  # Extra unmodeled radial air in a selected tape barrier is a sensitivity only.
  if k==3:mm+=extra_sep_mm
  dx=mm/1000;s=n*curr.get(w,0)/dx;per=p0+2*math.pi*x
  exact=per*(F*F*dx+F*s*dx*dx+s*s*dx**3/3)+2*math.pi*(F*F*dx*dx/2+2*F*s*dx**3/3+s*s*dx**4/4)
  val=exact if steps is None else sum((p0+2*math.pi*(x+(j+.5)*dx/steps))*(F+s*(j+.5)*dx/steps)**2*dx/steps for j in range(steps))
  rows.append({'segment':k,'winding':w,'turns':n,'radial_start_mm':x*1000,'radial_end_mm':(x+dx)*1000,'MMF_start_At':F,'MMF_end_At':F+s*dx,'leakage_contribution_H':MU0/(width_mm/1000)*exact})
  total+=val;F+=s*dx;x+=dx
 assert abs(F)<1e-10,'Only ampere-turn-balanced current combinations are modeled'
 return MU0/(width_mm/1000)*total,rows
currents={'PS_Aopen':{'P':1,'A':0,'S':-4},'PA_Sopen':{'P':1,'A':-120/22,'S':0},'AS_Popen':{'P':0,'A':1,'S':-22/30}}
cases=[]
for name,seg,widths in [('baseline',baseline,[8.25,10.5,16.2]),('interleaved_Ainner',selected,[13.3,13.8,14.3]),('interleaved_Aoutside',aoutside,[13.8])]:
 for width in widths:
  cases.append({'construction':name,'common_sheet_width_mm_assumption':width,'leakage_H':{key:inductance(seg,width,v)[0] for key,v in currents.items()}})
Lps,segments=inductance(selected,13.8,currents['PS_Aopen']);Laa=inductance(selected,13.8,currents['AS_Popen'])[0]
Lboth=inductance(selected,13.8,{'P':1,'A':1,'S':-142/30})[0];Lpa=(Lboth-Lps-Laa)/2
det=Lps*Laa-Lpa*Lpa;assert Lps>0 and Laa>0 and det>0
matrixPA=Lps+2*Lpa*(-120/22)+Laa*(120/22)**2
assert abs(matrixPA-inductance(selected,13.8,currents['PA_Sopen'])[0])<1e-18
numerical=[]
for steps in [40,80,160,320]:
 val=inductance(selected,13.8,currents['PS_Aopen'],steps)[0]
 numerical.append({'midpoints_per_segment':steps,'H':val,'absolute_error_H':abs(val-Lps)})
assert numerical[-1]['absolute_error_H']<numerical[0]['absolute_error_H']/50
assert numerical[-1]['absolute_error_H']<1e-10
regular=sum(s[2] for s in selected);seam=.077;build=regular+seam
assert abs(regular-2.153)<1e-12 and abs(build-2.230)<1e-12
side=(18.7-.6-13.1)/2-build-.05-.05
band=13.8;end=(16.2-band)/2
assert side>0 and end>0
contract={
 'id':'T1-INTERLEAVED-C2','status':'Proposed construction drawing; not approved/shared CAD, supplier-confirmed build, FEA, test or recognized finished component',
 'graph_and_external_pins_unchanged':True,'turns':{'P':120,'A':22,'S':30},'pins':{'P_dot':1,'P_finish':5,'A_dot':2,'A_finish':4,'S_dot':6,'S_finish':10,'unwound':[3,7,8,9]},
 'parts':{k:c0[k] for k in ['core_gapped','core_ungapped','bobbin','yokes','wire_P_A','wire_S','tape','EIS_candidate']},
 'selected_order_inner_to_outer':[{'winding':w,'turns':n,'radial_mm':t} for w,n,t in selected],
 'winding_band_mm':band,'pitch_mm':{'P60':band/60,'A22':band/22,'S15':band/15},
 'pitch_definition':'Conservative turn-cell width: n*pitch=13.8mm. Actual center-to-center occupied span=(n-1)*pitch+wireOD is smaller. Spread S and A evenly; do not close-pack into narrower subbands.',
 'P_connection':'One continuous120-turn wire,60 inner plus60 outer, same winding sense in electrical series; park the continuous bridge in the primary-side end pocket without a splice or extra pin. Start1 and finish5. No use of NC pins as a hidden junction.',
 'S_connection':'One continuous30-turn TIW wire,15+15 in electrical series with a controlled end crossover; dot6/finish10 and continuous insulation into terminal zones.',
 'geometry_mm':{'native_barrel_XY':[13.1,6.9],'native_barrel_corner_R':2,'native_straight_barrel_axial':16.2,'selected_active_band':band,'regular_radial':regular,'extra_noncoincident_seam_radial':seam,'maximum_radial':build,'outer_regular_shell_XY':[13.1+2*build,6.9+2*build],'minimum_side_screen_remaining_after_chosen_0p05_build_and_0p05_decenter':side,'axial_end_pocket_each':end,'proposed_finished_envelope':[30,30,18]},
 'seams':{'max_extra_tape_layers_any_angle':1,'overlap_mm':1.0,'required':'All6wrap seams staggered; no coincident ridge, no6layer overlap.0.077mm is imposed incoming upper thickness, not a new vendor guarantee.'},
 'leadout_contract':{'native_coordinates':'Bobbin STEP X,Y,Z. PCB component-side coordinates x=X,y=-Z; pins project +Y; source mark/dot map preserved.',
  'primary_pocket_Z_range_mm':[-8.1,-6.9],'secondary_pocket_Z_range_mm':[6.9,8.1],
  'primary_bridge_center_Z_mm':-7.5,'bridge_protection':'Candidate optional FIS-B3-listed Essex Furukawa PIT-S tubing; incoming required ID>=0.25mm,OD<=0.60mm. Dimensions are a new procurement requirement, not sourced product capability or a complete barrier rating.',
  'tube_placement_axial_error_max_mm':.15,'tube_max_OD_mm':.60,'axial_residual_each_mm':end/2-.60/2-.15,
  'routing':'P/A starts, finishes and parked bridge exit only to row1-5 at negativeZ; S starts/finish and crossover exit only to row6-10 at positiveZ. NC pins stay unwound. No stripped secondary wire may traverse core/yoke/primary pockets.',
  'not_verified':'End-pocket axial arithmetic does not prove bend radius, local radial/core/yoke clearance, barrier continuity or real winding-machine capability. A dimensioned actual3D exit/yoke section remains mandatory.'},
 'material_process_requirements':['Builder must adopt/confirm actual FIS-B3 recognized material functions/sites/grades; no recognition is claimed for this finished transformer.','P/A two complete1350F-1 wraps retained; S TIW supplies its stated component function, not an assumed end-product standard pass.','No base wrap assumes actual PM-9630 all-path wall>=0.3mm and source-function acceptance; this remains unverified.','Off-bobbin TIW end preparation and qualified pin joining remain separate. No420C wire test copied onto bobbin.','Do not add varnish, adhesive or tube substitutions outside confirmed EIS. PIT-S listing alone does not confirm selected size or bend capability.'],
 'magnetic_acceptance':{'Lp_mH':[2.0736,2.5344],'turns_ratio':'120:22:30; exact polarity/dots as specified','effective_PS_leakage_max_uH_proposal':20,'method':'Three-winding impedance model from independently measured pair conditions and operation checks, with fixture compensation/frequency/signal/amplitude recorded;20uH not established by this drawing or slab model.'},
 'insulation_access':'Core/yokes treated as hazardous primary-domain objects; bare secondary terminal pockets require actual air/surface/solid separation assessment. No norm-derived clearance, creepage or test voltage is adopted here.',
 'effect_on_old_evidence':'Ideal turns graph/values retained; winding distribution, length/DCR, leakage/capacitance and field coupling change. Old winding-specific startup/clamp/parasitic/thermal/process calculations cannot be claimed validated for this construction without affected re-analysis.'}
assert contract['leadout_contract']['axial_residual_each_mm']>0
length=[];cum=0;wireidx={'P':0,'A':0,'S':0}
wireturns={'P':0,'A':0,'S':0};Lwire={'P':.100,'A':.060,'S':.080}
for w,n,t in selected:
 if n:
  pitch=band/n;center=cum+t/2;perimeter=p0*1000+2*math.pi*center
  helix=math.hypot(perimeter,pitch);lm=n*helix/1000;Lwire[w]+=lm;wireturns[w]+=n
  length.append({'winding':w,'turns':n,'radial_center_mm':center,'MLT_rounded_rectangle_mm':perimeter,'helical_length_m':lm})
 cum+=t
assert wireturns==contract['turns']
R20per={'P':.7007,'A':.7007,'S':.2629};I={'P':.091545,'A':.10,'S':.53879};loss=[]
cutlimit={'P':5.4,'A':.95,'S':1.45}
assert all(Lwire[w]<=cutlimit[w] for w in cutlimit)
contract['proposed_cut_length_upper_m_including_leads']=cutlimit
contract['proposed_DCR20_upper_ohm']={w:cutlimit[w]*R20per[w] for w in cutlimit}
contract['cut_length_status']='Design/procurement acceptance proposal with explicit reserve above regular helical calculation; not confirmed builder capability. TEX-E source R20 is reference table, so exact purchased-wire resistance requirement must be agreed.'
contract['material_process_requirements'].append('A-to-outerP has three intervening complete1350F-1 wraps (around A, between S layers, before outerP); do not count spaced TIW roundwires themselves as a continuous sheet barrier. Exit paths still require separate all-path review.')
for temp in [20,100,110,125]:
 row={w:{'length_m_calculated_geometry_and_leads':Lwire[w],'length_m_proposed_acceptance_upper':cutlimit[w],'resistance_ohm':R20per[w]*cutlimit[w]*(1+.00393*(temp-20)),'I_RMS_A_screen':I[w]} for w in I}
 for w in row:row[w]['DC_equivalent_loss_W']=row[w]['resistance_ohm']*I[w]**2
 total=sum(r['DC_equivalent_loss_W'] for r in row.values())
 loss.append({'temperature_C':temp,'windings':row,'total_DC_equivalent_W':total,'remaining_of_0p50W_T1_budget_for_core_AC_gap_termination_W':.5-total})
flux=[]
for lp in [2.0736e-3,2.304e-3,2.5344e-3]:
 for ip in [.358522,1.6/(2.37*.979)]:
  b=lp*ip/(120*57e-6);flux.append({'Lp_H':lp,'Ipk_A':ip,'kind':'normal witness' if ip<.5 else 'static backup-current proxy, NOT maximum dynamicfault','B_from_LpI_over_NA_T':b,'remanence_not_included':True})
# Inverse budget frontier: no waveform-specific core loss is fabricated from sine data.
hot=next(x for x in loss if x['temperature_C']==110);available=hot['remaining_of_0p50W_T1_budget_for_core_AC_gap_termination_W']
result={'kind':'Executed source-pinned construction and conditional air-energy/DC screens; no FEA, leakage guarantee, actual temperature or measurement','candidate':contract['id'],'raw_bobbin_bbox_from_retained430face_data_mm':rawbox,'fresh_STEP_import_performed':False,'source_retrieval_limitation':'New primary STEP/PDF byte attempts failedDNS in child andHTTP403 in coordinator; retained prior pinned geometry used.','geometry':contract['geometry_mm'],'leakage_cases':cases,'selected_PS_slab_H':Lps,'selected_balanced_two_coordinate_leakage_matrix_H':[[Lps,Lpa],[Lpa,Laa]],'matrix_coordinates':'Ip,Ia with Is=-(120Ip+22Ia)/30; only balanced air-energy subspace, not a complete3port magnetizing model','PSD_determinant_H2':det,'PA_matrix_consistency_error_H':abs(matrixPA-inductance(selected,13.8,currents['PA_Sopen'])[0]),'numerical_midpoint_convergence':numerical,'selected_PS_segment_energy':segments,'extra_A_S_radial_separation_sensitivity':[{'extra_mm':x,'PS_slab_H':inductance(selected,13.8,currents['PS_Aopen'],extra_sep_mm=x)[0]} for x in [0,.05,.1,.2]],'selected_PS_model_fraction_of20uH':Lps/20e-6,'max_unmodeled_extra_before20uH_H_arithmetic_only':20e-6-Lps,'length_by_layer':length,'copper_loss_screens':loss,'flux_screens':flux,'core_and_AC_loss_acceptance':{'T1_total_normal_loss_target_W':.5,'110C_DC_equivalent_screen_W':hot['total_DC_equivalent_W'],'remaining_core_plus_AC_plus_fringe_plus_termination_W':available,'N87_source_reference':'June2025 material p2 typical375kW/m3 at100kHz,200mT,100C; Bs390mT atH1200A/m/10kHz/100C. Neither is actual flyback loss or safe operating flux. No fitted Steinmetz coefficients or unipolar/DC-bias correction available.','required':'Actual waveform-specific core+AC/fringing/termination loss must fit remaining budget across duty/frequency/temperature and all required faults. Do not compare total triangular flux swing directly to sinusoidal peak or use Bs as a designpass.'},'capacitance_EMI':'Interleaving adds another P/S-facing interface. TI SLUP338 identifies leakage/capacitance tradeoff. No actual Cps or commonmode current is established; EMI/VS sampling and startup must be reassessed.','limitations':['1D homogenized sheets omit axial fringe/unequal occupancy, round-wire local fields,3D core/gap/yoke geometry and leadouts. Variable MLT is geometric, not FEA.','The modeled width is an explicit common current-sheet assumption; total physicalwindow width is not a guarantee that windingcurrent occupies it.','Baseline result flags20uH as unsupported by prior construction; it does not mathematically prove measuredbaselinefailure. Selected14uH is a promisingcandidate, not a manufacturedmaximum.','Layer pitch and end-pocket/tube limits are proposed controls, not confirmed winding-builder capabilities.','Copper skin/proximity/gapfringing/termination and core loss are omitted from DC loss numbers. RMS maxima are conservative separate priorwitnesses; A100mA is a sensitivity.','Changes are proposed only. No shared footprint,graph,BOM,approvedrequirements or productPCB is modified.']}
result['material_files_hash_checked']=material_checked
def bessel(order,z):
 term=(z/2)**order/math.factorial(order);value=term
 for k in range(1,80):
  term*=-(z*z/4)/(k*(k+order));value+=term
  if abs(term)<max(abs(value),1)*1e-17:break
 return value
def skin_ratio(radius,frequency,temp):
 rho=1.724e-8*(1+.00393*(temp-20));delta=math.sqrt(rho/(math.pi*frequency*MU0));z=(1-1j)*radius/delta
 return ((z/2)*bessel(0,z)/bessel(1,z)).real,delta
assert abs(skin_ratio(.00015,1,20)[0]-1)<1e-8
result['isolated_round_wire_skin_sensitivity']=[{'radius_mm':r,'frequency_Hz':f,'temperature_C':t,'Rac_over_Rdc_isolated_wire':skin_ratio(r/1000,f,t)[0],'skin_depth_mm':skin_ratio(r/1000,f,t)[1]*1000} for r in [.09,.15] for f in [106000,500000,1000000,2000000] for t in [20,110]]
result['skin_sensitivity_scope']='Own round-conductor diffusion/Bessel solution using engineeringrho20=1.724e-8ohmm,alpha.00393,mu_r1; no proximity,gapfield,terminations or actual current spectrum. Singlefrequency ratios cannot bound actual AC loss.'
(D/'construction-contract.json').write_text(json.dumps(contract,indent=2)+'\n',encoding='utf-8',newline='\n')
(D/'results.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8',newline='\n')
# Native SVG drawing, no vendor artwork or implied CAD/FEA.
S=[];W,H=1200,1000
S.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}"><rect width="1200" height="1000" fill="#f8fafc"/><style>text{{font-family:Arial,sans-serif;fill:#172033}} .small{{font-size:13px}} .title{{font-size:24px;font-weight:bold}} .label{{font-size:16px}} .dim{{stroke:#172033;stroke-width:1.2;fill:none}} .dash{{stroke-dasharray:6 4}}</style>')
png=None
if args.png:
 from PIL import Image,ImageDraw,ImageFont
 png=Image.new('RGB',(W,H),'#f8fafc');pd=ImageDraw.Draw(png)
 fontpath=Path('C:/Windows/Fonts/arial.ttf');boldpath=Path('C:/Windows/Fonts/arialbd.ttf')
def txt(x,y,t,size=14,bold=False):
 import html
 S.append(f'<text x="{x}" y="{y}" font-size="{size}"'+(' font-weight="bold"' if bold else '')+'>'+html.escape(t)+'</text>')
 if png:pd.text((x,y-size),t,fill='#172033',font=ImageFont.truetype(str(boldpath if bold else fontpath),size))
def line(x1,y1,x2,y2,color='#172033',width=1.2,dash=False):
 S.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{color}" stroke-width="{width}"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
 if png:pd.line((x1,y1,x2,y2),fill=color,width=max(1,int(width)))
def rect(x,y,w,h,fill,stroke='#526078',dash=False):
 S.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}"'+(' stroke-dasharray="6 4"' if dash else '')+'/>')
 if png:pd.rectangle((x,y,x+w,y+h),fill=fill if fill!='none' else None,outline=stroke)
def dim(x1,y1,x2,y2,label,tx,ty):
 line(x1,y1,x2,y2);line(x1-4,y1-4,x1+4,y1+4);line(x2-4,y2-4,x2+4,y2+4);txt(tx,ty,label,13)
txt(34,40,'T1-INTERLEAVED-C2 | proposed winding construction',24,True)
txt(34,64,'Engineering drawing / mm | source-derived regular geometry; exits, yokes and insulation require actual 3D acceptance',13)
txt(34,100,'A  Radial stack (radial thickness exaggerated)',17,True)
colors={'P':'#fbbf24','S':'#67e8f9','A':'#d8b4fe','T':'#cbd5e1'}
yy=130;scale=100
for k,(w,n,t) in enumerate(selected):
 hh=t*scale;rect(70,yy,300,hh,colors[w]);lab=f'{k+1:02d} '+(f'{w}: {n} turns' if n else f'1350F-1: {round(t/.077)} wrap(s)')+f' / {t:.3f}'
 txt(386,yy+hh/2+5,lab,13);yy+=hh
dim(48,130,48,yy,'',9,yy+23);txt(70,yy+28,'2.153 regular +0.077 one staggered seam = 2.230 max',13,True)
txt(70,yy+50,'No base wrap: bobbin all-path ground wall not yet verified.',12)
txt(70,yy+71,'P60 + P60 remain one continuous primary; no new pin.',12)
txt(660,100,'B  Axial winding/leadout allocation',17,True)
xx=730;top=148;px=23
rect(xx,top,band*px,160,'#e0f2fe');rect(xx-end*px,top,end*px,160,'#fef3c7');rect(xx+band*px,top,end*px,160,'#cffafe')
for j in range(61):line(xx+j*band*px/60,top+15,xx+j*band*px/60,top+50,'#b45309')
for j in range(16):line(xx+j*band*px/15,top+75,xx+j*band*px/15,top+125,'#0891b2',2)
dim(xx,top-20,xx+band*px,top-20,'13.8 active band',xx+95,top-27)
dim(xx-end*px,top+185,xx+(band+end)*px,top+185,'16.2 retained straight barrel',xx+45,top+207)
txt(xx-end*px-18,top+237,'P/A end pocket: 1.20',12);txt(xx+175,top+237,'S end pocket: 1.20',12)
txt(672,top+267,'P pitch 0.230 | A pitch 0.6273 | S pitch 0.920',12)
txt(672,top+287,'Spread winding cells across full band; do not close-pack S.',12)
txt(34,495,'C  Component-side terminal map / proposed finished envelope',17,True)
cx,cy,ps=260,670,10
rect(cx-150,cy-150,300,300,'none','#64748b',True)
rect(cx-125,cy-130,250,260,'#e2e8f0')
for pin in json.loads((P/'transformer-footprint/geometry-contract.json').read_text())['pads']:
 n=int(pin['number']);x,y=pin['at'];fill='#fbbf24' if n in [1,2,4,5] else '#67e8f9' if n in [6,10] else '#fff'
 rect(cx+x*ps-7,cy+y*ps-7,14,14,fill);txt(cx+x*ps-4,cy+y*ps+27,str(n),13,True)
txt(cx-91,cy+38,'CORE / YOKES: PRIMARY DOMAIN',11,True)
dim(cx-150,cy+168,cx+150,cy+168,'30 max allocation',cx-51,cy+190)
txt(458,550,'Selected recipe: P60 / 2T / A22 / T / S15 / T / S15 / T / P60 / T',13,True)
txt(458,580,'Minimum side screen: 2.50 - 2.230 - 0.05 - 0.05 = 0.170',13)
txt(458,610,'Regular shell: 17.56 x 11.36; proposed full envelope 30 x 30 x 18',13)
txt(458,640,'Bridge: continuous primary, parked only in P/A end pocket.',13)
txt(458,665,'Optional PIT-S tube: required ID >=0.25 / OD <=0.60; size unconfirmed.',12)
txt(458,692,'At Z=-7.50 +/-0.15, axial residual to pocket edges >=0.15.',12)
txt(458,718,'No extra bridge/crossover ridge over the 13.8 active band.',12)
txt(458,744,'CORE/YOKE/BARE-TERMINAL AND LEAD-EXIT AIR/SURFACE/SOLID',12,True)
txt(458,766,'PATHS ARE NOT ESTABLISHED BY THIS 2D RESERVATION.',12,True)
txt(458,795,'No inferred IEC spacing or test voltage; no supplier or process approval.',12)
txt(34,910,f'PS air-energy screen: baseline 74.25 uH -> selected {Lps*1e6:.2f} uH at declared sheet widths.',16,True)
txt(34,936,'20 uH remains a finished-transformer acceptance proposal, NOT a guaranteed result of the slab model.',14)
txt(34,963,'Unshared proposal only. No PCB / physical measurement / actual fresh STEP collision check / safety certification.',13)
S.append('</svg>');svg='\n'.join(S)+'\n';ET.fromstring(svg);(D/'construction.svg').write_text(svg,encoding='utf-8',newline='\n')
if png:png.quantize(colors=96).save(D/'construction.png',optimize=True)
print(json.dumps({'candidate':contract['id'],'selected_PS_uH':Lps*1e6,'baseline_PS_uH_10p5':cases[1]['leakage_H']['PS_Aopen']*1e6,'selected_PA_uH':matrixPA*1e6,'regular_build_mm':regular,'one_seam_build_mm':build,'side_remaining_mm':side,'end_pocket_mm':end,'DC110_W':hot['total_DC_equivalent_W'],'remaining_core_AC_W':available,'numerical_320_error_H':numerical[-1]['absolute_error_H'],'repository_input_hashes_and_external_pin_contract_checked':True,'material_source_bytes_checked':len(material_checked)},indent=2))

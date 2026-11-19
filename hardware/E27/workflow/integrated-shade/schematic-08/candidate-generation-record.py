from pathlib import Path
import json,hashlib,copy,collections,csv,shutil,itertools,math
R=Path(__file__).parent; ROOT=R/'Velluneo-2.0'; B=ROOT/'hardware/E27/variants/integrated-shade/SC07_protection'; S=ROOT/'hardware/E27/variants/integrated-shade/SC08_prototype'; W=ROOT/'hardware/E27/workflow/integrated-shade/schematic-08'; OUT=R.parent/'outputs'
S.mkdir(exist_ok=True);W.mkdir(exist_ok=True)
def save(p,d):p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
save(S/'owner-prototype-scope.json',{'approved_by':'Kamil','actual_answers':['Prototyp laboratoryjny do pomiarów','0–40°C; pomiary temperatur elementów na prototypie'],'question_item_ids':['request_user_input_async/call_7bfedf40c8d644cdaec63902814923fc/0','request_user_input_async/call_7bfedf40c8d644cdaec63902814923fc/1'],'evidence':'Actualsend_user_message_question_reply incurrentchat','scope':'Experimental laboratoryprototype,0..40Cambient,actualcomponenttemperaturesmeasuredonprototype','not_approved':['SC08newmap','Schematic/PCBstage','Ordering/manufacturingrelease','Energizedmains/surge/faulttests','Finishedlampqualification']})
parts=copy.deepcopy(json.loads((B/'bom-design.json').read_text(encoding='utf-8'))['components']);parts=[p for p in parts if p['ref'] not in ['L1','R1']];by={p['ref']:p for p in parts}
for p in parts:
 p['qualification']='SC08-B proposed experimental prototype; no capture/stage/release acceptance'
 p['pins']={k:('BUS_PLUS' if v=='RECT_PLUS' else 'MOS_GATE' if v=='PNP_BASE' else v) for k,v in p['pins'].items()}
by['RF1']['pins']['2']='AC_MID'
rf=copy.deepcopy(by['RF1']);rf.update(ref='RF2',pins={'1':'AC_MID','2':'AC_FUSED'},notes='Second series fusible220ohm2W; both pulse and continuous heat must be qualified. No saturated input coil.');parts.append(rf)
by['RF1']['notes']='One of two series220ohm2W fusible resistors; total440ohm. Input dissipation penalty is explicit.'
by['U1']['pins']['4']='DRAIN_BLOCKED'
di=copy.deepcopy(by['D1']);di.update(ref='D4',kind='D',mpn='STTH110A',value='1000V1A blocking',pins={'1':'DRAIN_BLOCKED','2':'BUS_PLUS'},pin_types={'1':'passive','2':'passive'},source='https://www.st.com/resource/en/datasheet/stth110.pdf',footprint='Diode_SMD:D_SMA',notes='ST SMA pin1cathode toU1DRAIN; pin2anode toBUS_PLUS. Blocks reverse drain current into input. New exact geometry/pin verification due before native capture.');parts.append(di)
by['D3'].update(mpn='1.5KE440A-E3/54',value='376Vstandoff TVS',source='https://www.vishay.com/docs/88301/15ke.pdf',footprint='Diode_THT:D_DO-201AD_P15.24mm_Horizontal',notes='Cathode BUS_PLUS/anodeDC_RETURN. Secondary clamp only; conditionalhotTVSmodel is not guaranteedVc. Independent scalarRCsurge bound assumesTVSopen. Exact footprint geometry review due.')
by['Q2'].update(kind='PMOS',mpn='PMV65XP,215',value='P-MOS20V',pins={'1':'MOS_GATE','2':'VCC_OV','3':'OPTO_DRIVE'},pin_types={'1':'input','2':'passive','3':'passive'},source='https://assets.nexperia.com/documents/data-sheet/PMV65XP.pdf',notes='Physical1G2S3D; maxRDSon105mohm atVGS−4.5V,Tj150C removesPNPsaturation budget. Hot switching time still requires correlation.')
by['C4'].update(mpn='CL32B226KAJNNNE',value='22uF25VX7R',source='https://product.samsungsem.com/mlcc/CL32B226KAJNNN.do',footprint='Capacitor_SMD:C_1210_3225Metric',notes='One of two parallel nonpolar22uF25VX7R1210. CombinedCeff≥18uF proposed acceptance; supplierbias/agingmin not guaranteed by an invented reserve.')
c=copy.deepcopy(by['C4']);c.update(ref='C10');parts.append(c)
for ref in ['R10','R11','R12','R24','R25','R28']:
 by[ref].update(mpn='CRCW2512715RFKEGHP',value='715ohm1.5WHP',notes='Oneofsixfeed715R;localambientmax90C,not100C. Hotpowerrecalculatedwithoneothershorted.')
by['R23'].update(mpn='RC0805FR-074K3L',value='4k3',notes='Pull-downlimitsPMOS100uAhotOFFleakage; includesdividerinjection and5uAengineeringreserve. MustverifyactualOFFVGSandOPTO_DRIVE.')
by['R22'].update(mpn='TNPW1206210KBYEA',value='210k0.1%10ppm',notes='Recomputedhysteresis forPMOSrail; preserveconditionalretrybelow25Hz.')
by['R2']['notes']='28.7ohm initial population only. CandidateE96trim22.1..31.6ohm requires unpowered replacement and controlled engineering change; calibrate55mA then verifyline/temperature. No fulltempaccuracy claim.'
save(S/'bom-design.json',{'revision':'SC08-B','status':'Independent proposed change map; no new CAD, no owner approval','components':parts})
shutil.copy2(R/'sc08-hot-research/hot-prototype-recommendation.json',S/'hot-research.json')
for n in ['input-results.json','input_screen.py']:
 if (R/'sc08-input-research'/n).exists():shutil.copy2(R/'sc08-input-research'/n,S/n)
shutil.copy2(R/'sc08-current-research/research.md',S/'current-research.md')
shutil.copy2(R/'sc08-current-research/trim_sensitivity.py',W/'historical-SC07-trim-source.py')
shutil.copy2(R/'sc08-current-research/trim-results.json',S/'historical-SC07-trim-results.json')
shutil.copy2(R/'sc08-input-research/proposal.md',S/'input-research.md')
g=.003; rlo=.99*.97;rhi=1.01*1.03
def bounds(vs,ds):
 vals=[v*(1+t/b+t/h)-d*t/h+ib*t for v,t,b,h,d,ib in itertools.product(vs,[320000*(1-g),320000*(1+g)],[1000*(1-g),1000*(1+g)],[210000*(1-g),210000*(1+g)],ds,[-15e-9,15e-9])]
 return [min(vals),max(vals)]
rise=bounds([.396,.404],[0,.5]);fall=bounds([.387,.400],[11.397,12.9]);window=rise[0]-fall[1]
rail=[11.4,12.9];feed=4290
loads={'two_LED_zeroVF_A':2*rail[1]/(1780*rlo),'gate_divider_A':rail[1]/(21000*rlo),'OPTO_pulldown_A':rail[1]/(4300*rlo),'hysteresis_A':rail[1]/(210000*.997),'rail_divider_A':rail[1]/(48300*.9965),'U2_reference_reserve_A':19.5e-6}
feedmin=(fall[0]-rail[1])/(feed*rhi); loadmax=sum(loads.values())
off=(145-rail[0])/(feed*rlo)+2*145/(56000*rlo)+145/(321000*.997)+.00145
vgsmin=(rail[0]-.4)*(10000*rlo)/(11000*rhi+10000*rlo);vgsmax=rail[1]*(10000*rhi)/(11000*rlo+10000*rhi)
u3p=(145-rail[0])/(5*715*rlo)*rail[1]
calc={'revision':'SC08-B','evidence_kind':'Calculated proposal; not physical measurements or manufacturerfulltempguarantee','OVP':{'rise_V':rise,'fall_V':fall,'window_min_V':window,'rail_acceptance_V':rail,'off_drive_budget_V':[0,.5],'on_drive_budget_V':[11.397,12.9]},'auxiliary':{'loads_upper_A':loads,'feed_min_A':feedmin,'remaining_U3_A':feedmin-loadmax,'required_min_A':.001,'feed_each_145V_mixed_normal_W':(145-rail[0])**2*(715*rhi)/(715*(rhi+5*rlo))**2,'feed_each_one_feed_short_W':(145-rail[0])**2*(715*rhi)/(715*(rhi+4*rlo))**2,'allowed_each_90C_W':1.5*65/85,'U3_one_feed_short_power_upper_W':u3p,'U3_Tj_at_local80C_theta85_C':80+85*u3p,'local_ambient_design_condition_C':80},'Q2':{'VGS_magnitude_V':[vgsmin,vgsmax],'RDSon_hot_max_ohm':.105,'Vdrop_20mA_V':.02*.105,'drop_budget_V':.003,'max_gate_rating_V':12,'off_node_max_V_at_VGS0':(100e-6+.404/(210000*.997)+5e-6)*4300*rhi,'off_leakage_basis':'ManufacturerIDSS100uAat150C,VGS0;5uAreserve;actualgateoffstatevalidationstillrequired','min_LED_A':(rail[0]-.003-1.5)/(1780*rhi),'max_LED_short_resistor_W':rail[1]**2/(1780*rlo),'allowed_LED_R125C_W':.5*30/85},'retry':{'discharge_current_upper_A':off,'minimum_off_s':120e-6*window/off,'frequency_upper_Hz':off/(120e-6*window),'conditional_on':'Actualshutdown andspecifiedrail/thresholdbounds'},'samplehold':{'combined_nominal_F':44e-6,'combined_budget_F':44e-6*.9*.85*.8*.7,'prototype_Ceff_required_F':18e-6,'required_at_trim_min_F':20/(62000*22.1*.99),'manufacturer_DC_bias_min_verified':False,'note':'0.8agingand0.7biasareengineeringreserves,notmanufacturerlimits; effectivecapmeasurementneeded'},'reconnection':{'Cout_fault_V':145,'Cmax_F':180e-6,'stored_energy_J':.5*180e-6*145**2,'R7min_ohm':470*.95*.97,'healthy60V_initial_A':(145-60)/(470*.95*.97),'one_LED_short58V_initial_A':(145-58)/(470*.95*.97),'zeroV_current_upper_A':145/(470*.95*.97),'R7_normal55mA_W':.055**2*470,'R7_at90mA_Rmax_W':.09**2*470*1.05*1.03,'warning':'145Vand60/58Vfloorsconditional. NeitherR7pulse/continuousfaultheatnorLEDThermalratingclosedbythiscalculation.'},'closure':{'genuinely_addressed':['PMOS hotonresistance replaces unsupportedPNPsaturationassumption','InputL1andR1removed so their resonance/saturationmechanismdoesnotexist','Addedblockingdiodeaddressesreversecurrentpath','ExplicitinputRC/surgeandoutputenergybounds calculated','Largerhotter-ratednonpolarCFBproposal'], 'not_closed':['Hotactuator timing andcomplete.6msshutdown requiremeasurement','Ceff≥18uF supplierorbenchcorrelation','Peakcurrent≤.7A andtemperature/line/currenttrim qualification','RF/R7pulseandcontinuousfaultheat, thermalboard design','Actualsurge/EMC/optics/safetyanddomainqualification'],'no_PCB_or_order_approval':True}}
save(S/'recalculate-design.py',{}) if False else None
save(S/'calculated-control.json',calc)
save(S/'source-basis.json',{'revision':'SC08-B','base_commit':'a6c7ed424a6aa882ef7e5b46899955d3d928f09d','basis':'Independently prepared from approvedSC07map and primarydatasheets before CAD; proposedexperimentalchange, not approved','baseline_files':[{'path':p.relative_to(ROOT).as_posix(),'sha256':sha(p)} for p in [B/'bom-design.json',B/'intended-connectivity.json',B/'requirements.json']], 'scope_input':{'path':'owner-prototype-scope.json','sha256':sha(S/'owner-prototype-scope.json')},'calculation_inputs':[{'path':p.name,'sha256':sha(p)} for p in [S/'calculated-control.json',S/'input-results.json']],'primary_sources':[{'url':p['source'],'part':p['mpn']} for p in [by['Q2'],by['C4'],by['D3'],di]],'changed_fields_invalidate_SC07_capture_approval':True})
nets=collections.defaultdict(list);nc=[];rows=[]
for p in parts:
 for pin,net in p['pins'].items():
  rows.append({'ref':p['ref'],'pin':pin,'net':net or 'NC','mpn':p['mpn']})
  if net is None:nc.append({'ref':p['ref'],'pin':pin,'reason':'Unusedcomparatoroutput;definedinputretained'})
  else:nets[net].append({'ref':p['ref'],'pin':pin})
intent={'schema_version':1,'revision':'SC08-B','basis':'Independent proposedphysicalpinmap before newCAD. SC07 approval not reused.','basis_sources':[{'path':p.name,'sha256':sha(p)} for p in [S/'source-basis.json',S/'bom-design.json']],'components':[{'ref':p['ref'],'units':[{'name':'A','pins':list(p['pins'])}]} for p in parts],'nets':[{'id':n,'pins':ps} for n,ps in sorted(nets.items())],'no_connects':nc,'barriers':[],'approval':None};save(S/'intended-connectivity.json',intent)
digest=hashlib.sha256(json.dumps({k:v for k,v in intent.items() if k!='approval'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
for name,data,fields in [('Velluneo_SC08_polaczenia.csv',rows,['ref','pin','net','mpn']),('Velluneo_SC08_czesci.csv',[{k:p[k] for k in ['ref','value','mpn','footprint','source']} for p in parts],['ref','value','mpn','footprint','source'])]:
 with (OUT/name).open('w',encoding='utf-8-sig',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(data)
shutil.copy2(OUT/'Velluneo_SC08_polaczenia.csv',S/'physical-pin-intent.csv')
save(W/'task-contract.json',{'task':'SC08 bounded prototype electrical corrections','base_commit':'a6c7ed424a6aa882ef7e5b46899955d3d928f09d','writer':'/root','authorized_human':'Kamil','branch':'concept/integrated-shade-nonisolated-buck','scope':'Prepare exact reviewed component/map corrections and explicit laboratoryprototypevalidation criteria. Do not promote conditional calculations to qualification.','allowed_paths':[S.relative_to(ROOT).as_posix()+'/**',W.relative_to(ROOT).as_posix()+'/**'],'actual_owner_scope':'owner-prototype-scope.json:Laboratoryprototype0..40Cambient;localhotspotlimitsseparate','requirements_affected':['REQ-POWER','REQ-FAULT','REQ-PARTS','REQ-MAINS','REQ-ENV','REQ-SAFETY','REQ-INTERFACE'],'main_and_SC07_unchanged':True,'no_new_CAD_before_actual_new_map_approval':True})
save(W/'intent-status.json',{'revision':'SC08-B','intent_digest':digest,'components':len(parts),'pins':len(rows),'nets':len(nets),'NC':len(nc),'approval':None,'native_CAD':False,'PCB':False})
print(json.dumps({'components':len(parts),'pins':len(rows),'nets':len(nets),'digest':digest,'feed_shunt_A':feedmin-loadmax,'retry_Hz':calc['retry']['frequency_upper_Hz'],'U3_Tj_conditional':80+85*u3p}))

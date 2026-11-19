from pathlib import Path
import json,math,itertools,sys,hashlib,shutil
ROOT=(Path(__file__).resolve().parents[5] if Path(__file__).parent.name=='SC06_driver' else Path(__file__).parent/'Velluneo-2.0');S=ROOT/'hardware/E27/variants/integrated-shade/SC06_driver';W=ROOT/'hardware/E27/workflow/integrated-shade/schematic-06';OUT=ROOT.parent.parent/'outputs'
def save(p,j):p.write_text(json.dumps(j,ensure_ascii=False,indent=2,allow_nan=False)+'\n',encoding='utf-8')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
# Independent component-error screen: .1% initial +.1%100K TCR +.1%agingreserve.
e=.003;top=[320000*(1-e),320000*(1+e)];bot=[1000*(1-e),1000*(1+e)];hy=[330000*(1-e),330000*(1+e)]
def trip(vth,vdrive):
 return [v*(1+a/b+a/c)-a*d/c+i*a for v,a,b,c,d,i in itertools.product(vth,top,bot,hy,vdrive,[-15e-9,15e-9])]
rise=trip([.396,.404],[0,.5]);fall=trip([.387,.400],[11.35,12.38])
vlo,vhi=min(rise),max(rise);flo,fhi=min(fall),max(fall)
cmin=150e-6*.8;cmax=150e-6*1.2;rrlo=470*.95*.97;rrhi=470*1.05*1.03
feedlo=10000*.99*.97;feedhi=10000*1.01*1.03
bleedlo=56000*.99*.97;bleedhi=56000*1.01*1.03
currentoff=135/feedlo+2*135/bleedlo+135/(321000*.997)+.00145
window=vlo-fhi;toff=cmin*window/currentoff
r={'revision':'SC06-B','kind':'Calculatedengineeringacceptanceproposal,notSPICE/measurement/certification',
 'OVP':{'rising_v':[vlo,vhi],'falling_v':[flo,fhi],'independent_window_min_v':window,'resistor_error_each':e,'basis':'TLV6700rise396..404mV,fall387..400mV;inputbias+/-15nA;OFFcollector0..0.5V/ON11.35..12.38Vareproposedverifiedlimits;agingreserve.1%isengineeringbudget','rail_v':[11.65,12.38],'rail_precision_requires_ika_min_ma':1,'startup_and_temperature':'Relay/BJTtiminganddropsnotguaranteedfulltemperature;qualifylocalPhotoMOSambient<=85C'},
 'auxiliary':{'feed_each_ohm':2000,'count':5,'feed_each_max_w':(135-11.65)**2/(feedlo*5),'each_allowed125c_w':(155-125)/(155-70),'at112v_min_feed_ma':(112-12.38)/feedhi*1000,'upper_load_ma_screen':8.05,'remaining_shunt_bias_ma':(112-12.38)/feedhi*1000-8.05,'nominal_120v_feed_ma':(120-12.075)/10000*1000,'nominal_output_current_for55led_120v_ma':55+(120-12.075)/10000*1000+2*120/56000*1000+120/321000*1000,'capacitor_leakage_max_ma':1.45,'note':'ThefeedalreadyincludesLEDdrive/shunt/lowvoltageloadpower;donotaddthemagaintototaloutputpower.'},
 'normal_headroom':{'healthy_load_vmax':84.5,'LED_average_max_ma':60.5,'total_load_max_ma_requirement':80,'Cmin_f':cmin,'full10ms_droop_v':.08*.01/cmin,'peak_requirement_screen_v':84.5+.0605*rrhi+.08*.01/cmin,'basis':'Loadvoltage/currentupperlimitsareacceptanceinputsrequiringqualification;full10msdroopisaconservativereserve,notapredictedwaveform.'},
 'output_energy':{'Cmax_f':cmax,'Vmax_requirement':135,'energy_j':.5*cmax*135**2,'RINS_min_ohm':rrlo,'healthy60v_peak_a':(135-60)/rrlo,'one_short58v_peak_a':(135-58)/rrlo,'entire_short_peak_a':135/rrlo,'entire_short_peak_w':135**2/rrlo,'RINS_nominal55mA_w':.055**2*470,'RINS_max60p5mA_w':.0605**2*rrhi,'pulse_qualification':'AC05roomtemperature50W5stestonlycomparisonscreen;hot/repetitivepulseandcontinueddriverenergyremainqualification.'},
 'passive_discharge':{'bleeders_parallel_ohm_nominal':28000,'each_max135v_w':135**2/bleedlo,'normal135_to5_s':cmax*bleedhi/2*math.log(135/5),'one_open135_to5_s':cmax*bleedhi*math.log(135/5),'target_one_open_s':40,'assumptions':'ACremoved,nootherenergysource;remainingbleedercontinuous;notcertifiedaccessiblecontactlimit;capleakage/auxdrainignoredtoconservativelylengthentime.'},
 'BP_shutdown':{'series_ohm_min':100*.99*.97,'CBP_max_assumed_f':120e-9,'BP_initial_max_v':6.10,'initial_current_bound_a':6.1/(100*.99*.97),'CBP_energy_j':.5*120e-9*6.1**2,'BP_charge_current_max25c_a':.0075,'steady_BP_positive_bound_v':.0075*(100*1.01*1.03+1.25),'UV_boundary_min_derived_v':5.55-1.2,'note':'RemovedD2/SCRBP-to-groundpath,positiveBPclamp. HotrelayRonandBPchargingcurrentaretestinputs,notrelabeled25Cguarantees.'},
 'open_load_retry':{'off_drain_max_a':currentoff,'off_interval_min_s':toff,'frequency_upper_hz':1/toff,'frequency_target_hz':25,'conditions':'SuccessfulBPshutdown,Cmin120uF,noviableLEDload;includesCmaxleakageinIoff. InternalTLVminimumhysteresisnotassumed.'},
 'dynamic_acceptance_screen':{'trip_max_v':vhi,'current_peak_required_bound_a':.7,'shutdown_required_latency_s':.0006,'delta_v_constantcurrent':.7*.0006/cmin,'residualL_energy_j':.5*.003*.7**2,'peak_energy_bound_v':math.sqrt((vhi+.7*.0006/cmin)**2+(.003*.7**2)/cmin),'requirement_v':135,'status':'Conditionalengineeringbudget;requiresactualdelay/currentvalidation. Relay.5msis25Ctest,notfulltemperaturereleaseproof.'},
 'input':{'Vac_max':253,'normal_peak_v':253*math.sqrt(2),'RF220_min_ohm':220*.95*.97,'declared_surge_source_peak_v':1000+253*math.sqrt(2),'TVS_min_breakdown25c_v':447,'TVS_upper_clamp25c_v':648,'source_current_upper_screen_a':(1000+253*math.sqrt(2)-447)/(220*.95*.97),'TVS_characterized_current_a':7.7,'RFrough_model_w':.8,'RFrough_model_basis':'Ownlimited220ohm/lumped430nFsource,3mH/Rsense33.2ohm,110–123Voutput/207–253VAC:0.75–0.79W;round0.8W.Notactualpifilterthermalqualification.','not_proven':['TVShotclamp/parasiticringingbelow700V','RFimpulse/fusingandRMS/temperature','Inductorinsulationandinrush','EMC/PF/wholeproductstandards'],'C1rated_at100c_v':2000*(1-.0125*15),'C2rated_at100c_v':1000*(1-.0125*15)}}
r['checks']={'normal_screen_below123':r['normal_headroom']['peak_requirement_screen_v']<123,'each_aux_below125c_derating':r['auxiliary']['feed_each_max_w']<r['auxiliary']['each_allowed125c_w'],'shunt_bias_at112_ge1ma':r['auxiliary']['remaining_shunt_bias_ma']>=1,'bleeder_one_open_below40s':r['passive_discharge']['one_open135_to5_s']<40,'bleeder_each_below125c_derating':r['passive_discharge']['each_max135v_w']<(155-125)/(155-70),'conditional_retry_below25hz':1/toff<25,'conditional_dynamic_below135':r['dynamic_acceptance_screen']['peak_energy_bound_v']<135}
save(S/'electrical-calculations.json',r)
# Humanreadablepre-capturepresentationisnotanativeKiCadschematic.
svg='''<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="840" viewBox="0 0 1400 840"><rect width="1400" height="840" fill="#f1f4f7"/><style>text{font-family:Arial,sans-serif;fill:#19334a} .h{font-size:30px;font-weight:bold}.t{font-size:21px}.s{font-size:18px}.b{fill:white;stroke:#46657e;stroke-width:2}.w{stroke:#376b83;stroke-width:3;fill:none;marker-end:url(#a)}</style><defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto"><path d="M0 0L8 3L0 6" fill="#376b83"/></marker></defs><text x="40" y="55" class="h">Velluneo SC06-B — plan polaczen przed schematem KiCad</text><text x="40" y="95" class="t">Zasilacz 230 V / 50 Hz | kondensator w bazie | bez zalozonego obrysu obudowy</text>'''
def block(x,y,w,h,title,lines):
 global svg
 svg+=f'<rect class="b" x="{x}" y="{y}" width="{w}" height="{h}" rx="8"/><text x="{x+15}" y="{y+32}" class="t">{title}</text>'
 for i,line in enumerate(lines):svg+=f'<text x="{x+15}" y="{y+65+i*25}" class="s">{line}</text>'
block(40,145,260,150,'Wejscie i filtr',['RF1 220 ohm, mostek','C1 100 nF / 2 kV','L1 10 mH, C2 330 nF','TVS na szynie DC'])
block(365,145,295,150,'Przetwornica buck',['LYT0006D-TL','L2 + L3 = 3 mH','R2 = 33,2 ohm','D1 SiC 1200 V'])
block(735,145,250,150,'Kondensator w bazie',['C5 150 uF / 160 V','2 x 56 kohm rownolegle','Cel: ponizej 40 s do 5 V','takze przy 1 przerwie'])
block(1060,145,300,150,'Wyjscie LED',['R7 470 ohm / 5 W','Panel okolo 55 mA','Propozycja 30 LED w szeregu','Wyjscie odniesione do sieci'])
for a,b in [((300,215),(365,215)),((660,215),(735,215)),((985,215),(1060,215))]:svg+=f'<path class="w" d="M{a[0]} {a[1]} L{b[0]} {b[1]}"/>'
block(735,390,335,145,'Pomiar przepiecia',['TLV6700 + precyzyjny dzielnik','Regulowane zasilanie okolo 12 V','Zewnetrzna histereza','Automatyczne ponowne wlaczenie'])
block(365,390,295,145,'Wylaczenie sterownika',['PhotoMOS AQY221R2VY','BP polaczone z SOURCE','przez R6 100 ohm','Bez zwarcia BP do masy'])
svg+='<path class="w" d="M860 295L860 390"/><path class="w" d="M735 460L660 460"/><path class="w" d="M510 390L510 295"/>'
svg+='<text x="40" y="615" class="t">Usuniety poprzedni tor SCR / D2: nie prowadzimy impulsu kondensatora przez pin BP.</text><text x="40" y="660" class="t">To mapa do zatwierdzenia. Nie jest schematem KiCad, projektem PCB ani dokumentacja produkcyjna.</text><text x="40" y="705" class="s">Ostateczna kwalifikacja wymaga sprawdzenia startu, temperatur, impulsow i zachowania przy uszkodzeniu elementu.</text><text x="40" y="750" class="s">BOM i pelna tabela fizycznych pinow sa dolaczone. Main pozostaje bez zmian.</text></svg>'
(OUT/'Velluneo_SC06_plan.svg').write_text(svg,encoding='utf-8');shutil.copy2(OUT/'Velluneo_SC06_plan.svg',S/'capture-plan.svg')
print(json.dumps({'checks':r['checks'],'OVP':r['OVP'],'retry':r['open_load_retry'],'normalpeak':r['normal_headroom']['peak_requirement_screen_v'],'dynamic':r['dynamic_acceptance_screen']['peak_energy_bound_v']},indent=2))

assert all(r["checks"].values()), "A declared engineering screen failed"

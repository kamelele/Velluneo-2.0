from pathlib import Path
import sys,ast,json,hashlib,math,itertools,csv
W=Path(__file__).resolve().parent;sys.path[:0]=[str(W/'led19-libs'),str(W/'python-libs'),str(W/'cam-libs')]
import fitz,numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
R=W/'Velluneo-readiness';P=R/'hardware/E27/workflow/specification-reset';D=P/'led-compatibility-19';D.mkdir(exist_ok=True)
source=W/'led19-sources/cree2835-current.pdf';maker_sha=hashlib.sha256(source.read_bytes()).hexdigest();assert maker_sha=='74d4261952c25e6833212a82b0f72e759f8297478627a368f4acff22378c92c8'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(n,j):(D/n).write_text(json.dumps(j,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def txt(n,s):(D/n).write_text(s,encoding='utf-8')
inputs=['catalogue-pcb-16/calculations.json','catalogue-pcb-16/design/Velluneo_driver.kicad_pcb','catalogue-pcb-16/design/proposed-parts.json','electrical-integration/native-typical-flux-curve.json','electrical-refinement/optics/results.json','compact-60/led-heat/results.json','compact-60/led-heat/calculate.py','requirements-and-plan.md']
binding={x:sha(P/x)for x in inputs}
for n in ast.parse((P/'compact-60/led-heat/calculate.py').read_text()).body:
 if isinstance(n,ast.FunctionDef)and n.name=='points':exec(compile(ast.Module(body=[n],type_ignores=[]),'nativecurvehelper','exec'))
doc=fitz.open(source);draw=doc[5].get_drawings();rect=draw[18]['rect'];pts=points(draw[23]);v=2.6+(pts[:,0]-rect.x0)/rect.width*.6;i=(rect.y1-pts[:,1])/rect.height*.480;order=np.argsort(i);i=i[order];v=v[order]
curve=json.loads((P/'electrical-integration/native-typical-flux-curve.json').read_text());assert curve['source_sha256']==maker_sha;fc=np.array(curve['samples'])
def phi(a):
 assert fc[0,0]<=a*1000<=fc[-1,0];return float(np.interp(a*1000,fc[:,0],fc[:,1]))
def vf(a,t=85):
 assert i[0]<=a<=i[-1];return float(np.interp(a,i,v))-.0009*(t-25)
driver=json.loads((P/'catalogue-pcb-16/calculations.json').read_text());currents=[driver['normal']['output_screen_min_a'],driver['normal']['output_nom_a'],driver['normal']['output_screen_max_a']]
assert currents[1]==.319
parts={'H27':dict(mpn='JB2835BWT-G-H27GA0000-N0000001',CCT_K=2700,CRI_test_min=80,phi25=29.1,phi85=27.2,old_count=8),'H40':dict(mpn='JB2835BWT-G-H40GA0000-N0000001',CCT_K=4000,CRI_test_min=80,phi25=32.1,phi85=30.,old_count=7),'H65':dict(mpn='JB2835BWT-G-H65GA0000-N0000001',CCT_K=6500,CRI_test_min=80,phi25=32.,phi85=29.9,old_count=7),'U40':dict(mpn='JB2835BWT-G-U40GA0000-N0000001',CCT_K=4000,CRI_test_min=90,phi25=27.6,phi85=25.8,old_count=None)}
tau=.87
def flux(key,n,a,ref=85,transmission=tau):return n*parts[key]['phi85'if ref==85 else'phi25']*phi(a)*transmission
def freq(r,out):return .329*4*(out+1.7)*r*1.021/(.0011*.9*.715**2)
def model(key,n,a,t=85):
 out=n*vf(a,t);pe=out*a;return dict(key=key,MPN=parts[key]['mpn'],count=n,current_A=a,junction_reference_C=t,per_LED_Vf_typ_V=vf(a,t),panel_voltage_typ_V=out,per_LED_electrical_typ_W=pe/n,panel_electrical_typ_W=pe,flux_typ_model_lm=flux(key,n,a,ref=85),flux_reference='85C manufacturer reference times25C currentcurve, assumedseparable; tau.87',within_19to22_typ=19<=out<=22,within_750to850_typ=750<=flux(key,n,a)<=850,aux_VDD_low_screen_V=(out+.5)*10/18-1,frequency_screen_Hz=freq(1.8,out))
rows=[model(k,n,a,t)for k,n,a,t in itertools.product(parts,[6,7,8],currents,[10,25,85,105,115])]
nom={k:model(k,parts[k]['old_count']or 7,.319)for k in parts}
old=[nom[k]['flux_typ_model_lm']for k in ['H27','H40','H65']]
u=[model('U40',7,a)for a in currents];h=[model('H40',7,a)for a in currents]
thermal=[]
for a,tsp,rjs in itertools.product(currents,[75,85,95,105],[7.6,15.]):
 # Tsp input is an assumed measured solderpoint, not ambient or predicted case.
 pe=a*vf(a,85);thermal.append(dict(current_A=a,assumed_solderpoint_C=tsp,R_junction_solder_K_per_W=rjs,LED_electrical_model_W=pe,Tj_no_optical_credit_C=tsp+pe*rjs,Rjs_is_typical_or_hypothetical='7.6makerTYPICAL;15engineeringallowanceNOTmakerbound'))
counts=[dict(count=n,voltage_range_typ_V=[min(n*vf(a,t)for a,t in itertools.product(currents,[10,25,85,105,115])),max(n*vf(a,t)for a,t in itertools.product(currents,[10,25,85,105,115]))],aux_VDD_min_screen_V=min((n*vf(a,t)+.5)*10/18-1 for a,t in itertools.product(currents,[10,25,85,105,115])))for n in [6,7,8]]
trim=[]
for r in [2.21,2.26]:
 a=.319*.9*4/(2*r);out=7*vf(a);trim.append(dict(R9_ohm=r,current_A=a,H40_7_model_lm=flux('H40',7,a),panel_voltage_typ_V=out,frequency_conservative_screen_Hz=freq(r,out),frequency_screen_below120k=freq(r,out)<120000,scope='UNADOPTED diagnostic. R9-only substitution cannot be approved from optical calculation: frequency/operatingbias/currentloop/startup recheck required.'))
sens=[dict(transmission=tt,relative_stabilized_gain=gg,current_A=a,U40_7_model_lm=flux('U40',7,a,transmission=tt)*gg)for tt,gg,a in itertools.product([.80,.87,.90],[.90,1.,1.10],currents)]
voltage_sens=[dict(current_A=a,Tj_C=t,assumed_extra_Vf_per_LED=delta,panel_V=7*(vf(a,t)+delta))for a,t,delta in itertools.product(currents,[10,85,115],[0.,.13,.20])]
result=dict(scope='LED19 analytical compatibility assessment, not CAD change, measured qualification, final LED selection or manufacturing release',source_commit='7f4b7781f2178af5a57d42212a02ac1996ffcd2a',maker_SHA256=maker_sha,maker_revision='CLJ-DS40 Rev10B',parts=parts,driver_current_A=dict(nominal=currents[1],conditional_screen_min=currents[0],conditional_screen_max=currents[2],eta_assumed=.9,not_measured_or_full_bounds=True),assumptions=['Nominal19..22V driverloadallocation, not testedcompliancerange','Flux85C reference and25C relativecurrentcurve assumedseparable','Diffusertransmission.87 unmeasured','No upperfluxbin guaranteed byMPN; minimumflux at55mA not a guaranteed hot/highcurrentminimum','125CabsoluteTj and480mAabsoluteDC requirederating; notlifetimeratings','No transfer of80CRI spectrum to90CRI; thermal uses noopticalcredit','CCT/CRI at319mA andwarm/coldreelvoltage spread notqualified'],original_family_nominal=nom,original_family_ratio=max(old)/min(old),H40_7_current_screen=h,U40_7_current_screen=u,voltage_count_comparison=counts,thermal_solderpoint_scenarios=thermal,derating_example=dict(source='Cree p4 Rja40K/Wexample, linear64C480mA to105C180mA',allowed_mA_at85C_ambient=480-(85-64)*(480-180)/(105-64),ambient_threshold_C_at_currentmax=64+(480-currents[2]*1000)*(105-64)/(480-180),not_actual_lamp_Rja=True),R9_only_diagnostic_not_ECO=trim,U40_flux_sensitivities=sens,voltage_spread_sensitivities=voltage_sens,U40_7_nominal_flux25C_reference_lm=flux('U40',7,.319,ref=25),U40_7_tau_interval_all_three_conditional_currents=[750/(7*25.8*phi(currents[0])),850/(7*25.8*phi(currents[2]))],model_checks=dict(H40_7_above850_at_nominal=nom['H40']['flux_typ_model_lm']>850,U40_7_inside_band_all_declared_current_screen=all(x['within_750to850_typ']for x in u),six_LED_aux_screen_below9p45=counts[0]['aux_VDD_min_screen_V']<9.45,eight_LED_above22_typ=counts[2]['voltage_range_typ_V'][0]>22,R9_only_frequency_not_closed=all(not x['frequency_screen_below120k']for x in trim)),decision='OriginalH40x7 is electrically plausible but nominally too bright for 750..850lm atC16current; NOT a finalpairing. CandidateU40x7 (4000K,90CRIclass) fits nominalflux/current/voltage screens without changingdriver, but bin/diffuser/thermal/actualvoltage/startup/CCT/CRI andsourcing/assembly needconfirmation. Noautomaticpartsubstitution orproductionrelease.')
result['assumptions'].append('DC/average-current model; actual LED ripple, transient peaks and PstLM/SVM not characterized.')
result['decision']='H40x7 is electrically plausible but exceeds850lm under oldtau.87 hypothesis. Retain it as firstverificationcandidate due knownJLCroute and characterize opticalgain; do not blindlychangeR9. U40x7 is optional90CRIcomparison, not approvedsubstitution: nominalfits but upperdeclaredcurrent exceeds850lm atsame.87tau. Exactbin/diffuser/thermal/voltage/startup/current/CCT/CRI remain unqualified. NoCAD/manufacturingchange.'
optical_targets={}
for key in ['H40','U40']:
 tt=tau*800/nom[key]['flux_typ_model_lm']
 optical_targets[key]=dict(assumed_tau_for800_at_nominal=tt,tau_interval_for750to850_all_three_currentpoints=[750/(7*parts[key]['phi85']*phi(currents[0])),850/(7*parts[key]['phi85']*phi(currents[2]))],model_lm_at_target_tau=[flux(key,7,a,transmission=tt)for a in currents],not_selected_or_measured=True,limits='Only an allocated total stabilized opticalgain under typicalbin/Tj85C hypotheses; not a chosen diffuser or guaranteedacceptance. LEDgainspread, drivereta and actualTj unmeasured.')
result['optical_throughput_diagnostics_not_selected']=optical_targets
prior=json.loads((P/'electrical-refinement/optics/results.json').read_text());oldi=prior['minimax_nominal_family_current_A']
assert abs(flux('H40',7,oldi)-prior['nominal_family_lm_at_minimax_current']['4000'])<1e-9
oldheat=json.loads((P/'compact-60/led-heat/results.json').read_text());assert abs(vf(oldi)-oldheat['family_typical']['4000']['Vf85_typical_V'])<1e-12
assert abs(freq(1.8,22)-driver['normal']['frequency_22v_conservative_hz'])<1e-8
assert len(rows)==180 and all(math.isfinite(x['panel_voltage_typ_V'])for x in rows)
result['numerical_verification']=dict(prior_optical_model_replayed=True,prior_native_voltage_replayed=True,C16_frequency_equation_replayed=True,finite_screen_rows=180,interpretation='Numericalverification passes; engineering compatibility observations include failures.')
result['historical_band_diagnostics']=result.pop('model_checks')
result['owner_decision']=dict(date='2026-11-21',verbatim='jak będzie wiecej lumenów to nie problem',evidence='Actual owner message in this conversation; no permanent message URL available',accepted_scope='850lm is no longer a rejection ceiling. Preserve750lm minimum, first4000K, other CCT/family/thermal/electrical/insulation/life requirements. Not approval of CAD, manufacturing or measured performance.')
result['current_assessment']=dict(first_panel='7series JB2835BWT-G-H40GA0000-N0000001',driver='Unchanged C16 R9=1.80ohm, nominal319mA',nominal_DC_voltage_model_in_allocation=nom['H40']['within_19to22_typ'],typical_19to22V_over_declared_current_temperature_grid=19<=counts[1]['voltage_range_typ_V'][0]and counts[1]['voltage_range_typ_V'][1]<=22,minimum750lm_at_declared_currentpoints_oldtau0p87=all(x['flux_typ_model_lm']>=750 for x in h),higher_flux_is_not_a_rejection=True,DC_current_below480mA_absolute_ceiling_only=max(currents)<.480,thermal_performance_measured=False,actual_LED_peak_current_or_Vf_extremes_qualified=False,final_LED_panel_CAD_or_manufacturing_release=False)
result['decision']='Retain7seriesH40/4000K and unchangedC16current for firstverificationpanel. The owner now accepts higherlumens: old850lmexceedance is NOT a rejection and no opticalattenuation/R9/CRIchange is required merely to meet800lm. Nominal20.652V/6.588W/~959lm atassumedtau.87,Tj85Cfluxmodel. Currenttemperature/ripple/Vf/bin/diffuser/actualphotometry/CRI/CCT/life andwholelampsafety remainunqualified. Warm8LEDstring still exceedsallocated22V; eventualthreecolourfamily notclosed. U40 andR9/opticalattenuation rows retained as historical diagnostics only.'
peak_led_power=max(a*vf(a,t)for a,t in itertools.product(currents,[10,25,85,105,115]))
result['thermal_no_optical_credit_budget']=dict(per_LED_typical_model_upper_W=peak_led_power,seven_LED_typical_model_upper_W=7*peak_led_power,conditions='Rectangular current303.624..336.057mA/Tj10..115C typicalVf model, NOT a guaranteed peak/binnedpower bound; all electricalinput budgeted as heat',assumed_solderpoint_C=95,conditional_Tj_C_using7p6_typical=95+7.6*peak_led_power,conditional_Tj_C_using15_engineering_allowance=95+15*peak_led_power,illustrative_panel_Rth_to_ambient_max_K_per_W_for95C_at40C=(95-40)/(7*peak_led_power),thermal_path_or95C_target_not_measured=True,driver_heat_coupling_not_included=True)
put('results.json',result)
put('input-binding.json',dict(base_commit=result['source_commit'],repository_files=binding,external_manufacturer=dict(path='work/led19-sources/cree2835-current.pdf',url='https://downloads.cree-led.com/files/ds/j/JSeries-2835-3V-Consolidated.pdf',sha256=maker_sha,pages_visually_inspected=[4,5,6,7],fresh_download_date='2026-11-21',bytes_match_prior_source=True),production_files_unchanged=True))
put('native-curve-data.json',dict(source_sha256=maker_sha,current_flux_curve=curve,voltage_curve=dict(printed_page=6,drawing_index=23,axis=list(rect),samples_A_V=np.column_stack((i,v)).tolist()),method='Same native vector extraction as pinned compact60 study; currentcurve piecewiseBezier sampling, linearinterpolation; no pixel-fit or claimed guaranteedlimits.'))
with(D/'screen-cases.csv').open('w',newline='',encoding='utf-8')as f:
 wr=csv.DictWriter(f,fieldnames=list(rows[0]));wr.writeheader();wr.writerows(rows)
put('sources.json',dict(checked='2026-11-21 Europe/Warsaw',sources=[dict(id='CREE',url='https://downloads.cree-led.com/files/ds/j/JSeries-2835-3V-Consolidated.pdf',sha256=maker_sha,application='p4ratings/derating,p5exactMPNflux85C/p6typicalflux/Vfcurves,p7chromaticity; localactualfreshPDFvisuallyinspected; notredistributed'),dict(id='TI',url='https://www.ti.com/lit/ds/symlink/ucc28700.pdf',application='CCcurrentlaw,frequency/thresholdlimits;120kHzminmaxfrequency, not130guarantee'),dict(id='JLC-H40',url='https://jlcpcb.com/partdetail/C17218060',application='ExactH40listing/SMTroute confirmed inpublicpage; no reserved/liveavailablequantity; vendor200mW/60mAtesttextdoesnotreplacemakerderating'),dict(id='DK-U40',url='https://www.digikey.com/en/products/detail/cree-led/JB2835BWT-G-U40GA0000-N0000001/14554788',application='ExactU40listing Active,cut-tape1piece route. Retrievedwebsnapshot shows85548stock,0.13USD1piece; crawled3weeksold, notliveguaranteed/reserved. JLCU40code/consignmentNOTconfirmed.')]))
# Original scientific visualization; no manufacturer image/table redistribution.
fig,axs=plt.subplots(1,2,figsize=(12.8,5.2),layout='constrained');xx=np.linspace(.22,.35,180)
for key,color,label in [('H40','#b54936','H40 / klasa CRI80'),('U40','#176557','U40 / klasa CRI90')]:axs[0].plot(xx*1000,[flux(key,7,a)for a in xx],color=color,lw=2,label=label)
axs[0].axhspan(750,850,color='#777777',alpha=.12,label='Dawny cel 750–850 lm');axs[0].axhline(750,color='#555555',ls=':',label='Zachowane minimum 750 lm');axs[0].axvspan(currents[0]*1000,currents[2]*1000,color='#5279ad',alpha=.12,label='Warunkowy zakres C16');axs[0].axvline(319,color='#5279ad',ls='--',lw=1)
axs[0].set(xlabel='Prąd szeregu [mA]',ylabel='Strumień całej lampy [lm]',title='7 LED / 4000 K — model typowy');axs[0].legend(fontsize=8);axs[0].grid(alpha=.18)
for n,color in [(6,'#888888'),(7,'#176557'),(8,'#b54936')]:axs[1].plot([10,25,85,105,115],[n*vf(.319,t)for t in[10,25,85,105,115]],label=f'{n} LED, 319 mA',color=color,lw=2)
axs[1].axhspan(19,22,color='#777777',alpha=.12,label='Przyjęte 19–22 V');axs[1].set(xlabel='Temperatura złącza LED [°C]',ylabel='Napięcie szeregu [V]',title='Liczba LED a napięcie — model typowy');axs[1].legend(fontsize=8);axs[1].grid(alpha=.18)
fig.suptitle('Velluneo C16 — większa jasność zaakceptowana przez właściciela',fontsize=16);fig.supxlabel('Źródło: Cree CLJ-DS40 Rev10B, C16 • τ=0,87; strumień przy odniesieniu Tj=85°C • obliczenia, nie pomiary',fontsize=9);fig.savefig(D/'LED19_comparison.png',dpi=220);plt.close(fig)
txt('.gitignore','.work/\n__pycache__/\n')
txt('task-contract.md','''# LED19 bounded compatibility task

Owner requests checking selected LEDs against current C16 supply, specifically
voltage, light and thermal loading at319mA and whether seven series LEDs fit.
Root solewriter: led-compatibility-19/**, additiveproject-index entry and the owner-authorized revision13 append-only requirements addendum. BaseGit
7f4b7781f2178af5a57d42212a02ac1996ffcd2a. C16/C17/VIS18CAD, BOMs, rules,
manufacturing files and stage approvals are read-only. Owner explicitly relaxes only the850lm upper criterion; retain other requirements.
Check actual pinned/fresh makerPDF and exactordercode; reproduce existingtypical
curve and sourcecurrent, cover conditionalcurrent/temperature/count andthermal
derating; identify incompletebounds. Compare onecompatible4000Kcandidate if the
oldpartmissestarget; do not silentlychangeCAD orapproveparts. Fouractualindependent
reviewroles inspect samefrozenpacket. Publish checkedresults in VelluneoGitHub.
No stockreservation,suppliermessage,order,physicalmeasurement orstageadvance.
''')
txt('README.md',f'''# LED19 - seven-LED panel checked against C16

## Current result and owner decision

On21November2026 the owner stated: "jak będzie wiecej lumenów to nie problem".
The former850lm ceiling is therefore not a rejection criterion. The750lm minimum,
first4000K configuration and other colour/family, electrical, thermal, service,
insulation and lifetime requirements remain. This is not a manufacturing approval.
See owner-decision.md and the revision13 addendum in requirements-and-plan.md.

Retain seven series Cree JB2835BWT-G-H40GA0000-N0000001 (4000K,80CRIclass) as the
first panel verification candidate, with unchanged C16 R9=1.80ohm / nominal319mA.
Typical-model result:20.652V,6.588W and958.8lm at assumed optical transmission0.87
and the calculated85C junction-flux reference. The three conditional currentpoints
303.624/319/336.057mA yield917.6/958.8/1004.2lm. Higher flux is accepted; these are
calculations, not measured output or full production bounds.

## Electrical compatibility

For seven LEDs, the typical-voltage model over those currents and junction10..115C
gives20.345..21.255V, inside the allocated19..22V load window. This is not a guarantee
of cold/hot/reel extrema. Source current includes assumed transformer delivery0.90;
actual delivery, ripple and transient peaks are uncharacterized. R6/current-loop,
startup/clamp and all other C16 qualification holds remain applicable.

Six LEDs give17.439..18.218V and can fail the existing healthyVDD9.45V bias screen.
Eight give23.252..24.291V, beyond the current22V allocation. The old8LED2700K panel
cannot silently inherit the seven-LED4000K result. The eventual three-colour family
is not closed by this assessment.

## Thermal conditions

Cree specifies480mA maximum DC and125C absolute junction temperature, with explicit
thermal derating. These are not lifetime targets. Its40K/W junction-to-ambient
example permits about326mA at85C AMBIENT; that is distinct from85C JUNCTION used in
the flux model. Neither the actual lamp's thermal resistance nor temperature is known.

Budget all electrical LED input as heat, with no optical credit: the rectangular
typical-model high point is{result['thermal_no_optical_credit_budget']['seven_LED_typical_model_upper_W']:.3f}W for seven LEDs, excluding driver
heat/coupling. At an ASSUMED95C solder point, the same modeled power gives junction
about{result['thermal_no_optical_credit_budget']['conditional_Tj_C_using7p6_typical']:.2f}C with maker7.6K/W TYPICAL Rjs, or
{result['thermal_no_optical_credit_budget']['conditional_Tj_C_using15_engineering_allowance']:.2f}C with a hypothetical15K/W allowance. This does not establish either a95C
solder point or a guaranteed junction/life limit. A metal-core/otherwise qualified
substrate, TIM/heat path and measured solder-point/junction estimate are still due.
Transformer surrounding ambient<=50C and driver component temperatures are separate.

## Retained diagnostics, not new selections

The U40/90CRIclass comparison gives824.6lm nominal and789.2..863.6lm at the same
assumptions. It is not selected: changing CRI/parts is unnecessary merely to keep
the former upper limit. Its DigiKey one-piece route is documented; JLC sourcing is
unconfirmed. No purchasing or assembly acceptance is implied.

R9-only2.21/2.26ohm diagnostics reduce H40 flux but require128.4/131.0kHz in the
existing conservative frequency screen, above the120kHz minimum maximum-frequency
capability. Therefore a resistor-only change is not an accepted fix. Optical
attenuation diagnostics are historical; extra dimming is not required by the owner.

## Evidence and limits

The fresh manufacturerPDF matches pinned CLJ-DS40Rev10B bytes. ExactMPN/limits and
native curves were visually checked; numerical replay matches earlier flux/voltage
and C16frequency calculations. results.json and180-row screen-cases.csv preserve
failures and source assumptions. The chart labels the old band as historical.

The order code does not guarantee an upper flux bin. Hot flux references are
calculated by Cree; scaling with the25C current curve assumes separability. Actual
diffuser transmission, bin, stabilizedjunction temperature, CRI/CCT at319mA, flicker,
lifespan and thermal fit require characterization. Photometric acceptance uses the
owner's230Vac/25+/-1Cambient/base-up/complete-diffuser/stabilization method, not an
assumption that ambient equals junction temperature.

No full manufacturerPDF is redistributed. Replay uses the external retained PDF
through check_led19.py from workspacework/. Production CAD/BOMs/rules/C17exports
are unchanged. This is a compatibility calculation and retained verification
direction, not a finishedLEDpanelPCB, measured qualification or production release.
''')
assert all(sha(P/x)==z for x,z in binding.items())
print(json.dumps(dict(nominal=nom,counts=counts,trim=trim,assessment=result['current_assessment'],thermal=result['thermal_no_optical_credit_budget']),indent=2))





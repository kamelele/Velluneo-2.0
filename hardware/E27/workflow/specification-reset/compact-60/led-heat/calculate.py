"""Reproduce COMPACT-60 LED heat from native primary PDF vectors and CIE data.
Requires PyMuPDF/numpy; no network, CAD mutation or physical observations.
"""
from pathlib import Path
import argparse, hashlib, json, math
import fitz
import numpy as np
HERE=Path(__file__).resolve().parent
BASE=HERE.parents[1]
ROOT=HERE.parents[6]
EXPECTED={
 'cree2835.pdf':'74d4261952c25e6833212a82b0f72e759f8297478627a368f4acff22378c92c8',
 'cree-lm80.pdf':'35ea8a1f3658866877efd058af3eff0384ed0e31437c71e274000a99e248f54c',
 'cree-thermal.pdf':'2487399e6e62987aaec1c8d1bb44e8418c3d673137ee70ca4ea3b3c15b878038',
 'cie1931.csv':'fa663e3535a7e0763a745993a1f0a192eb0275ac46ad2d1befd7626841e713c1'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,obj): (HERE/n).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8',newline='\n')
def points(draw):
 out=[]
 for item in draw['items']:
  if item[0]=='l': out.extend([(p.x,p.y) for p in item[1:]])
  elif item[0]=='c':
   p=np.array([(p.x,p.y) for p in item[1:]])
   for t in np.linspace(0,1,5):out.append(tuple((1-t)**3*p[0]+3*(1-t)**2*t*p[1]+3*(1-t)*t*t*p[2]+t**3*p[3]))
  else:raise ValueError(item[0])
 return np.array(out)
def main(src):
 hashes={n:sha(src/n) for n in EXPECTED};assert hashes==EXPECTED,hashes
 pdf=fitz.open(src/'cree2835.pdf'); spectra=pdf[40].get_drawings(); box=spectra[28]['rect']
 cie=np.loadtxt(src/'cie1931.csv',delimiter=',');wl=np.arange(380.,781.);v=np.interp(wl,cie[:,0],cie[:,2])
 electrical=pdf[5].get_drawings(); boxv=electrical[18]['rect'];pv=points(electrical[23])
 volts=2.6+(pv[:,0]-boxv.x0)/boxv.width*.6;amps=(boxv.y1-pv[:,1])/boxv.height*.480
 order=np.argsort(amps);amps=amps[order];volts=volts[order]
 optical=json.loads((BASE/'electrical-refinement/optics/results.json').read_text(encoding='utf-8'))
 current=optical['minimax_nominal_family_current_A'];vf25=float(np.interp(current,amps,volts));vf85=vf25-.0009*60
 outputs={}; extracted={};checks=[]
 for cct,idx,n in [('2700',39,8),('4000',36,7),('6500',33,7)]:
  xy=points(spectra[idx]);x=380+(xy[:,0]-box.x0)/box.width*400;y=(box.y1-xy[:,1])/box.height
  # Native plots have sub-pixel zero-axis overshoot; clip only physically negative ordinates.
  s=np.maximum(0,np.interp(wl,x,y)); area=float(np.trapezoid(s,wl));ler=683*float(np.trapezoid(s*v,wl))/area
  flux=optical['nominal_family_lm_at_minimax_current'][cct];escape=flux/ler; emitted=escape/.87
  pe=n*current*vf85
  outputs[cct]={'LED_count':n,'current_A':current,'Vf25_typical_V':vf25,'Vf85_typical_V':vf85,'panel_V85_typical_V':n*vf85,
    'panel_electrical85_typical_W':pe,'whole_lamp_flux_typical_lm':flux,'spectral_LER_typical_lm_per_radiant_W':ler,
    'escaping_radiant_typical_W':escape,'LED_emitted_radiant_typical_W_neutral_diffuser':emitted,
    'LED_local_heat_typical_W':pe-emitted,'diffuser_absorption_typical_W_neutral_diffuser':emitted-escape,
    'panel_plus_diffuser_heat_typical_W':pe-escape,'per_LED_electrical85_typical_W':current*vf85,
    'junction_rise_full_electrical_times_7p6_typical_K':current*vf85*7.6}
  # Check independent numerical integration at 0.25nm resolution.
  wf=np.arange(380,780.0001,.25);sf=np.maximum(0,np.interp(wf,x,y));vf=np.interp(wf,cie[:,0],cie[:,2]);lf=683*np.trapezoid(sf*vf,wf)/np.trapezoid(sf,wf)
  checks.append({'CCT':cct,'LER_1nm_vs_quarter_nm_delta_percent':float(100*(lf/ler-1))})
  extracted[cct]={'PDF_printed_page':41,'drawing_index':idx,'wavelength_nm':wl.tolist(),'relative_spectrum':np.round(s,8).tolist()}
 # Source-conditioned screens: they are NOT guaranteed LED V/I bounds.
 coldhot=[]
 for i in [.21876295319202657,current,.2891944014593847]:
  v25=float(np.interp(i,amps,volts))
  for t in [-20,25,85,105]:
   vv=v25-.0009*(t-25)
   coldhot.append({'I_A':i,'T_C':t,'Vf_typ_V':vv,'7_LED_V':7*vv,'8_LED_V':8*vv,'8_LED_electrical_W':8*i*vv})
 screen_power=27*.2891944014593847
 geom={'panel_diameter_mm':48,'package_mm':[2.8,3.5,.7],'LED_ring_radius_mm':16,'eight_LED_pitch_mm':32*math.sin(math.pi/8),
 'worst_body_circumradius_mm':16+math.hypot(2.8,3.5)/2,'rim_contact_OD_mm':48,'rim_contact_ID_mm':36,
 'rim_contact_area_mm2':math.pi*(24**2-18**2),'TIM_0p1mm_k1p5_1D_R_K_per_W':.0001/(1.5*math.pi*(.024**2-.018**2)),
 'dielectric_150um_k1_8mm_square_R_K_per_W':.00015/(.008**2),'dielectric_150um_k1_3mm_square_R_K_per_W':.00015/(.003**2)}
 checks.extend([{'check':'all_model_LED_heat_positive','pass':all(o['LED_local_heat_typical_W']>0 for o in outputs.values())},
 {'check':'all_integration_errors_below_0p02percent','pass':all(abs(c['LER_1nm_vs_quarter_nm_delta_percent'])<.02 for c in checks if 'LER_1nm_vs_quarter_nm_delta_percent'in c)},
 {'check':'ring_body_fits_48mm','pass':geom['worst_body_circumradius_mm']<24}])
 assert all(c.get('pass',True) for c in checks)
 write('native-spectra.json',{'source_SHA256':hashes['cree2835.pdf'],'native_axis_rect_points':list(box),'method':'Bezier 4 subdivisions/segment; linear resample1nm; negative undershoot clipped0','curves':extracted})
 result={'scope':'Calculated typical models and conservative conditional bounds; no simulation or physical measurement; no changed parts or graph.',
 'source_SHA256':hashes,'script_SHA256':sha(Path(__file__)),'optical_input_SHA256':sha(BASE/'electrical-refinement/optics/results.json'),
 'spectral_model_assumptions':['80CRI published generic spectra apply at modeled actual current/temperature (unverified)','380-780nm truncated source; not all emitted wavelengths','fitted diffuser spectrally neutral tau_radiant=tau_luminous=.87 (unverified)','85C electrical junction/reference condition not actual25Cambient'],
 'family_typical':outputs,'typical_forward_voltage_coldhot_screen':coldhot,
 'guaranteed_condition_only_escape_lower_bound_W_at750lm':750/684,
 'whole_lamp_heat_identity':'Qtotal=measured Pin - total escaping radiant; conditional Qtotal<=Pin-actual flux/684. No credit for absorbed/scattered photons remaining inside.',
 'no_flux_credit_LED_electrical_rectangular_screen_W':screen_power,
 'panel_temperature_contract_calculated':{'rim_C':75,'local_R_allowance_K_per_W_per_LED':10,'mutual_R_allowance_K_per_W_total_panel':1,'solder_case_screen_C':75+screen_power+10*screen_power/7,'junction_screen_C_with15KperW_allowance':75+screen_power+25*screen_power/7,'solder_case_design_target_C':95,'junction_design_target_C':115},
 'screen_junction_rise_7p6_times_Imax_27div7_K':7.6*.2891944014593847*27/7,
 'screen_junction_rise_design_allowance15_times_Imax_27div7_K':15*.2891944014593847*27/7,
 'geometry_calculated_proposal':geom,'checks':checks}
 write('results.json',result)
 print(json.dumps({'family_typical':outputs,'screen_power_W':screen_power,'checks':checks},indent=2))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--sources',type=Path,required=True);main(p.parse_args().sources)

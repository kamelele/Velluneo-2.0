"""ELEC-CLOSE-01 custom winding candidate, conditional geometry/DC calculation.
No magnetic/core-loss fit, thermal equilibrium, safety or measured result implied.
"""
import math,json,pathlib,argparse
P=pathlib.Path(__file__).resolve().parent
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--output',type=pathlib.Path,default=P/'winding-results.json')
args=parser.parse_args()
# Native data transcribed from exact primary sources; dimensions mm.
AN=40.7; width=10.5
wire_p=dict(name='ELEKTRISOLA Polysol 180 P180 copper 0.180mm IEC Grade2',bare=.18,bare_min=.177,od_max=.217,r20_max_ohm_m=.7007)
wire_s=dict(name='Furukawa TEX-E 0.30mm',bare=.30,bare_min=.29,od_max=.520,r20_max_ohm_m=.2629,reference_table_not_purchase_spec=True)
tape=dict(name='3M1350F-1',nominal=.064,representative_upper=.077,not_binding_spec=True)
# Packing pitches and length budgets are construction proposals, not source guarantees.
windings=[dict(id='P',turns=120,layers=[40,40,40],pitch=.240,wire=wire_p,irms=.091545,ipeak=.358522,dot=1,finish=5),dict(id='A',turns=22,layers=[22],pitch=.240,wire=wire_p,irms=None,ipeak=None,dot=2,finish=4),dict(id='S',turns=30,layers=[15,15],pitch=.550,wire=wire_s,irms=.53879,ipeak=1.434,dot=6,finish=10)]
# Four single tape wraps, nonaligned seams; at any angular location permit at most
# one additional overlap thickness. Not multilayer safety-insulation qualification.
radial_wire=sum(len(w['layers'])*w['wire']['od_max'] for w in windings)
radial_regular=radial_wire+4*tape['representative_upper']
radial_seam=radial_regular+tape['representative_upper']
# Copper alpha is an engineering copper-material approximation, not a wire maker's
# hot resistance guarantee. 20/100/125C sensitivity; MLT50 native representative,
# MLT60 proposed length acceptance/sensitivity, plus100mm total lead length.
alpha=.00393
cases=[]
for mlt in [50,60]:
 for temp in [20,100,125]:
  rows=[]
  for w in windings:
   length=w['turns']*mlt/1000+.100
   r=w['wire']['r20_max_ohm_m']*length*(1+alpha*(temp-20))
   area=math.pi*w['wire']['bare_min']**2/4
   rows.append(dict(winding=w['id'],wire_length_m=length,R_ohm=r,DC_equivalent_Irms_loss_W=None if w['irms'] is None else w['irms']**2*r,peak_IR_drop_V=None if w['ipeak'] is None else w['ipeak']*r,Jrms_A_mm2=None if w['irms'] is None else w['irms']/area,aux_loss_at_rms_A_W={str(i):i*i*r for i in [.02,.05,.10]} if w['id']=='A' else None))
  cases.append(dict(MLT_mm=mlt,temperature_C=temp,windings=rows,sum_PS_dc_loss_W=sum(x['DC_equivalent_Irms_loss_W'] or 0 for x in rows)))
copper_area=sum(w['turns']*math.pi*w['wire']['bare']**2/4 for w in windings)
wire_envelope_area=sum(w['turns']*math.pi*w['wire']['od_max']**2/4 for w in windings)
for w in windings:
 w['maximum_layer_span_mm']=max(w['layers'])*w['pitch']
 w['available_unused_width_mm']=width-w['maximum_layer_span_mm']
 assert sum(w['layers'])==w['turns'] and w['maximum_layer_span_mm']<=width
result=dict(status='proposed construction; source-linked conditional calculations, not qualified winding',native=dict(AN_mm2=AN,MLT_mm=50,Np=120,Ns=30,Na=22,AL_nH=160,AL_tolerance_fraction=.10,Lp_mH=160e-6*120**2,Amin_mm2=57),winding_band_mm=width,winding_order_inner_to_outer=['base tape','P three layers, no interlayer tape','one tape wrap','A one layer','one tape wrap','S two layers','outer tape'],windings=windings,tape=tape,geometry=dict(radial_wire_mm=radial_wire,radial_regular_mm=radial_regular,radial_one_seam_mm=radial_seam,band_x_radial_envelope_mm2=width*radial_seam,band_envelope_over_AN=width*radial_seam/AN,copper_area_mm2=copper_area,copper_fill=copper_area/AN,wire_OD_circle_area_mm2=wire_envelope_area,OD_circle_fill=wire_envelope_area/AN,needed_local_cross_section_mm=[width,radial_seam],rectangular_window_fit_verified=False),loss_cases=cases,limitations=['AN area alone does not guarantee rectangle or local exit clearance; require actual usable bobbin width>=10.5mm and radialroom>=2.293mm everywhere in active band.','P layer crossover routes use reserved side pockets, not an added crossover over active winding; feasibility must be confirmed on winding drawing/sample.','MLT60mm is proposed cut-length acceptance/sensitivity, not a sourced maximum.','Source table OD/resistance and tape thickness include reference/representative limitations; procurement batch limits must be specified.','Temperature loss extrapolation uses approximate copper alpha .00393/K; skin/proximity/gapfringing/termination AC loss excluded.','P/S currents are separate maxima from a correlated corner sweep; summed losses are a conservative screen of maxima, not one asserted controller trajectory.','Aux waveform not supplied; auxiliary loss coefficient and explicit current sensitivities only.'])
args.output.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(dict(geometry=result['geometry'],hot60mm=cases[-1]),indent=2))

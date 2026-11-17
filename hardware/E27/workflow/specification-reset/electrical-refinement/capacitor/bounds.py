"""Conditional KCL and nonnegative-triangular-pulse bounds; not hardware certification."""
from pathlib import Path
import json,math,hashlib,argparse
P=Path(__file__).resolve().parent
SPEC=Path(__file__).resolve().parents[2]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--historical-results',type=Path,default=SPEC/'electrical-integration/input-corners-results.json')
parser.add_argument('--switched-results',type=Path,default=P/'results.json')
parser.add_argument('--output',type=Path,default=P/'bounds-results.json')
args=parser.parse_args()
s=args.historical_results
if hashlib.sha256(s.read_bytes()).hexdigest()!='a2ba3a610228251b3f825fcdc7375e99e5e4d74a252ca3ee515775a112bf9816':
 raise ValueError('Historical averaged-result SHA256 mismatch; review changed inputs')
old=json.loads(s.read_text());b=old['summary']['proposed_two_series_pairs']['bounds'];sw=json.loads(args.switched_results.read_text())
ib=b['line_rms_A'][1];vmin=b['bulk_min_V'][0];vmax=b['bulk_max_V'][1];peak=.358522;pload=11.;rbleed=499000*.979
# Exact for complete triangular pulses at fixedpeak, or with explicit endpulse correction:
# Ip_rms²=(2/3)*Ip_peak*Ip_mean. Ip_mean<=P/Vmin ifP is electricalmeaninput.
ip=math.sqrt(2*peak*pload/(3*vmin));bleed=vmax/rbleed;draw=ip+bleed
root=math.hypot(ib,draw);rating=.190*.80
ir_allowed=math.sqrt(rating**2-draw**2)-ib
# Illustrative additional input-energy return fraction; not supported leakage bound.
# Shape-independent 0<=Ir<=Ipk => Ir_rms²<=Ipk*Ir_mean; if positivebulkreturnedpower<=11W*.01 then Ir_mean<=that/Vmin.
return_fraction=.01;irproxy=math.sqrt(peak*pload*return_fraction/vmin)
withret=math.hypot(ib+irproxy,draw)
rows=sw['rows'];ibsw=max(r['Ib_rms']for r in rows);idsw=max(r['Idraw_rms']for r in rows);icsw=max(r['Ic_rms']for r in rows)
result=dict(averaged_source_results_sha256=hashlib.sha256(s.read_bytes()).hexdigest(),native_rating=dict(iref120Hz_A=.190,coefficient50Hz=.80,all_band_50Hz_comparison_A=rating,not_combined_spectrum_or_lifetime_qualification=True),conditional_mixed_envelope=dict(Ibridge_rms_A=ib,Vmin_V=vmin,Vmax_V=vmax,triangular_primary_rms_A=ip,bleeder_sup_A=bleed,draw_rms_triangle_bound_A=draw,nonnegative_KCL_rss_bound_A=root,triangle_Ibridge_plus_Idraw_A=ib+draw,allowed_positive_return_rms_A_if_all_other_bounds_hold=ir_allowed,source_model_is_averaged_not_actual_switched_bound=True),illustrative_unverified_onepercent_return=dict(return_power_fraction=return_fraction,peak_return_A=peak,shape_independent_return_rms_bound_A=irproxy,combined_KCL_bound_A=withret,rating_ratio=withret/rating,not_a_qualified_leakage_or_clampwaveform_bound=True),switched_model_samewaveform=dict(Ibridge_max_rms_A=ibsw,Idraw_max_rms_A=idsw,RSS_of_separate_maxima_A=math.hypot(ibsw,idsw),actual_max_Ic_rms_A=icsw,rating_ratio=icsw/rating,additional_signed_current_triangle_budget_A_if_baseline_waveform_unchanged=rating-icsw,positive_return_rss_budget_A_if_bounds_stillhold=math.sqrt(rating**2-idsw**2)-ibsw),conditions=['KCL pointwiseIc=Ib+Ir-Id; Ib,Ir,Idnonnegative. Dropnegativecrossesonly; retainIbIr viaCauchy.','Ib andId bounds must hold on actualsamewaveforms after addingreturn. An unknownreturn changesbulkvoltage/bridgeconduction andcannot simplybe appendedas aphysicalratingpass.','Clampreturn power/peak bounds, triangularprimarymoments,11Wdrawenvelope andsourcebridgeHF requireactualcircuitvalidation.','Signed/unaccounted currentsu require trianglebudget||Ic+u||<=||Ic||+||u|| on the samebaseline; not independence/orthogonality.','Do not infer sum(I_f/I_allow_f)^2 formula as manufacturerprescription; nativefamilytableprovides coefficients only.'])
args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

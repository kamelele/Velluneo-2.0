"""Phase-wise conservative rigid-envelope insertion bounds, not actual wire/force qualification."""
from pathlib import Path
import json,math,itertools
D=Path(__file__).resolve().parent;P=D.parent
C=json.loads((D/'assembly-contract.json').read_text(encoding='utf-8'));R=json.loads((D/'results.json').read_text(encoding='utf-8'));L=json.loads((D/'packing-diagnostic.json').read_text(encoding='utf-8'));I=json.loads((P/'compact-60/mechanics/native-inventory.json').read_text(encoding='utf-8'))
cup=C['cup']
def rad(z):
 p=cup['lower_outer_profile_Z_R_mm']
 for (a,x),(b,y)in zip(p,p[1:]):
  if z<=b:return x+(y-x)*(z-a)/(b-a)
 return p[-1][1]
def rr_sdf(x,d):
 a,b,c,e=cup['upper_inside_X_D_box_mm'];r=cup['upper_inside_corner_r_mm'];qx=abs(x-(a+c)/2)-(c-a)/2+r;qy=abs(d-(b+e)/2)-(e-b)/2+r
 return math.hypot(max(qx,0),max(qy,0))+min(max(qx,qy),0)-r
obs=[]
for p in R['part_results']:
 b=p['nominal_box_X_D_Z_mm'];obs.append({'name':p['ref'],'box':[b[0]-.4,b[1]-.35,b[2]-.6,b[3]+.4,b[4]+.35,b[5]+.6]})
for p in R['joints']:
 b=p['box_X_D_Z_mm'];obs.append({'name':p['ref']+'.'+p['pin']+'tail','box':[b[0]-.4,b[1]-.35,b[2]-.6,b[3]+.4,b[4]+.35,b[5]+.6]})
# PCB dimension/pose is conservative; groove fit below uses correlated width/thickness float rather than impossible extreme combinations.
obs.append({'name':'PCB','box':[-16.375,-.55,30.5,16.375,1.75,91.5]})
upper=[]
for p in obs:
 b=p['box']
 if b[5]<40:continue
 radius_required=max(math.hypot(x,d)for x in(b[0],b[3])for d in(b[1],b[4]));margin=28.1-.2-radius_required
 if b[5]>=56:margin=min(margin,min(-rr_sdf(x,d)-.2 for x in(b[0],b[3])for d in(b[1],b[4])))
 upper.append({'object':p['name'],'minimum_passage_margin_mm':margin})
# Every loading translation is along+Z. The uppercup's lowercavity isconstant28.1 andupperDshape iscontainedin thatcircle.
# For each constantcross-section box, finalhighestZ decides whether itever enters the narrower upperDsection.
low=[p for p in obs if p['box'][2]<=42.1]
lowmax=max((max(math.hypot(x,d)for x in(p['box'][0],p['box'][3])for d in(p['box'][1],p['box'][4])),p['name'])for p in low)
sleeve_inner_min=rad(34)-cup['nose_overlap_radial_stack_mm']-.2
sleeve_outer_max=max(v[1]for v in cup['lower_outer_profile_Z_R_mm'])-cup['joiner_outer_reduction_from_profile_mm']+cup['joiner_outer_radius_tol_mm']+cup['joiner_eccentricity_bound_mm']
sleeve_to_upper_clear=28.1-.2-sleeve_outer_max
nose_to_sleeve_clear=cup['joiner_radial_gap_mm']-.2-cup['joiner_outer_radius_tol_mm']-cup['joiner_eccentricity_bound_mm']
# Endcradles are parts of removablelid/nose and absent duringPCBloading. Include allpackage,jointandSMTmetal envelopes.
metal=[]
for p in I['parts']:
 c=L['positions'][p['ref']];sg=1 if c['side']=='F'else-1;seat=.6+sg*.8;ds=sorted([seat,seat+sg*.35])
 for pp,b in zip(p['pads'],c['pads']):
  if pp['tht']:continue
  metal.append({'name':p['ref']+'.'+pp['pin']+'pad','box':[b[0]-.6,ds[0]-.35,61-b[3]-.8,b[2]+.6,ds[1]+.35,61-b[1]+.8]})
def overlapXD(a,b):return a[0]<b[3]and b[0]<a[3]and a[1]<b[4]and b[1]<a[4]
cradles=[];hits=[]
for which,zinterval in [('nose',C['support']['bottom_cradle_Z_mm']),('lid',C['support']['top_cradle_Z_mm'])]:
 for xi in C['support']['bottom_left_right_X_intervals_mm']if which=='nose'else C['support']['left_right_X_intervals_mm']:
  for di in C['support']['D_flange_intervals_mm']:
   q=[xi[0],di[0],zinterval[0],xi[1],di[1],zinterval[1]];cradles.append({'piece':which,'box_X_D_Z_mm':q})
   for p in obs[:-1]+metal:
    b=p['box'];reaches=b[2]<=q[5]if which=='nose'else b[5]>=q[2]
    if reaches and overlapXD(q,b):hits.append({'cradle':which,'object':p['name']})
guide=R['guide'];checks={'upper_cup_populatedPCB_loading_min_margin_mm':min(p['minimum_passage_margin_mm']for p in upper),'sleeve_lower_obstacle_max_radius_mm':lowmax[0],'sleeve_lower_obstacle_name':lowmax[1],'sleeve_inner_min_radius_mm':sleeve_inner_min,'sleeve_over_lowerPCB_min_margin_mm':sleeve_inner_min-lowmax[0],'sleeve_outer_max_radius_with_tolerance_and_eccentricity_mm':sleeve_outer_max,'sleeve_into_upper_mouth_min_radial_clearance_mm':sleeve_to_upper_clear,'nose_over_sleeve_min_radial_clearance_mm':nose_to_sleeve_clear,'endcradle_swept_obstacle_cases':hits,'groove_min_width_insertion_clearance_mm':guide['min_width_insertion_clearance_mm'],'groove_min_thickness_insertion_clearance_mm':guide['min_thickness_insertion_clearance_mm']}
assert checks['upper_cup_populatedPCB_loading_min_margin_mm']>=.3,checks
assert checks['sleeve_over_lowerPCB_min_margin_mm']>=.3 and sleeve_to_upper_clear>0 and nose_to_sleeve_clear>0,checks
assert not hits,hits
out={'scope':'Analyticalrigid-envelopepathscreen underdeclaredheight/position/processallocations, includingPCB,31bodyenvelopes,3mmtrimmedtails andallSMTmetal envelopes forcradles. Not assembledwirebends/retentionforce/manufacturedprocess validation.','RF01_resolution':'No fixeduppercupwallbelowZ40. Narrowjoiner isseparate andaddedafterPCB; no T1/C1needpassitsnarrowlowersection. Cradlesarewithremovablenose/lid,notintegralsiderailsduringloading.','phaseA':'LoadpopulatedPCBupwards throughopenuppercupZ40 withjoiner,nose,lidandcradlesabsent. Forboxcrosssections, cavityshrinksmonotonicallyfromcircletoDshape; checkedtransverseboundseveryreachedsection.','phaseB':'Insertseparatesleeveupwardsfrombelow. OnlyobstacleswithworstlowerZ<=42.1canbeencountered. Allfitminimuminnersleevebound. Thelargestoutertipfitsthroughuppercupmouthincludingtolerance/eccentricity.','phaseC':'Closelowernosefrombelow. InnerprofileisnondecreasingwithlocalZ, sofinalpositionisthesmallestclearance; sleeve/partboundschecked. FloorremainsbelowPCB. Lowercradlesclearallbodies/joints/metalenvelopesencountered.','phaseD':'Closelidfromabove; endcradlesfittedinthisphase clearallbodies/joints/metalenvelopesencountered. Actualcontact/wirebendroutingandforcequalificationremainopen.','checks':checks,'upper_loading_objects':upper,'endcradles':cradles,'conditional_path_screen_pass':True,'actual_assembly_qualified':False,'open':['Unselectedwire/cablebend/strainreliefandcontactsoutside3mmjointreservation','Material/seam/retention/assemblytoolingandforcequalification','SourceT1/F1/seating/installedheight/tolerancecontractsnot supplierconfirmed','Electricalinsulationof2mmupperand6mmlowerlapnotestablished']}
print(json.dumps(out,indent=2))

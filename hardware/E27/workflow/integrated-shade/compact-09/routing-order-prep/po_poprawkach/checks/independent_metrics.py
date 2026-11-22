"""Read-only comparison and same-net Kelvin overlap audit; not EMI/thermal proof."""
from pathlib import Path
import sys,json,math,hashlib,itertools,argparse
import pcbnew as k
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'work/compact09/catalog-only/checker'));import checker as c
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def metrics(path,project,matrix,assessment):
 before=sha(path);b=c.q.load_native(path);co=c.Checker(b,c.Contract(project,matrix,assessment));co.collect();tracks=list(b.GetTracks());fps={f.GetReference():f for f in b.GetFootprints()};pads={(r,p.GetNumber()):p for r,f in fps.items()for p in f.Pads()}
 def pt(r,n):p=pads[r,n].GetPosition();return[k.ToMM(p.x)-100,k.ToMM(p.y)-100]
 pairs=[('C6.1 to T1.1',('C6','1'),('T1','1')),('C6.2 to D1.2',('C6','2'),('D1','2')),('C5.1 to U1.1',('C5','1'),('U1','1'))]
 endpoints=[{'pair':name,'a_mm':pt(*a),'b_mm':pt(*d),'pad_center_distance_mm':math.dist(pt(*a),pt(*d))}for name,a,d in pairs]
 endpoints.append({'pair':'C5.2 to nearest U1 SOURCE','pad_center_distance_mm':min(math.dist(pt('C5','2'),pt('U1',n))for n in ['5','6','7','8'])})
 keys={};duplicates=[];netstats={};lengths=[]
 for t in tracks:
  if isinstance(t,k.PCB_VIA):continue
  a=t.GetStart();d=t.GetEnd();length=k.ToMM(t.GetLength());lengths.append(length);key=(t.GetLayer(),t.GetNetname(),t.GetWidth(),tuple(sorted([(a.x,a.y),(d.x,d.y)])))
  if key in keys:duplicates.append([keys[key],t.m_Uuid.AsString()])
  keys[key]=t.m_Uuid.AsString();x=netstats.setdefault(t.GetNetname(),{'length_mm':0,'segments':0});x['length_mm']+=length;x['segments']+=1
 source=[]
 for layer in ['F.Cu','B.Cu']:
  union=k.SHAPE_POLY_SET()
  for o in co.objects:
   if o.layer==layer and o.net=='SW_SOURCE':union.BooleanAdd(o.shape)
  source.append({'layer':layer,'SOURCE_saved_copper_union_mm2':union.Area()/1e12})
 result={'PCB_sha256':before,'footprints':len(fps),'physical_pads':len(pads),'track_segments':len(lengths),'vias':sum(isinstance(t,k.PCB_VIA)for t in tracks),'track_length_sum_mm':sum(lengths),'shorter_than_0_30_mm':sum(x<.3 for x in lengths),'at_most_0_10_mm_tolerance_1nm':sum(x<=.100001 for x in lengths),'exact_duplicate_track_pairs':duplicates,'net_track_statistics':netstats,'SOURCE_area':source,'SOURCE_pour_mm2':sum(z.GetFilledPolysList(z.GetLayer()).Area()/1e12 for z in b.Zones()if not z.GetIsRuleArea() and z.GetNetname()=='/SW_SOURCE'),'endpoint_proxies':endpoints,'pad_net_map':{r+'.'+n:p.GetNetname()for(r,n),p in pads.items()},'MPNs':{r:f.GetValue()for r,f in fps.items()},'layer_count':b.GetCopperLayerCount(),'board_thickness_mm':k.ToMM(b.GetDesignSettings().GetBoardThickness()),'native_loaded_track_net_parity':c.q.raw_track_nets(path)=={t.m_Uuid.AsString():t.GetNetname()for t in tracks},'source_unchanged':sha(path)==before}
 return result,co
def kelvin(co,records):
 routes=records.get('routes',records.get('tracks',[]));ids={r['uuid']for r in routes if 'kelvin' in str(r.get('purpose',r.get('function',r.get('name','')))).lower()};objects=co.objects;ks=[o for o in objects if o.id in ids];missing=ids-{o.id for o in ks}
 allowed={o.layer:o.shape for o in objects if o.id=='R5.2'};findings=[];checked=0
 for a in ks:
  for b in objects:
   if a.layer!=b.layer or b.net!='FB_INDUCTOR' or b.id in ids or b.id in ['R5.2','U1.3']:continue
   p=c.q.clipped(a.shape,b.shape)
   if p.IsEmpty():continue
   checked+=1
   if a.layer in allowed:p.BooleanSubtract(allowed[a.layer])
   if not p.IsEmpty():findings.append({'Kelvin':a.id,'other_FB':b.id,'layer':a.layer,'overlap_outside_R5_mm2':p.Area()/1e12})
 return {'passed':bool(ids) and not missing and not findings,'Kelvin_native_objects':len(ks),'missing_declared_UUIDs':sorted(missing),'other_FB_intersections_checked':checked,'findings':findings,'limit':'Saved planar outward polygon intersection audit at2um approximation, excluding allowed physicalR5padandU1receiverpad; not impedance or current waveform proof.'}
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--before',required=True);ap.add_argument('--before-project',required=True);ap.add_argument('--before-assessment',required=True);ap.add_argument('--after',required=True);ap.add_argument('--after-project',required=True);ap.add_argument('--after-assessment',required=True);ap.add_argument('--matrix',required=True);ap.add_argument('--seed',required=True);ap.add_argument('--output',required=True);a=ap.parse_args()
 old,_=metrics(a.before,a.before_project,a.matrix,a.before_assessment);new,co=metrics(a.after,a.after_project,a.matrix,a.after_assessment);r={'actual_actor':'/root','date':'2026-11-22','before':old,'after':new,'same_pad_net_graph':old['pad_net_map']==new['pad_net_map'],'same_component_values':old['MPNs']==new['MPNs'],'Kelvin_audit':kelvin(co,load(a.seed)),'physical_measurements':False,'metric_limits':'SOURCEcopperareas include allsaved copper perfaceunion. Endpointdistances are geometricproxies only. Tracksum includes allbranches; neither is commutation-loop inductance or EMI/thermal qualification.'};Path(a.output).write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'same_graph':r['same_pad_net_graph'],'same_values':r['same_component_values'],'before_segments':old['track_segments'],'after_segments':new['track_segments'],'before_SOURCE_pour_mm2':old['SOURCE_pour_mm2'],'after_SOURCE_pour_mm2':new['SOURCE_pour_mm2'],'Kelvin':r['Kelvin_audit']}))

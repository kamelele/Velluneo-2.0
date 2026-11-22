"""Exercise the semantic audit on isolated, explicitly invalid copper fixtures."""
from pathlib import Path
import json,sys,hashlib,argparse,shutil
import pcbnew as k
import independent_metrics as m

ap=argparse.ArgumentParser()
ap.add_argument('--project',required=True)
ap.add_argument('--matrix',required=True)
ap.add_argument('--assessment',required=True)
ap.add_argument('--seed',required=True)
ap.add_argument('--output',required=True)
a=ap.parse_args();project=Path(a.project);board=project/'SC09_compact.kicad_pcb';out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
source=m.sha(board);records=m.load(a.seed)
_,co=m.metrics(board,project,a.matrix,a.assessment)
baseline=m.kelvin(co,records)
assert baseline['passed'], 'Controls require an independently passing starting candidate'
missing=json.loads(json.dumps(records));missing['routes'].append({'uuid':'00000000-0000-4000-8000-000000000001','purpose':'Kelvin missing-UUID negative control'})
missing_result=m.kelvin(co,missing);assert not missing_result['passed'] and missing_result['missing_declared_UUIDs']
b=m.c.q.load_native(board)
ids={r['uuid'] for r in records['routes'] if 'kelvin' in r.get('purpose','').lower()}
# Choose an existing interior point of the saved sense path, away from R5,
# and deliberately attach a same-net force branch to it outside the allowed pad.
pads={(f.GetReference(),p.GetNumber()):p for f in b.GetFootprints() for p in f.Pads()}
r5=pads['R5','2'].GetPosition()
choices=[t for t in b.GetTracks() if not isinstance(t,k.PCB_VIA) and t.m_Uuid.AsString() in ids and k.ToMM(t.GetLength())>1]
assert choices,'Need a nontrivial declared Kelvin trace'
def distance(t):
    s=t.GetStart();e=t.GetEnd();return ((s.x+e.x)/2-r5.x)**2+((s.y+e.y)/2-r5.y)**2
t=max(choices,key=distance);s=t.GetStart();e=t.GetEnd();p=k.VECTOR2I(round((s.x+e.x)/2),round((s.y+e.y)/2));force=pads['T1','2']
bad=k.PCB_TRACK(b);bad.SetNet(t.GetNet());bad.SetLayer(t.GetLayer());bad.SetWidth(k.FromMM(.3));bad.SetStart(p);bad.SetEnd(force.GetPosition());b.Add(bad)
fixture=out/'invalid-same-net-force-join.kicad_pcb';assert k.SaveBoard(str(fixture),b,True)
_,invalid_co=m.metrics(fixture,project,a.matrix,a.assessment)
join_result=m.kelvin(invalid_co,records);assert not join_result['passed'] and join_result['findings']
assert m.sha(board)==source,'Control mutated source'
r={'actual_actor':'/root','source_sha256':source,'source_unchanged':True,'baseline':baseline,'missing_UUID_control':missing_result,'same_net_force_join_control':join_result,'invalid_fixture_sha256':m.sha(fixture),'added_track_uuid':bad.m_Uuid.AsString(),'scope':'Deliberately invalid isolated fixtures validate missing-object and same-net intersection detection. Native different-net DRC is not claimed clean for these fixtures. They are never adopted into customer CAD.'}
(out/'controls.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({'baseline_passed':baseline['passed'],'missing_UUID_rejected':not missing_result['passed'],'same_net_join_rejected':not join_result['passed'],'source_unchanged':True}))

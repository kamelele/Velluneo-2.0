"""Read-only new22-net matrix adapter to the previously qualified native polygon kernel."""
from pathlib import Path
import sys,json,hashlib,itertools
H=Path(__file__).resolve().parent;S=H.parents[3]/'variants/integrated-shade/SC10_TME'
sys.path.insert(0,str(H))
import checker as old
q=old.q;k=old.k
load=lambda p:json.loads(p.read_text(encoding='utf-8-sig'))
class Contract:
 def __init__(self,board):
  g=load(S/'intended-connectivity.TME-A.json'); m=load(S/'functional-spacing-targets.json')
  self.expected={(p['ref'],p['pin']):'/'+n['id']for n in g['nets']for p in n['pins']}
  self.mapping={n:n for n in set(self.expected.values())}
  native_pads={(f.GetReference(),p.GetNumber()):p for f in board.GetFootprints()for p in f.Pads()}
  for n in g['no_connect']:
   key=(n['ref'],n['pin']);actual_name=native_pads[key].GetNetname()
   # A KiCad generated NC name includes the symbol-pin function. Match identity,
   # require a private singleton pad net, then normalize only its display name.
   assert actual_name.startswith('unconnected-(T1-')and actual_name.endswith('-Pad'+n['pin']+')')
   assert sum(p.GetNetname()==actual_name for p in native_pads.values())==1
   self.expected[key]=actual_name;self.mapping[actual_name]=f'unconnected-(T1-Pad{n["pin"]})'
  self.refs={r for r,p in self.expected};self.nets=set(self.mapping.values())
  assert len(self.nets)==22 and len(self.expected)==65 and len(self.refs)==25
  self.matrix={frozenset([r['net_a'],r['net_b']]):{'surface_creepage_target_mm':r['target_mm'],'route_clearance_target_mm':r['target_mm']}for r in m['pairs']}
  assert set(self.matrix)=={frozenset(p)for p in itertools.combinations(self.nets,2)}
  self.minimum={'track_width':.3,'hole_size':.3,'annular_width':.2,'edge_clearance':1.};self.exceptions=[];self.areas=[];self.outline=None
 def gap(self,a,b):return 0. if a==b else self.matrix[frozenset([a,b])]['surface_creepage_target_mm']
 def width(self,n):return .3
class Checker(old.Checker):
 def collect(self):
  super().collect(); self.exact_integer_via_checks=[]
  via={t.m_Uuid.AsString():t for t in self.board.GetTracks()if isinstance(t,k.PCB_VIA)}
  remaining=[]
  for f in self.findings:
   if f['type']=='via_drill_or_annulus':
    t=via[f['uuid']];diameter=min(t.GetWidth(l)for l in [k.F_Cu,k.B_Cu]);drill=t.GetDrillValue()
    # Avoid false.7-.3binaryfloat annulus failure. Compare exact native nanometres.
    passed=drill>=k.FromMM(self.c.minimum['hole_size'])and diameter-drill>=2*k.FromMM(self.c.minimum['annular_width'])
    self.exact_integer_via_checks.append({'uuid':f['uuid'],'diameter_nm':diameter,'drill_nm':drill,'required_annulus_nm':k.FromMM(self.c.minimum['annular_width']),'passed':passed,'reason':'Replacesfloatingpointsubtractionwithstrictnativeintegercomparison; no tolerance relaxation.'})
    if passed:continue
   remaining.append(f)
  self.findings=remaining
def run():
 p=S/'Plytka_TME.kicad_pcb';before=q.sha(p);r={'actual_actor':'/root','board_sha256':before,'checker_sha256':q.sha(__file__),'reused_kernel_sha256':q.sha(H/'kernel_sc08.py'),'matrix_sha256':q.sha(S/'functional-spacing-targets.json'),'limits':['Same-face planar native outwardpolygon2um approximation, not normative creepage/3Dinsulationcompliance.','Noexceptions or waivedpackages. All231pairs/22nets include7NCwindingterminals.','No source propagation or CADmutation; rawsavedtracknets must equal loadednativeidentities.'],'approvals':None}
 try:
  assert k.GetBuildVersion()=='10.0.6'; b=q.load_native(p);c=Contract(b)
  assert q.raw_track_nets(p)=={t.m_Uuid.AsString():t.GetNetname()for t in b.GetTracks()}
  ck=Checker(b,c);out=ck.run();out['exact_integer_via_checks']=ck.exact_integer_via_checks;out['pair_minima']=out.pop('all_55_pair_minima');out['NC_routing_violations']=[t.m_Uuid.AsString()for t in b.GetTracks()if t.GetNetname().startswith('unconnected-')]
  if out['NC_routing_violations']:out['passed']=False
  r.update(out)
 except Exception as e:r.update(passed=False,stopped=True,error=type(e).__name__+': '+str(e))
 r.update(input_unchanged=q.sha(p)==before)
 if not r['input_unchanged']:r['passed']=False
 (H/'spacing-report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({key:r.get(key)for key in ['passed','stopped','error','input_unchanged','copper_edge_minimum','stats']}));print('findings',len(r.get('findings',[])))
if __name__=='__main__':run()

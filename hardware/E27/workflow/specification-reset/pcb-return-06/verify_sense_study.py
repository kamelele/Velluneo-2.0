"""Saved study pin parity and limited branch topology, not operating qualification."""
from pathlib import Path
import json,math,pcbnew,importlib.util
D=Path(__file__).resolve().parent;E=D/'design';S=D/'studies/sense';spec=importlib.util.spec_from_file_location('g',E/'full_geometry.py');g=importlib.util.module_from_spec(spec);spec.loader.exec_module(g)
main=pcbnew.LoadBoard(str(E/'Velluneo_specification_reset.kicad_pcb'));study=pcbnew.LoadBoard(str(S/'Velluneo_sense_exploration.kicad_pcb'));assert not list(main.GetTracks())
def members(b):return{f.GetReference()+'.'+p.GetNumber():(p.GetNetname(),p.GetPosition().x,p.GetPosition().y,p.GetSize().x,p.GetSize().y,p.GetDrillSize().x,p.GetDrillSize().y,int(p.GetShape()),int(p.GetAttribute()),tuple(p.GetLayerSet().Seq()))for f in b.GetFootprints()for p in f.Pads()}
assert members(main)==members(study)and len(members(main))==81
assert{f.GetReference():(f.GetValue(),f.GetFieldText('MPN'),f.GetFPID().GetLibItemName().c_str())for f in main.GetFootprints()}=={f.GetReference():(f.GetValue(),f.GetFieldText('MPN'),f.GetFPID().GetLibItemName().c_str())for f in study.GetFootprints()}
model_count=0
for f in study.GetFootprints():
 for model in f.Models():
  assert model.m_Filename.startswith('${KIPRJMOD}/../../design/models/');assert(S/model.m_Filename.removeprefix('${KIPRJMOD}/')).resolve().is_file();model_count+=1
assert model_count==33
tracks=list(study.GetTracks());assert len(tracks)>8 and sum(isinstance(t,pcbnew.PCB_VIA)for t in tracks)==5
sets={}
for t in tracks:sets.setdefault(t.GetNetname(),[]).append(t)
assert len([t for t in sets['/SENSE']if t.GetLayer()==pcbnew.F_Cu])==6 and len(sets['/CS'])==1
def xy(p):return pcbnew.ToMM(p.x)-100,pcbnew.ToMM(p.y)-100
edges=[(xy(t.GetStart()),xy(t.GetEnd()))for t in sets['/SENSE']if t.GetLayer()==pcbnew.F_Cu];degrees={}
for a,b in edges:
 for p in(a,b):key=tuple(round(n,6)for n in p);degrees[key]=degrees.get(key,0)+1
assert sorted(degrees.values())==[1,1,2,2,2,2,2]
assert{p for p,k in degrees.items()if k==1}=={tuple(round(n,6)for n in g.centres[p])for p in('R9.1','R6.1')}
length=sum(math.dist(a,b)for a,b in edges);rho=1.724e-8;return_r20=rho*.0027/(.001*35e-6);return_r100=return_r20*(1+.00393*80)
noise=[]
for cap_pf in(.01,.03,.1,.3,1.):
 for dv in(5,10,20):noise.append(dict(assumed_coupling_pF=cap_pf,assumed_dv_dt_V_per_ns=dv,first_order_shunt_voltage_disturbance_V=cap_pf*1e-12*dv*1e9*2.32))
out=dict(native_main_and_study_pad_memberships_and_geometry_identical=True,components=33,pads=81,main_tracks=0,all33study_model_paths_resolve=True,study_track_segments=len(tracks)-5,study_vias=5,SENSE_only_two_branch_endpoints=['R9.1','R6.1'],SENSE_actual_track_length_mm=length,CS_actual_track_length_mm=sets['/CS'][0].GetLength()/1e6,shunt_return_actual_track_length_mm=2.7,shunt_return_width_mm=1.,assumed_finished_copper_um=35,conditional_return_R20_ohm=return_r20,conditional_return_R100_ohm=return_r100,conditional_return_drop_at_assumed_p35855_A_V=return_r100*.35855,SENSE_conditional_dc_resistance20_ohm=rho*(length/1000)/(.0004*35e-6),coupling_sensitivity=noise,proposed_noise_allocation_V=.002,max_coupling_for2mV_at10Vns_and2p32ohm_pF=.002/(10e9*2.32)*1e12,actual_coupling_extracted=False,complete_GND_driver_return_routed=False,accepted_routing=False,scope='Saved native branch/graph evidence and conditional resistance/coupling sensitivity only.35um is assumed not confirmed stackup; fringing/inductance/return sharing/actual waveforms remain unverified. No IC simulation or powered tests.')
(S/'verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8',newline='\n');print(json.dumps({k:v for k,v in out.items()if k!='coupling_sensitivity'},indent=2))

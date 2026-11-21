from pathlib import Path
import json,hashlib,shutil,os,pcbnew as k
R=Path(__file__).resolve().parents[2]/'Velluneo-2.0';S=Path(__file__).resolve().parent/'project';D=Path(__file__).resolve().parent/'routing';out=D;out.mkdir(exist_ok=True)
src=Path(os.environ['SC09_ROUTE_BOARD']);b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(src));assert len(list(b.GetTracks()))==0,'Never reset routed board';shutil.copy2(src,out/'unrouted-baseline.kicad_pcb')
fps={f.GetReference():f for f in b.GetFootprints()};pads={(r,p.GetNumber()):p for r,f in fps.items() for p in f.Pads()};v=lambda x,y:k.VECTOR2I(k.FromMM(x+100),k.FromMM(y+100));pos=lambda r,n:tuple(round(k.ToMM(t)-100,5) for t in [pads[r,str(n)].GetPosition().x,pads[r,str(n)].GetPosition().y]);before={a:p.GetNetname() for a,p in pads.items()};tracks=[]
def route(r,n,points,layer=k.B_Cu,width=.4,name=''):
 net=pads[r,str(n)].GetNet()
 for a,c in zip(points,points[1:]):
  if a==c:continue
  t=k.PCB_TRACK(b);t.SetNet(net);t.SetLayer(layer);t.SetWidth(k.FromMM(width));t.SetStart(v(*a));t.SetEnd(v(*c));b.Add(t);tracks.append({'uuid':t.m_Uuid.AsString(),'net':net.GetNetname(),'a':a,'b':c,'layer':b.GetLayerName(layer),'width':width,'function':name})
def via(r,n,p):
 t=k.PCB_VIA(b);t.SetNet(pads[r,str(n)].GetNet());t.SetViaType(k.VIATYPE_THROUGH);t.SetLayerPair(k.F_Cu,k.B_Cu);t.SetPosition(v(*p));t.SetWidth(k.FromMM(.8));t.SetDrill(k.FromMM(.3));b.Add(t);tracks.append({'uuid':t.m_Uuid.AsString(),'net':t.GetNetname(),'point':p,'type':'via'})
# Manufacturer-package breakout only. Free-board targets apply beyond frozen scopes.
route('BR1',1,[pos('BR1',1),(4.5,12.7)],name='bridge_positive_escape')
route('BR1',3,[pos('BR1',3),(8.4,12.625),(8.4,10.8)],name='bridge_return_escape')
route('BR1',2,[pos('BR1',2),(3.85,18.1)],name='bridge_phase_escape')
route('BR1',4,[pos('BR1',4),(10.6,18.1),(10.6,14.6)],name='bridge_neutral_escape')
route('U1',4,[pos('U1',4),(46.65,7.68),(48.4,9.1)],name='drain_escape');via('U1',4,(48.4,9.1))
route('U1',3,[pos('U1',3),(45.45,6.335),(45.45,5.0),(44.8,4.5)],name='feedback_Kelvin_escape');via('U1',3,(44.8,4.5))
route('U1',2,[pos('U1',2),(48.5,5.065)],width=.3,name='monitor_escape');via('U1',2,(48.5,5.065))
# Short, actual bypass connection; source rail is a separate broad path around sense pads.
route('C5',1,[pos('C5',1),(46.725,1.725),pos('U1',1)],width=.3,name='BP_decoupling')
for n in [5,6,7,8]:route('U1',n,[pos('U1',n),(40.5,pos('U1',n)[1])],width=.6,name='SOURCE_common_pins')
route('U1',5,[(40.5,7.605),(40.5,3.795)],width=.6,name='SOURCE_low_resistance_trunk')
route('C5',2,[pos('C5',2),(48.85,2.9)],width=.4,name='SOURCE_bypass_escape');via('C5',2,(48.85,2.9))
route('R5',1,[(31.5,3.5),pos('R5',1)],width=.6,name='SOURCE_R5_branch')
route('R5',2,[pos('R5',2),(38.65,3.5),(39.15,3)],width=.4,name='sense_to_power_inductor_star')
route('R6',2,[pos('R6',2),(37.8,6),(38.65,5.15),(38.65,3.5)],width=.4,name='parallel_current_sense')
route('J1',1,[pos('J1',1),pos('RF1',1)],k.B_Cu,.4,'AC_L_short_new_bare_wire_port')
route('R7',1,[pos('R7',1),(35,6.5),(48.5,6.5),(48.5,5.065)],k.F_Cu,.3,'local_standing_OVP_M')
route('R7',2,[pos('R7',2),pos('T1',1)],k.F_Cu,.3,'local_standing_LED')
route('C4',1,[(48.4,9.1),(48.4,10.2),(48.4,14),pos('C4',1)],k.F_Cu,.4,'short_HF_BUS_to_drain')
route('D1',2,[pos('D1',2),pos('C4',2)],k.B_Cu,.4,'short_HF_diode_to_bus_cap')
route('D1',1,[pos('T1',2),(43.2,2.9)],k.F_Cu,.4,'power_cathode_to_catalogue_inductor_front');via('D1',1,(43.2,2.9))
route('D1',1,[(43.2,2.9),pos('D1',1)],k.B_Cu,.4,'power_cathode_to_inductor_back')
route('U1',5,[pos('U1',5),(40.5,7.45),(33.425,7.45),pos('R6',1)],k.B_Cu,.4,'short_SOURCE_force_path')
route('R4',1,[pos('R4',1),pos('R7',1)],k.B_Cu,.3,'local_M_divider')
route('R4',2,[pos('R4',2),(31.5,6)],k.B_Cu,.3,'local_SOURCE_divider')
route('L1',2,[pos('L1',2),(9,25.8),(42,25.8),(44,24.9),(49.1,24.9),(49.1,17),pos('C4',1)],k.F_Cu,.3,'low_frequency_filtered_feed_outside_HF_loop')
route('RF1',2,[pos('RF1',2),(45.7,20.3),(35,20.3),pos('RV1',1)],k.B_Cu,.3,'fused_input_to_MOV')
route('BR1',2,[pos('BR1',2),(4,17)],k.B_Cu,.3,'fused_bridge_escape');via('BR1',2,(4,17))
route('BR1',2,[(4,17),(13.2,15.5),pos('RV1',1)],k.F_Cu,.3,'fused_input_bridge_feed')
route('BR1',1,[(4.5,12.7),(1.1,13.6),(1.1,22.2),pos('L1',1)],k.B_Cu,.3,'rectified_bus_left_perimeter')
route('L1',1,[pos('L1',1),(7,18.9),(17.5,18.9),pos('C1',1)],k.F_Cu,.3,'input_filter_cap_bus')
via('R5',2,(39.15,3))
route('R5',2,[(39.15,3),pos('T1',2)],k.F_Cu,.4,'sense_force_to_catalogue_coil')
route('R5',2,[pos('R5',2),(37,2.4)],k.B_Cu,.3,'Kelvin_tap_at_R5_pad');via('R5',2,(37,2.4))
route('R5',2,[(37,2.4),(37,4.5),(44.8,4.5)],k.F_Cu,.3,'Kelvin_separate_below_catalogue_power_pad')
route('U1',5,[(31.5,3.5),(31.5,6),pos('R6',1)],k.B_Cu,.4,'SOURCE_sense_star_no_top_via')
route('C5',2,[(48.85,2.9),(47.3,2.9),(47.3,5.6),(40,5.6)],k.F_Cu,.4,'SOURCE_bypass_between_new_pads');via('C5',2,(40,5.6))
route('C5',2,[(40,5.6),(40.5,5.6)],k.B_Cu,.4,'SOURCE_bypass_to_common_IC_trunk')
# Save in a candidate first, then reject any native ownership/net propagation.
candidate=out/'seed-native.kicad_pcb';assert k.SaveBoard(str(candidate),b,True);saved=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(candidate))
after={(f.GetReference(),p.GetNumber()):p.GetNetname() for f in saved.GetFootprints() for p in f.Pads()};assert before==after,'Native save changed pad net!'
savedtracks={t.m_Uuid.AsString():t.GetNetname() for t in saved.GetTracks()};assert all(savedtracks[t['uuid']]==t['net'] for t in tracks),'Native save changed track net!'
shutil.copy2(candidate,src);(out/'seed-authoring.json').write_text(json.dumps({'kind':'Rootauthoredprotectedcriticalpaths,actualpad/tracknetinvariancechecked','source_sha256':hashlib.sha256(src.read_bytes()).hexdigest(),'tracks':tracks,'pad_net_invariance':True,'track_net_invariance':True},indent=2)+'\n')
print('Saved protected seed',len(tracks),'native copper objects; all46pad nets preserved')


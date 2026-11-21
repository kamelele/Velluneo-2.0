from pathlib import Path
import pcbnew as p,json,shutil
W=Path(__file__).resolve().parent;D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/supplier-review-13';E=D/'design';B=E/'Velluneo_driver.kicad_pcb';b=p.LoadBoard(str(B));moves=[];endmoves=[]
for ref,dx,dy in [('R10',-.5,0),('C3',0,.6),('R17',0,.4)]:
 f=next(x for x in b.GetFootprints()if x.GetReference()==ref);old={q.GetNumber():(q.GetPosition().x,q.GetPosition().y,q.GetNetname())for q in f.Pads()};pos=f.GetPosition();f.SetPosition(p.VECTOR2I(pos.x+p.FromMM(dx),pos.y+p.FromMM(dy)));new={q.GetNumber():(q.GetPosition().x,q.GetPosition().y)for q in f.Pads()}
 for t in b.GetTracks():
  for num,(x,y,net)in old.items():
   if t.GetNetname()!=net:continue
   if isinstance(t,p.PCB_VIA):
    if(t.GetPosition().x,t.GetPosition().y)==(x,y):t.SetPosition(p.VECTOR2I(*new[num]));endmoves.append(dict(ref=ref,pin=num,via=True))
   else:
    for end in('Start','End'):
     q=getattr(t,'Get'+end)()
     if(q.x,q.y)==(x,y):getattr(t,'Set'+end)(p.VECTOR2I(*new[num]));endmoves.append(dict(ref=ref,pin=num,endpoint=end,uuid=t.m_Uuid.AsString()))
 moves.append(dict(ref=ref,before_mm=[pos.x/1e6,pos.y/1e6],after_mm=[f.GetPosition().x/1e6,f.GetPosition().y/1e6],reason='FinishedT1reservation'if ref=='R10'else'P/Sfinishedmetalspacingreserve'))
f=next(x for x in b.GetFootprints()if x.GetReference()=='T1');p.FootprintSave(str(E/'Velluneo_ECO04.pretty'),f)
companions={ext:B.with_suffix(ext).read_bytes()for ext in('.kicad_pro','.kicad_sch','.kicad_dru')};p.SaveBoard(str(B),b)
for ext,raw in companions.items():B.with_suffix(ext).write_bytes(raw)
(D/'checks/local-placement-refinement.json').write_text(json.dumps(dict(moves=moves,attached_copper_endpoints=endmoves,circuit_pin_number_value_MPN_changes=False,first_probe='probe-drc.json',status='Candidate awaiting freshstrictDRC; no waiver or rulefloorreduction.'),indent=2)+'\n')
probe=D/'.work/probe2';probe.mkdir(parents=True,exist_ok=True)
for ext in('.kicad_pcb','.kicad_pro','.kicad_sch','.kicad_dru'):shutil.copyfile(B.with_suffix(ext),probe/B.with_suffix(ext).name)
q=probe/'Velluneo_driver.kicad_dru';q.write_text(q.read_text().replace('10.000000mm','10.700000mm'))
for n in('fp-lib-table','sym-lib-table'):shutil.copyfile(E/n,probe/n)
for n in('libraries','Velluneo_ECO04.pretty'):shutil.copytree(E/n,probe/n,dirs_exist_ok=True)
print('Moved3parts withconnectedpadendpointsfollowing; pinmapandMPNs unchanged.')

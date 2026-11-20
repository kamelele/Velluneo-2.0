from pathlib import Path
import pcbnew as p,json,shutil,hashlib
W=Path(__file__).resolve().parent;P=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset';D=P/'supplier-review-13';E=D/'design';B=E/'Velluneo_driver.kicad_pcb';b=p.LoadBoard(str(B));f=next(x for x in b.GetFootprints()if x.GetReference()=='T1')
def xy(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
before=B.read_bytes();(D/'evidence/source-before-refinement.kicad_pcb').write_bytes(before)
for g in f.GraphicalItems():
 if g.GetLayer()==p.F_CrtYd:g.SetStart(xy(84.75,77.75));g.SetEnd(xy(115.25,108.25))
g=p.PCB_SHAPE(f);g.SetShape(p.SHAPE_T_RECT);g.SetLayer(p.F_Fab);g.SetStart(xy(85,78));g.SetEnd(xy(115,108));g.SetWidth(p.FromMM(.10));f.Add(g)
name='TDK_EFD25_FINISHED30x30_RESERVATION';f.SetFPID(p.LIB_ID('Velluneo_ECO04',name));f.SetLibDescription('Finished30x30mm maximum body reservation with0.25mmcourtyard margin; supplier-confirmation required. Pads/pins unchanged.')
old=E/'Velluneo_ECO04.pretty/TDK_EFD25_Pad2p0_PROJECT.kicad_mod';text=old.read_text().replace('"TDK_EFD25_Pad2p0_PROJECT"','"'+name+'"').replace('(start -12.85 -13.25)','(start -15.25 -15.25)').replace('(end 12.85 13.25)','(end 15.25 15.25)');(E/'Velluneo_ECO04.pretty'/(name+'.kicad_mod')).write_text(text,encoding='utf-8')
# Controlled single AUX_RAW corner move adds finished-spacing reserve without changing topology.
changed=[]
for t in b.GetTracks():
 if isinstance(t,p.PCB_VIA)or t.GetNetname()!='/AUX_RAW':continue
 for end in('Start','End'):
  q=getattr(t,'Get'+end)()
  if q==xy(88.1,93.0):getattr(t,'Set'+end)(xy(88.1,93.6));changed.append(dict(uuid=t.m_Uuid.AsString(),endpoint=end,before_mm=[88.1,93.0],after_mm=[88.1,93.6]))
assert len(changed)==2,changed
companions={ext:B.with_suffix(ext).read_bytes()for ext in('.kicad_pro','.kicad_sch','.kicad_dru')};p.SaveBoard(str(B),b)
for ext,raw in companions.items():B.with_suffix(ext).write_bytes(raw)
sch=B.with_suffix('.kicad_sch');s=sch.read_text();oldid='Velluneo_ECO04:TDK_EFD25_Pad2p0_PROJECT';assert s.count(oldid)==1;s=s.replace(oldid,'Velluneo_ECO04:'+name);sch.write_text(s,encoding='utf-8')
(D/'checks/native-refinement.json').write_text(json.dumps(dict(T1_finished_max_body_mm=[30,30,18],courtyard_size_mm=[30.5,30.5],basis='Conservativeprocurementenvelope, not verifiedfinishedcomponent. Rawformergraphicretained; supplierdrawingmustfitreservation.',AUX_RAW_corner=changed,circuit_or_pad_changes=False),indent=2)+'\n')
probe=D/'.work/probe';probe.mkdir(parents=True,exist_ok=True)
for ext in('.kicad_pcb','.kicad_pro','.kicad_sch','.kicad_dru'):shutil.copyfile(B.with_suffix(ext),probe/B.with_suffix(ext).name)
q=probe/'Velluneo_driver.kicad_dru';q.write_text(q.read_text().replace('10.000000mm','10.700000mm'))
for n in('fp-lib-table','sym-lib-table'):shutil.copyfile(E/n,probe/n)
for n in('libraries','Velluneo_ECO04.pretty'):shutil.copytree(E/n,probe/n,dirs_exist_ok=True)
print('Candidate33/81samepins: finishedT1reservation and AUXcorner; probe3/10.7mm only.')

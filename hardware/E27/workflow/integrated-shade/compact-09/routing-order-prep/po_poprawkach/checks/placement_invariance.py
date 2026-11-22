from pathlib import Path
import json,hashlib,pcbnew as k
H=Path(__file__).resolve().parent;ROOT=H.parents[1];R=ROOT/'work/Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';B=H/'baseline-source';C=R/'hardware/E27/workflow/integrated-shade/compact-09/routing-order-prep/po_poprawkach/checks'
def capture(p):
 b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(p));parts={}
 for f in b.GetFootprints():
  parts[f.GetReference()]={'at':[f.GetPosition().x,f.GetPosition().y],'angle':f.GetOrientationDegrees(),'layer':f.GetLayer(),'FPID':[f.GetFPID().GetLibNickname(),f.GetFPID().GetLibItemName()],'value':f.GetValue(),'fields':dict(f.GetFieldsText()),'DNP':f.IsDNP(),'models':[m.m_Filename for m in f.Models()],'pads':{q.GetNumber():{'at':[q.GetPosition().x,q.GetPosition().y],'size':[q.GetSize().x,q.GetSize().y],'shape':int(q.GetShape()),'angle':q.GetOrientationDegrees(),'drill':[q.GetDrillSize().x,q.GetDrillSize().y],'net':q.GetNetname()}for q in f.Pads()}}
 vs={t.m_Uuid.AsString():[k.ToMM(t.GetPosition().x),k.ToMM(t.GetPosition().y),k.ToMM(t.GetWidth(k.F_Cu)),k.ToMM(t.GetDrill()),t.GetNetname()]for t in b.GetTracks()if isinstance(t,k.PCB_VIA)}
 coords=[x.GetStart()for x in b.GetDrawings()if x.GetLayer()==k.Edge_Cuts];outline=[min(k.ToMM(x.x)for x in coords),min(k.ToMM(x.y)for x in coords),max(k.ToMM(x.x)for x in coords),max(k.ToMM(x.y)for x in coords)]
 return parts,vs,outline
old,ov,oe=capture(B/'SC09_compact.kicad_pcb');new,nv,ne=capture(S/'SC09_compact.kicad_pcb');assert old==new and len(nv)==len(ov)==10 and ov.keys()==nv.keys()
changed={u:{'before':ov[u],'after':nv[u]}for u in ov if ov[u]!=nv[u]};u='d355cf10-6774-48cf-99c2-adaaa67f5a00';assert list(changed)==[u];assert ov[u]==[121.2,116.2,.75,.3,'/DC_RETURN']and nv[u]==[122.6,116.2,.75,.3,'/DC_RETURN'];assert ne==[99.4,99.4,150.6,132.4]
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();C.mkdir(parents=True,exist_ok=True);(C/'placement-invariance.json').write_text(json.dumps({'actual_actor':'/root','before_PCB_sha256':sha(B/'SC09_compact.kicad_pcb'),'after_PCB_sha256':sha(S/'SC09_compact.kicad_pcb'),'passed':True,'refs':len(new),'physical_pads':sum(len(x['pads'])for x in new.values()),'all_footprints_pads_models_fields_MPNs_values_exactly_unchanged':True,'nine_other_vias_exactly_unchanged':True,'authorized_via_change':changed,'outline_before_mm':oe,'outline_after_mm':ne,'measurements_performed':False},indent=2)+'\n');print('19parts46pads unchanged; preciselyone authorizedviamove; outline51.2x33')

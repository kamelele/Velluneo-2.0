from pathlib import Path
import json,hashlib,pcbnew as k
ROOT=Path(__file__).resolve().parents[2];R=ROOT/'work/Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';C=R/'hardware/E27/workflow/integrated-shade/compact-09/routing-junctions/po_poprawkach/checks';B=ROOT/'work/routing03/baseline-source/SC09_compact.kicad_pcb';A=S/'SC09_compact.kicad_pcb'
def capture(p):
 b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(p));parts={}
 for f in b.GetFootprints():
  parts[f.GetReference()]={'at':[f.GetPosition().x,f.GetPosition().y],'angle':f.GetOrientationDegrees(),'layer':f.GetLayer(),'FPID':[f.GetFPID().GetLibNickname(),f.GetFPID().GetLibItemName()],'value':f.GetValue(),'fields':dict(f.GetFieldsText()),'DNP':f.IsDNP(),'models':[m.m_Filename for m in f.Models()],'pads':{q.GetNumber():{'at':[q.GetPosition().x,q.GetPosition().y],'size':[q.GetSize().x,q.GetSize().y],'shape':int(q.GetShape()),'angle':q.GetOrientationDegrees(),'drill':[q.GetDrillSize().x,q.GetDrillSize().y],'net':q.GetNetname()}for q in f.Pads()}}
  outlines=sorted((x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y,x.GetWidth())for x in b.GetDrawings()if x.GetLayer()==k.Edge_Cuts)
 return parts,outlines
old,oe=capture(B);new,ne=capture(A);assert old==new and oe==ne
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();C.mkdir(parents=True,exist_ok=True);(C/'placement-invariance.json').write_text(json.dumps({'actual_actor':'/root','before_PCB_sha256':sha(B),'after_PCB_sha256':sha(A),'passed':True,'parts':len(new),'pads':sum(len(x['pads'])for x in new.values()),'exact_native_footprint_and_pad_geometry_values_MPN_models_equal':True,'exact_outline_equal':True,'physical_measurements':False},indent=2)+'\n');print('Nativeplacements/pads/models/MPNs/outlineexactlyunchanged',len(new),'refs')

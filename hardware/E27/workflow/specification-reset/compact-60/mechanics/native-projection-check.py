"""Compare analytical saved pad boxes to native KiCad transforms; no board saved."""
from pathlib import Path
import pcbnew,json,math
D=Path(__file__).resolve().parent;P=D.parents[1]
i=json.loads((D/'native-inventory.json').read_text(encoding='utf-8'));r=json.loads((D/'packing-diagnostic.json').read_text(encoding='utf-8'));fixtures=[];checked=[]
for part in i['parts']:
 ref=part['ref'];c=r['positions'][ref];name=part['footprint'].split(':')[1];f=pcbnew.FootprintLoad(str(P/'libraries/Velluneo_Driver.pretty'),name);assert f
 # Flip requires a parent board. This ephemeral single-footprint fixture is never saved or supplied to product checks.
 fixture=pcbnew.BOARD();fixture.Add(f);fixtures.append(fixture)
 if c['side']=='B':f.Flip(pcbnew.VECTOR2I(0,0),True)
 f.Rotate(pcbnew.VECTOR2I(0,0),pcbnew.EDA_ANGLE(c['angle_deg'],pcbnew.DEGREES_T));f.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(c['x_mm']),pcbnew.FromMM(c['y_mm'])))
 expected={p['pin']:b for p,b in zip(part['pads'],c['pads'])}
 for pad in f.Pads():
  b=expected[pad.GetNumber()];xy=[pcbnew.ToMM(pad.GetPosition().x),pcbnew.ToMM(pad.GetPosition().y)];angle=pad.GetOrientation().AsDegrees()%180;w,h=[pcbnew.ToMM(v)for v in[pad.GetSize().x,pad.GetSize().y]]
  assert min(abs(angle),abs(angle-90),abs(angle-180))<1e-6
  if abs(angle-90)<1e-6:w,h=h,w
  observed=[xy[0]-w/2,xy[1]-h/2,xy[0]+w/2,xy[1]+h/2];delta=max(abs(a-bb)for a,bb in zip(observed,b));assert delta<2e-6,(ref,pad.GetNumber(),observed,b,angle)
  checked.append({'ref':ref,'pin':pad.GetNumber(),'max_bbox_delta_mm':delta})
print(json.dumps({'native_pcbnew':pcbnew.Version(),'scope':'Actual native Flip/Rotate/position comparison in ephemeral geometry fixtures; no board saved, no product placement/DRC or functional approval.','checked_physical_pads':len(checked),'maximum_delta_mm':max(v['max_bbox_delta_mm']for v in checked),'checks':checked},indent=2))

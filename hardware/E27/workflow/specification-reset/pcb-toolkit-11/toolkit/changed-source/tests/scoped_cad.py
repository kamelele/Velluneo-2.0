"""Synthetic native4-layer controls. No customer geometry or actual approvals."""
from pathlib import Path
import sys,json,subprocess,hashlib,copy,uuid,os
import pcbnew as pcb
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'scripts'));import pcb_rules,scoped_policy,spatial,spatial_cad
WORK=ROOT/'.work/scoped-native';WORK.mkdir(parents=True,exist_ok=True);CLI=pcb_rules.cli_path(None);results=[]
def mm(x,y):return pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y))
config={'name':'scope','fabrication':{'vendor':'jlcpcb'},'assembly':{'mode':'supplier'},'product':{'minimums_mm':{'clearance':.25,'track_width':.3,'hole_size':.3,'annular_width':.2,'edge_clearance':.5},'copper_layers':['F.Cu','In1.Cu','In2.Cu','B.Cu'],'scoped_clearances':[{'id':'HVQ','nets_a':['H'],'nets_b':['Q'],'min_mm':3},{'id':'PS','nets_a':['H','Q'],'nets_b':['S'],'min_mm':10}]}}
values=pcb_rules.resolve(config)[2];project=pcb_rules.project_settings('scope',values,[])
area={'id':'ISOLATION','rectangle_mm':[0,25,60,30],'layers':['F.Cu','In1.Cu','In2.Cu','B.Cu'],'basis':'Synthetic native regression only','disallow':['track','via','pad','zone'],'exceptions':[]}
model={'payload':{'outline_mm':[0,0,60,40],'areas':[area],'copper_layers':['F.Cu','In1.Cu','In2.Cu','B.Cu'],'net_settings':project['net_settings']}}
def board(kind):
    folder=WORK/kind;folder.mkdir(exist_ok=True);b=pcb.BOARD();b.SetCopperLayerCount(4);nets={}
    for name in ['H','Q','S']:
        n=pcb.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
    for a,z in [((0,0),(60,0)),((60,0),(60,40)),((60,40),(0,40)),((0,40),(0,0))]:
        t=pcb.PCB_SHAPE(b);t.SetShape(pcb.SHAPE_T_SEGMENT);t.SetLayer(pcb.Edge_Cuts);t.SetStart(mm(*a));t.SetEnd(mm(*z));t.SetWidth(pcb.FromMM(.05));b.Add(t)
    positions={'H':10,'Q':16.6 if kind=='negative3' else 20,'S':33.6 if kind=='negative10' else 40}
    for ref,(name,x)in enumerate(positions.items(),1):
        f=pcb.FOOTPRINT(b);f.SetReference('X'+str(ref));f.SetPosition(mm(x,10));f.Reference().SetVisible(False);f.Value().SetVisible(False)
        for number,dx in [('1',0),('2',3)]:
            p=pcb.PAD(f);p.SetNumber(number);p.SetShape(pcb.PAD_SHAPE_CIRCLE);p.SetAttribute(pcb.PAD_ATTRIB_PTH);p.SetSize(mm(.7,.7));p.SetDrillSize(mm(.3,.3));p.SetLayerSet(pcb.LSET.AllCuMask());p.SetPosition(mm(x+dx,10));p.SetNet(nets[name]);f.Add(p)
        for a,z in [((x-.6,9.4),(x+3.6,9.4)),((x+3.6,9.4),(x+3.6,10.6)),((x+3.6,10.6),(x-.6,10.6)),((x-.6,10.6),(x-.6,9.4))]:
            sh=pcb.PCB_SHAPE(f);sh.SetShape(pcb.SHAPE_T_SEGMENT);sh.SetLayer(pcb.F_CrtYd);sh.SetStart(mm(*a));sh.SetEnd(mm(*z));sh.SetWidth(pcb.FromMM(.05));f.Add(sh)
        b.Add(f);t=pcb.PCB_TRACK(b);t.SetLayer(pcb.In1_Cu);t.SetWidth(pcb.FromMM(.3));t.SetStart(mm(x,10));t.SetEnd(mm(x+3,10));t.SetNet(nets[name]);b.Add(t)
    if kind in('negativeInner1','negativeInner2'):
        t=pcb.PCB_TRACK(b);t.SetLayer(pcb.In1_Cu if kind=='negativeInner1'else pcb.In2_Cu);t.SetWidth(pcb.FromMM(.3));t.SetStart(mm(10,27));t.SetEnd(mm(20,27));t.SetNet(nets['H']);b.Add(t)
    path=folder/'scope.kicad_pcb';pcb.SaveBoard(str(path),b);(folder/'scope.kicad_pro').write_text(json.dumps(project,indent=2)+'\n');(folder/'scope.kicad_dru').write_text(pcb_rules.dru(values)+spatial.rules(model)+scoped_policy.rules(config))
    # Exercise the real spatial reader/writer: proposed named area must use all4native layers.
    output=folder/'proposal.json';spatial_cad.run({'board':str(path),'model':model,'propose':True},output);result=json.loads(output.read_text());assert not result['errors'],result['errors'];assert result['proposed_board']
    import base64;path.write_bytes(base64.b64decode(result['proposed_board']));b=pcb.LoadBoard(str(path));z=next(iter(b.Zones()));assert {b.GetLayerName(l)for l in z.GetLayerSet().Seq()}==set(area['layers'])
    return folder,path
for kind in('clean','negative3','negative10','negativeInner1','negativeInner2'):
    folder,path=board(kind);out=folder/'drc.json';r=subprocess.run([CLI,'pcb','drc','--format','json','--severity-all','--output',str(out),str(path)],capture_output=True,text=True,encoding='utf-8',errors='replace',timeout=120);assert r.returncode==0,(r.stdout,r.stderr);j=json.loads(out.read_text());types=[v['type']for v in j['violations']]
    if kind=='clean':assert not types,(types,j['violations'])
    elif kind in('negative3','negative10'):assert 'clearance'in types,(kind,types)
    else:assert any('disallow'in t or 'not_allowed'in t for t in types),(kind,types)
    results.append({'name':kind,'passed':True,'types':types,'report_sha256':hashlib.sha256(out.read_bytes()).hexdigest()});print(kind,types,flush=True)
folder,path=board('disabledLayer');b=pcb.LoadBoard(str(path));b.SetCopperLayerCount(2);pcb.SaveBoard(str(path),b);before=path.read_bytes();rejected=False
try:spatial_cad.run({'board':str(path),'model':model,'propose':True},folder/'disabled.json')
except ValueError:rejected=True
assert rejected and path.read_bytes()==before;results.append({'name':'disabledLayer','passed':True,'before_mutation_rejection':True})
(ROOT/'reports').mkdir(exist_ok=True);(ROOT/'reports/scoped-integration-results.json').write_text(json.dumps({'passed':True,'pcbnew':pcb.Version(),'cases':results,'scope':'Synthetic native geometry controls, not product/process qualification.'},indent=2)+'\n');print('Six actual scoped/native controls passed')

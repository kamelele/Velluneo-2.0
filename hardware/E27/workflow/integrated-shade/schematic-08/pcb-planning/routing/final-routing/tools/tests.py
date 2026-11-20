"""Synthetic saved-native-board adversarial checks. No customer CAD writes."""
from pathlib import Path
import argparse, copy, json, subprocess, sys, re
import pcbnew as k
from checker import Contract, check_saved, mm, rectangle, sha, point, load_native, valid_zone_outline

HERE=Path(__file__).resolve().parent
FIX=HERE/'fixtures';FIX.mkdir(exist_ok=True)

def vec(x,y):return k.VECTOR2I(mm(x),mm(y))

class Synthetic(Contract):
    def __init__(self):
        self.synthetic=True;self.input_hashes={}
        self.mapping={'A':'BUS_PLUS','B':'DC_RETURN'}
        self.expected={('J1','1'):'A',('J1','2'):'B'}
        self.refs={'J1'};self.domains={'BUS_PLUS':'BUS_DRAIN','DC_RETURN':'CONTROL_RETURN'}
        self.outline=[0,0,140,100];self.thermal=[68,62,88,82]
        self.minimum={'track_width':.3,'clearance':.3,'edge_clearance':4.,'hole_size':.3,'annular_width':.2}
        self.class_settings={'classes':[{'name':'Default','track_width':.3}],'netclass_patterns':[]}
        self.areas=[{'id':'corner','rectangle_mm':[0,0,12,12],'layers':['F.Cu','B.Cu'],'disallow':['pad','track','via','zone']}]
        self.exceptions=[{'ref':'J1','pins':['1','2'],'nets':['BUS_PLUS','DC_RETURN'],'layers':['F.Cu'],'escape_layers':['F.Cu'],'except_object_types':['pad','track'],'escape_margin_mm':1.,'proposed_drawn_floor_mm':1.5}]

def basic(ambiguous=False):
    c=Synthetic();b=k.BOARD();b.SetCopperLayerCount(2)
    nets={}
    for name in c.mapping:
        n=k.NETINFO_ITEM(b,name);b.Add(n);nets[name]=n
    for a,z in [((0,0),(140,0)),((140,0),(140,100)),((140,100),(0,100)),((0,100),(0,0))]:
        line=k.PCB_SHAPE();line.SetShape(k.SHAPE_T_SEGMENT);line.SetStart(vec(*a));line.SetEnd(vec(*z));line.SetLayer(k.Edge_Cuts);line.SetWidth(mm(.05));b.Add(line)
    f=k.FOOTPRINT(b);f.SetReference('J1');b.Add(f)
    for pin,xy,net in [('1',(20,20),'A'),('2',(23,20),'B')]+([('3',(20,20),'A')] if ambiguous else []):
        p=k.PAD(f);p.SetNumber(pin);p.SetAttribute(k.PAD_ATTRIB_SMD);p.SetShape(k.PAD_SHAPE_RECT);p.SetSize(vec(1,1));p.SetPosition(vec(*xy));ls=k.LSET();ls.AddLayer(k.F_Cu);p.SetLayerSet(ls);p.SetNet(nets[net]);f.Add(p)
    if ambiguous:
        c.expected[('J1','3')]='A'
        additional=copy.deepcopy(c.exceptions[0]);additional['pins']=['3','2'];c.exceptions.append(additional)
    g=k.PCB_SHAPE(f);g.SetShape(k.SHAPE_T_RECT);g.SetStart(vec(19,19));g.SetEnd(vec(24,21));g.SetLayer(k.F_CrtYd);g.SetWidth(mm(.05));f.Add(g)
    return b,c,nets

def track(b,nets,net,a,z,layer='F.Cu',width=.3):
    t=k.PCB_TRACK(b);t.SetStart(vec(*a));t.SetEnd(vec(*z));t.SetWidth(mm(width));t.SetLayer(k.F_Cu if layer=='F.Cu' else k.B_Cu);t.SetNet(nets[net]);b.Add(t);return t

def via(b,nets,net,xy):
    v=k.PCB_VIA(b);v.SetPosition(vec(*xy));v.SetWidth(mm(.8));v.SetDrill(mm(.3));v.SetViaType(k.VIATYPE_THROUGH);v.SetLayerPair(k.F_Cu,k.B_Cu);v.SetNet(nets[net]);b.Add(v);return v

def zone(b,nets,net,rect,layer='F.Cu',hole=None,filled=True):
    z=k.ZONE(b);ly=k.F_Cu if layer=='F.Cu' else k.B_Cu;z.SetLayer(ly);z.SetNet(nets[net])
    p=rectangle(rect)
    if hole is not None:
        p.BooleanSubtract(rectangle(hole));p.Fracture()
    # Zone outline and stored fill deliberately both defined for native persistence.
    z.Outline().Append(rectangle(rect))
    if filled:
        z.SetFilledPolysList(ly,p);z.SetIsFilled(True);z.SetNeedRefill(False)
    b.Add(z);return z

def route2():
    b,c,n=basic()
    f=next(iter(b.GetFootprints()));f.SetReference('U1')
    for p in f.Pads():p.SetNumber('2' if p.GetNumber()=='1' else '4')
    c.refs={'U1'};c.expected={('U1','2'):'A',('U1','4'):'B'}
    c.mapping={'A':'SENSE_FB','B':'DRAIN_BLOCKED'}
    c.domains={'SENSE_FB':'SWITCH_FLOAT','DRAIN_BLOCKED':'BUS_DRAIN','DC_RETURN':'CONTROL_RETURN'}
    c.route2_authorized=True
    c.exceptions=[{'ref':'U1','pins':['2','4'],'nets':['SENSE_FB','DRAIN_BLOCKED'],
        'layers':['F.Cu'],'escape_layers':['F.Cu'],'except_object_types':['pad','track'],
        'escape_margin_mm':1.5,'proposed_drawn_floor_mm':1.9}]
    track(b,n,'A',(20,20),(20,22.2));track(b,n,'B',(23,20),(23,22.2))
    return b,c,n

results=[]
def run(name,b,c,want,expected_type=None,owners=None,tamper=None,required_kinds=None):
    path=FIX/(name+'.kicad_pcb')
    intentional_nets={str(t.m_Uuid.AsString()):t.GetNetname() for t in b.GetTracks()}
    if not k.SaveBoard(str(path),b,True):raise AssertionError('Save failed')
    # KiCad SaveBoard propagates nets through intentional shorts, destroying the
    # deliberately malformed negative case. Restore ONLY synthetic track net
    # attributes by exact UUID, then reload the saved fixture for the actual check.
    text=path.read_text(encoding='utf-8')
    def restore(match):
        block=match.group(0);uid=re.search(r'\(uuid "([^"]+)"\)',block).group(1)
        return re.sub(r'\(net "[^"]*"\)', '(net '+json.dumps(intentional_nets[uid])+')',block)
    text=re.sub(r'\((?:segment|via|arc)\s.*?\n\t\)',restore,text,flags=re.S)
    path.write_text(text,encoding='utf-8')
    restored=load_native(path)
    assert {str(t.m_Uuid.AsString()):t.GetNetname() for t in restored.GetTracks()}==intentional_nets
    provpath=None
    if owners is not None:
        saved=load_native(path);records=[]
        for t in saved.GetTracks():
            if isinstance(t,k.PCB_VIA):continue
            records.append({'uuid':str(t.m_Uuid.AsString()),'net':t.GetNetname(),'layer':k.LayerName(t.GetLayer()),'a':point(t.GetStart()),'b':point(t.GetEnd()),'width':k.ToMM(t.GetWidth()),'owner':owners.get(str(t.m_Uuid.AsString()))})
        prov={'output_sha256':sha(path),'native_track_provenance':records}
        if tamper:tamper(prov)
        provpath=FIX/(name+'-provenance.json');provpath.write_text(json.dumps(prov,indent=2)+'\n')
    report=check_saved(path,c,provpath)
    (FIX/(name+'-report.json')).write_text(json.dumps(report,indent=2)+'\n')
    ok=report['passed']==want and report['input_unchanged']
    if expected_type:ok=ok and (any(f['type']==expected_type for f in report.get('findings',[])) or expected_type in report.get('error',''))
    if required_kinds:ok=ok and any(set(f.get('kinds',[]))==set(required_kinds) for f in report.get('findings',[]))
    results.append({'name':name,'expect_pass':want,'test_passed':ok,'board_sha256':sha(path),'report_sha256':sha(FIX/(name+'-report.json')),'error':report.get('error'),'findings':report.get('findings',[])})
    if not ok:raise AssertionError(name+': '+json.dumps(report))

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--native-cli');args=parser.parse_args()
    source=load_native(FIX/'actual-9db-rounded-hole-outline-source.kicad_pcb')
    z=next(iter(source.Zones()))
    assert z.Outline().IsSelfIntersecting() and valid_zone_outline(z.Outline())
    run('actual-rounded-holes-native-false-positive-regression',source,Synthetic(),True)
    run('actual-native-fill-rounding-containment-positive',load_native(FIX/'actual-9db-rounding-fill-source.kicad_pcb'),Synthetic(),True)
    b,c,n=basic();z=zone(b,n,'B',[40,40,50,50]);z.SetFilledPolysList(k.F_Cu,rectangle([39.997,40,50,50]));run('zone-fill-over-envelope-three-micron-negative',b,c,False,'fill outside actual zone outline')
    b,c,n=basic();z=zone(b,n,'B',[40,40,50,50]);z.SetFilledPolysList(k.F_Cu,rectangle([39.999,40,50,50]));run('zone-fill-within-envelope-one-micron-positive',b,c,True)
    b,c,n=basic();z=zone(b,n,'B',[40,40,50,50]);p=z.Outline();p.RemoveAllContours();p.NewOutline()
    for x,y in [(40,40),(50,48),(40,50),(49,40)]:p.Append(mm(x),mm(y))
    run('actual-outline-bowtie-invalid-negative',b,c,False,'Invalid actual zone outline')
    b,c,n=basic();z=zone(b,n,'B',[40,40,50,50]);z.Outline().BooleanSubtract(rectangle([43,43,47,47]));run('cached-fill-inside-outline-hole-negative',b,c,False,'fill outside actual zone outline')
    b,c,n=route2();run('route2-exact-extended-positive',b,c,True)
    b,c,n=route2();c.route2_authorized=False;run('route2-unapproved-negative',b,c,False,'Unsupported exception scope')
    b,c,n=route2();c.exceptions[0]['pins']=['1','4'];run('route2-wrong-pair-negative',b,c,False,'Unsupported exception scope')
    b,c,n=route2();c.exceptions[0]['layers']=['F.Cu','B.Cu'];run('route2-wrong-layer-negative',b,c,False,'Unsupported exception scope')
    b,c,n=route2();c.exceptions[0]['ref']='J1';run('route2-wrong-owner-scope-negative',b,c,False,'Unsupported exception scope')
    b,c,n=route2();c.exceptions[0]['proposed_drawn_floor_mm']=1.8;run('route2-weakened-floor-negative',b,c,False,'Unsupported exception scope')
    b,c,n=route2();c.exceptions[0]['escape_margin_mm']=1.;run('route2-old-region-insufficient-negative',b,c,False,'copper_spacing')
    b,c,n=route2();via(b,n,'B',(23,22.2));run('route2-via-not-exempt-negative',b,c,False,'copper_spacing',required_kinds=['track','via'])
    b,c,n=route2();zone(b,n,'B',[22.9,22.0,23.1,22.2]);run('route2-zone-not-exempt-negative',b,c,False,'copper_spacing',required_kinds=['track','zone'])
    b,c,n=basic();z=zone(b,n,'B',[40,40,50,50]);z.Outline().RemoveAllContours();z.Outline().Append(rectangle([40,40,44,50]));run('cached-fill-outside-outline-negative',b,c,False,'fill outside actual zone outline')
    b,c,n=basic();z=zone(b,n,'B',[40,40,50,50]);z.Outline().Append(rectangle([55,40,60,50]));p=rectangle([40,40,50,50]);p.Append(rectangle([55,40,60,50]));z.SetFilledPolysList(k.F_Cu,p);run('native-multiouter-outline-cache-stop-negative',b,c,False,'fill outside actual zone outline')
    b,c,n=basic();run('pad-exception-positive',b,c,True)
    b,c,n=basic();track(b,n,'A',(20,20),(20,21.5));track(b,n,'B',(23,20),(23,21.5));run('connected-local-track-positive',b,c,True)
    b,c,n=basic();track(b,n,'A',(20,20),(20,30));track(b,n,'B',(23,20),(23,30));run('track-escape-outside-negative',b,c,False,'copper_spacing',required_kinds=['track'])
    b,c,n=basic();track(b,n,'A',(20,20),(20,21.5));via(b,n,'B',(23,21.5));run('added-via-no-exception-negative',b,c,False,'copper_spacing',required_kinds=['track','via'])
    b,c,n=basic();track(b,n,'A',(40,40),(50,50));track(b,n,'B',(40,50),(50,40));run('track-crossing-negative',b,c,False,'copper_spacing',required_kinds=['track'])
    b,c,n=basic();track(b,n,'A',(40,40),(50,40));track(b,n,'B',(40,50),(50,50));run('generic-separated-tracks-positive',b,c,True)
    b,c,n=basic();track(b,n,'A',(40,40),(50,40));track(b,n,'B',(40,40.4),(50,40.4));run('native-near-tracks-negative',b,c,False,'copper_spacing',required_kinds=['track'])
    b,c,n=basic();track(b,n,'A',(20,21.4),(20,21.5));track(b,n,'B',(23,21.4),(23,21.5));run('near-but-disconnected-no-owner-negative',b,c,False,'copper_spacing',required_kinds=['track'])
    b,c,n=basic();track(b,n,'A',(20,20.651),(20,21.5));track(b,n,'B',(23,20),(23,21.5));run('one-micron-gap-cannot-prove-owner-negative',b,c,False,'copper_spacing')
    b,c,n=basic(True);ta=track(b,n,'A',(20,20),(20,21.5));tb=track(b,n,'B',(23,20),(23,21.5));run('ambiguous-roots-negative',b,c,False,'copper_spacing')
    owners={str(ta.m_Uuid.AsString()):['J1','1'],str(tb.m_Uuid.AsString()):['J1','2']};run('explicit-provenance-positive',b,c,True,owners=owners)
    run('tampered-provenance-negative',b,c,False,'provenance geometry mismatch',owners=owners,tamper=lambda p:p['native_track_provenance'][0].update(width=.4))
    run('bad-provenance-hash-negative',b,c,False,'hash mismatch',owners=owners,tamper=lambda p:p.update(output_sha256='0'*64))
    b,c,n=basic();zone(b,n,'A',[70,65,75,70],'B.Cu');run('foreign-thermal-zone-negative',b,c,False,'U3_backside_reservation')
    b,c,n=basic();zone(b,n,'B',[70,65,75,70],'B.Cu');run('dc-return-thermal-zone-positive',b,c,True)
    b,c,n=basic();zone(b,n,'B',[40,40,50,50]);track(b,n,'A',(45,35),(45,55));run('track-zone-crossing-negative',b,c,False,'copper_spacing',required_kinds=['zone','track'])
    b,c,n=basic();zone(b,n,'B',[35,35,55,55],hole=[38,38,52,52]);track(b,n,'A',(45,43),(45,47));run('track-in-zone-hole-positive',b,c,True)
    b,c,n=basic();zone(b,n,'B',[20.9,19.9,21.1,20.1]);run('zone-not-package-exempt-negative',b,c,False,'copper_spacing',required_kinds=['pad','zone'])
    b,c,n=basic();zone(b,n,'B',[40,40,50,50],filled=False);run('unfilled-zone-stop-negative',b,c,False,'unfilled')
    b,c,n=basic();track(b,n,'B',(70,70),(75,70),'B.Cu');run('dc-return-thermal-track-positive',b,c,True)
    b,c,n=basic();track(b,n,'A',(70,70),(75,70),'B.Cu');run('foreign-thermal-track-negative',b,c,False,'U3_backside_reservation')
    b,c,n=basic();track(b,n,'A',(10,10),(20,10));run('protected-area-track-negative',b,c,False,'protected_area')
    b,c,n=basic();track(b,n,'A',(3.9,20),(3.9,30));run('edge-track-negative',b,c,False,'copper_edge_setback')
    b,c,n=basic();track(b,n,'A',(40,40),(50,40),width=.2);run('track-width-negative',b,c,False,'track_width')
    b,c,n=basic();arc=k.PCB_ARC(b);arc.SetStart(vec(40,40));arc.SetMid(vec(45,45));arc.SetEnd(vec(50,40));arc.SetWidth(mm(.3));arc.SetLayer(k.F_Cu);arc.SetNet(n['A']);b.Add(arc);run('unsupported-arc-stop-negative',b,c,False,'Only straight')
    b,c,n=basic();t=track(b,n,'A',(20,21.4),(20,21.5));track(b,n,'B',(23,20),(23,21.5));run('false-authored-owner-not-connected-negative',b,c,False,'copper_spacing',owners={str(t.m_Uuid.AsString()):['J1','1']})
    summary={'synthetic_only':True,'tool':k.GetBuildVersion(),'checker_sha256':sha(HERE/'checker.py'),'tests_sha256':sha(__file__),'tests':results,'passed':all(r['test_passed'] for r in results)}
    if args.native_cli:
        version=subprocess.run([args.native_cli,'--version'],capture_output=True,text=True,encoding='utf-8',errors='replace')
        assert version.returncode==0 and version.stdout.strip()=='10.0.6'
        records=[]
        for board,label in [('native-near-tracks-negative','near'),('generic-separated-tracks-positive','separated'),('track-crossing-negative','crossing')]:
            out=FIX/('native-'+label+'-drc.json');source=FIX/(board+'.kicad_pcb');before=sha(source)
            cmd=[args.native_cli,'pcb','drc','--format','json','--output',str(out),str(source)]
            proc=subprocess.run(cmd,capture_output=True,text=True,encoding='utf-8',errors='replace')
            assert proc.returncode==0 and sha(source)==before
            report=json.loads(out.read_text());types=[x['type'] for x in report['violations']]
            records.append({'source_sha256':before,'report_sha256':sha(out),'command':cmd,'exit_code':proc.returncode,'stderr':proc.stderr,'violations':types,'unconnected':len(report['unconnected_items'])})
            if label=='near':assert 'clearance' in types
            if label=='separated':assert 'clearance' not in types and 'shorting_items' not in types
        native={'passed':True,'scope':'Synthetic discrimination of non-touching clearance; not complete DRC-clean fixtures or production acceptance','crossing_limitation':'Native convenience connectivity can propagate different-net crossing identity; checker independently uses raw PCB_IO_MGR.Load and raw UUID/native-net parity','records':records}
        (HERE/'native-drc-comparison.json').write_text(json.dumps(native,indent=2)+'\n')
        summary['native_drc_comparison_sha256']=sha(HERE/'native-drc-comparison.json')
    (HERE/'test-results.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps({'tests':len(results),'passed':summary['passed']}))

if __name__=='__main__':main()

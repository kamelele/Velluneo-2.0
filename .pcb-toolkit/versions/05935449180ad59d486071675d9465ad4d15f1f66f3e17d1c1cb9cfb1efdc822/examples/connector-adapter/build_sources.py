"""Author the original tutorial CAD once with KiCad's matching pcbnew Python.

Not an agent, library qualification or manufacturer reference design.
Replaying checks does not regenerate or overwrite these sources.
"""
import json
import sys
import uuid
from pathlib import Path
import pcbnew as pcb

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT/'scripts'))
import pcb_rules as rules
import connectivity
import product_contracts
import spatial

HERE = Path(__file__).resolve().parent/'board'


def uid(name):
    return str(uuid.uuid5(uuid.NAMESPACE_URL, 'pcb-tutorial-adapter/'+name))


def main():
    HERE.mkdir(parents=True, exist_ok=True)
    root = uid('schematic')
    symbol = '''(symbol "Tutorial:Connector_2" (pin_names (offset 0)) (in_bom yes) (on_board yes)
      (property "Reference" "J" (at 0 5.08 0) (effects (font (size 1.27 1.27))))
      (property "Value" "Connector_2" (at 0 2.54 0) (effects (font (size 1.27 1.27))))
      (property "Footprint" "Tutorial:Connector_2" (at 0 0 0) (effects (font (size 1.27 1.27)) hide))
      (symbol "Connector_2_0_1" (rectangle (start -2.54 1.27) (end -1.27 -3.81)
        (stroke (width 0.254) (type default)) (fill (type background))))
      (symbol "Connector_2_1_1"
        (pin passive line (at 0 0 180) (length 2.54) (name "1" (effects (font (size 1.27 1.27)))) (number "1" (effects (font (size 1.27 1.27)))))
        (pin passive line (at 0 -2.54 180) (length 2.54) (name "2" (effects (font (size 1.27 1.27)))) (number "2" (effects (font (size 1.27 1.27)))))))'''
    placed = []
    for ref, x in [('J1',50.8),('J2',101.6)]:
        placed.append(f'''(symbol (lib_id "Tutorial:Connector_2") (at {x} 50.8 0) (unit 1)
          (in_bom yes) (on_board yes) (dnp no) (uuid "{uid(ref)}")
          (property "Reference" "{ref}" (at {x-5} 46 0) (effects (font (size 1.27 1.27))))
          (property "Value" "Connector_2" (at {x-5} 58 0) (effects (font (size 1.27 1.27))))
          (property "Footprint" "Tutorial:Connector_2" (at {x} 50.8 0) (effects (font (size 1.27 1.27)) hide))
          (pin "1" (uuid "{uid(ref+'pin1')}")) (pin "2" (uuid "{uid(ref+'pin2')}"))
          (instances (project "board" (path "/{root}" (reference "{ref}") (unit 1)))))''')
    wires = ''.join(f'(wire (pts (xy 50.8 {y}) (xy 101.6 {y})) (stroke (width 0) (type default)) (uuid "{uid(net)}"))'
                    f'(label "{net}" (at 76.2 {y} 0) (effects (font (size 1.27 1.27))) (uuid "{uid(net+"label")}"))'
                    for y,net in [(50.8,'LINE_1'),(53.34,'LINE_2')])
    (HERE/'board.kicad_sch').write_text(f'''(kicad_sch (version 20250114) (generator "electronics-rules")
      (uuid "{root}") (paper "A4") (lib_symbols {symbol}) {''.join(placed)} {wires}
      (sheet_instances (path "/" (page "1"))))''',encoding='utf-8')
    (HERE/'Tutorial.kicad_sym').write_text('(kicad_symbol_lib (version 20241209) (generator "electronics-rules") '+symbol.replace('(symbol "Tutorial:Connector_2"', '(symbol "Connector_2"', 1)+')',encoding='utf-8')
    (HERE/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "Tutorial") (type "KiCad") (uri "${KIPRJMOD}/Tutorial.kicad_sym") (options "") (descr "Original fictional tutorial symbol")))',encoding='utf-8')
    (HERE/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "Tutorial") (type "KiCad") (uri "${KIPRJMOD}/Tutorial.pretty") (options "") (descr "Original tutorial geometry; no part qualification")))',encoding='utf-8')
    board=pcb.BOARD()
    mm=lambda x,y:pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y))
    for start,end in [((0,0),(30,0)),((30,0),(30,20)),((30,20),(0,20)),((0,20),(0,0))]:
        shape=pcb.PCB_SHAPE(board);shape.SetShape(pcb.SHAPE_T_SEGMENT);shape.SetStart(mm(*start));shape.SetEnd(mm(*end));shape.SetLayer(pcb.Edge_Cuts);shape.SetWidth(pcb.FromMM(.05));board.Add(shape)
    nets=[]
    for name in ['LINE_1','LINE_2']:
        net=pcb.NETINFO_ITEM(board,'/'+name);board.Add(net);nets.append(net)
    for ref,x in [('J1',7.5),('J2',22.5)]:
        fp=pcb.FOOTPRINT(board);fp.SetReference(ref);fp.SetValue('Connector_2');fp.SetFPID(pcb.LIB_ID('Tutorial','Connector_2'));fp.SetAttributes(pcb.FP_THROUGH_HOLE)
        fp.SetPath(pcb.KIID_PATH('/'+root+'/'+uid(ref)))
        fp.SetPosition(mm(x,8.73));fp.Reference().SetPosition(mm(x,5));fp.Value().SetVisible(False)
        for i,net in enumerate(nets):
            pad=pcb.PAD(fp);pad.SetNumber(str(i+1));pad.SetShape(pcb.PAD_SHAPE_CIRCLE);pad.SetAttribute(pcb.PAD_ATTRIB_PTH);pad.SetSize(mm(1.8,1.8));pad.SetDrillSize(mm(1,1))
            # Standard plated-hole copper and mask only, no paste/silk on pads.
            layers=pcb.LSET();[layers.AddLayer(k) for k in [pcb.F_Cu,pcb.B_Cu,pcb.F_Mask,pcb.B_Mask]];pad.SetLayerSet(layers)
            pad.SetPosition(mm(x,8.73+i*2.54));pad.SetNet(net);fp.Add(pad)
        for a,b in [((-1.5,-1.5),(1.5,-1.5)),((1.5,-1.5),(1.5,4.04)),((1.5,4.04),(-1.5,4.04)),((-1.5,4.04),(-1.5,-1.5))]:
            line=pcb.PCB_SHAPE(fp);line.SetShape(pcb.SHAPE_T_SEGMENT);line.SetLayer(pcb.F_CrtYd);line.SetWidth(pcb.FromMM(.05));line.SetStart(mm(x+a[0],8.73+a[1]));line.SetEnd(mm(x+b[0],8.73+b[1]));fp.Add(line)
        board.Add(fp)
        if ref=='J1':
            lib=pcb.FOOTPRINT(fp);lib.SetPosition(mm(0,0));lib.SetReference('REF**');lib.SetPath(pcb.KIID_PATH());lib.ClearAllNets()
            (HERE/'Tutorial.pretty').mkdir(exist_ok=True);pcb.PCB_IO_KICAD_SEXPR().FootprintSave(str(HERE/'Tutorial.pretty'),lib)
    for i,net in enumerate(nets):
        track=pcb.PCB_TRACK(board);track.SetStart(mm(7.5,8.73+i*2.54));track.SetEnd(mm(22.5,8.73+i*2.54));track.SetWidth(pcb.FromMM(.5));track.SetLayer(pcb.F_Cu);track.SetNet(net);board.Add(track)
    pcb.SaveBoard(str(HERE/'board.kicad_pcb'),board)
    (HERE/'board.kicad_prl').unlink(missing_ok=True)
    config=rules.read(ROOT/'templates/project/hardware.json');config['fabrication']['vendor']='jlcpcb';config['assembly']['mode']='inhouse'
    config['product']['domains']=['Fictional passive lab adapter; <=5 V and <=10 mA only; not qualified']
    config['product']['spatial_file']='spatial-constraints.json'
    config['source_files']=['board.kicad_sch','board.kicad_pcb','board.kicad_pro','board.kicad_dru','Tutorial.kicad_sym','sym-lib-table','fp-lib-table','Tutorial.pretty/Connector_2.kicad_mod','specification.md','review-basis.md','bom.csv','bringup-plan.md']
    rules.write(HERE/'hardware.json',config)
    basis={'path':'specification.md','sha256':rules.digest(HERE/'specification.md')}
    intent={'schema_version':1,'revision':'tutorial-1','basis':'Independent pin table in specification.md; not exported CAD','basis_sources':[basis],
      'components':[{'ref':ref,'units':[{'name':'A','pins':['1','2']}]} for ref in ['J1','J2']],
      'nets':[{'id':'LINE_'+str(i),'pins':[{'ref':ref,'pin':str(i)} for ref in ['J1','J2']]} for i in [1,2]],'no_connects':[],'barriers':[]}
    intent['approval']={'approved_by':'synthetic-tutorial-NOT-human-approval','evidence':'Demonstration replay only; see review-basis.md','intent_digest':connectivity.intent_digest(intent)}
    rules.write(HERE/'intended-connectivity.json',intent)
    shape={'schema_version':1,'revision':'tutorial-1','basis':'Independent fictional 30 x 20 mm board specification','basis_sources':[basis],'outline_mm':[0,0,30,20],'areas':[],'blocks':[],'no_blocks_reason':'Passive two-wire adapter; no active functional blocks in this tutorial.'}
    shape['approval']={'approved_by':'synthetic-tutorial-NOT-human-approval','evidence':'Demonstration replay only; see review-basis.md','intent_digest':spatial.intent_digest(shape)}
    rules.write(HERE/'spatial-constraints.json',shape)
    requirements={'schema_version':1,'product':'fictional-passive-adapter','revision':'tutorial-1','subsystems':[{'id':'ADAPTER','kind':'pcb','owner':'tutorial-author'}],
      'requirements':[{'id':identifier,'revision':'1','owner':'tutorial-author','gate':gate,'basis':'Original fictional specification.md; no general safety/process recommendation','text':text,'acceptance':acceptance,'method':'review','implementation':[{'subsystem':'ADAPTER','object':obj}],'evidence_ids':['EV-TUTORIAL']} for identifier,gate,text,acceptance,obj in [
        ('REQ-SCOPE','specification','Passive lab continuity demonstration only, <=5 V and <=10 mA.','Review scope and unqualified process status.','specification.md'),
        ('REQ-PINS','schematic','J1.1 connects only J2.1; J1.2 connects only J2.2.','Compare independent physical-pin intent with actual CAD.','J1/J2 physical pins'),
        ('REQ-GEOMETRY','routing','30 x 20 mm board, 15 mm long 0.5 mm tracks and 2.54 mm pad pitch.','Inspect board geometry and fresh CAD reports.','board.kicad_pcb')]],'interfaces':[],'unknowns':[],
      'evidence':[{'id':'EV-TUTORIAL','kind':'review','result':'pass','verified_by':'synthetic-tutorial-NOT-independent-review','artifact':'review-basis.md','sha256':rules.digest(HERE/'review-basis.md'),'inputs':[]}]}
    requirements['evidence'][0]['intent_digest']=product_contracts.intent_digest(requirements);rules.write(HERE/'requirements.json',requirements)
    # Authored initial settings, not implicit adoption in a recipient's project.
    _,_,values=rules.resolve(config);rules.write(HERE/'board.kicad_pro',rules.project_settings('board',values,[]))
    (HERE/'board.kicad_dru').write_text(rules.dru(values),encoding='utf-8')


if __name__=='__main__':main()

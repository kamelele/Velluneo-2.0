"""Original schematic fixtures independent of the approved pin-table expectation."""
import json
import shutil
import sys
import uuid
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import pcb_rules as rules
import connectivity_fixture


def uid():return str(uuid.uuid4())


def write(folder,case='valid'):
    folder.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'examples/connectivity/basis.md',folder/'basis.md')
    intended=json.loads((ROOT/'examples/connectivity/intended-connectivity.json').read_text(encoding='utf-8'))
    # Synthetic approval is fixture setup only. Expected pin groups never come
    # from a netlist or the erroneous geometry variant being tested.
    connectivity_fixture.approve(intended)
    rules.write(folder/'intended-connectivity.json',intended)
    root=uid()
    def definition(name,units):
        body=f'''(symbol "Connectivity:{name}" (pin_names (offset 0)) (in_bom yes) (on_board no)
          (property "Reference" "U" (at 0 2 0) (effects (font (size 1 1))))
          (property "Value" "{name}" (at 0 -2 0) (effects (font (size 1 1))))
          (symbol "{name}_0_1" (rectangle (start -1 -1) (end 1 1) (stroke (width 0) (type default)) (fill (type background))))'''
        for number,pins in units:
            body+=f'(symbol "{name}_{number}_1" '+''.join(
                f'''(pin passive line (at 0 {y} 0) (length 0)
                   (name "P{pin}" (effects (font (size 1 1)))) (number "{pin}" (effects (font (size 1 1)))))'''
                for pin,y in pins)+')'
        return body+')'
    # Actual CAD geometry is specified separately from the expected net sets.
    definitions=[definition('Dual',[(1,[('1',0),('2',-2.54)]),(2,[('3',0),('4',-2.54)])]),
                 definition('Connector',[(1,[('1',0),('2',-2.54),('3',-25.4),('4',-27.94)])])]
    placed=[]
    for ref,name,unit,x,y,pins in [('U1','Dual',1,25.4,25.4,['1','2']),
                                  ('U1','Dual',2,25.4,50.8,['3','4']),
                                  ('J1','Connector',1,50.8,25.4,['1','2','3','4'])]:
        if case=='omitted-unit' and ref=='U1' and unit==2:continue
        placed.append(f'''(symbol (lib_id "Connectivity:{name}") (at {x} {y} 0) (unit {unit})
          (in_bom yes) (on_board no) (dnp no) (uuid "{uid()}")
          (property "Reference" "{ref}" (at {x} {y-2} 0) (effects (font (size 1 1))))
          (property "Value" "{name}" (at {x} {y+2} 0) (effects (font (size 1 1))))
          {''.join('(pin "'+p+'" (uuid "'+uid()+'"))' for p in pins)}
          (instances (project "board" (path "/{root}" (reference "{ref}") (unit {unit})))))''')
    segments=[(25.4,25.4,50.8,25.4),(25.4,27.94,50.8,27.94),(25.4,50.8,50.8,50.8)]
    if case=='split':segments=segments[1:]
    if case=='wrong-pin':segments[:2]=[(25.4,25.4,50.8,27.94),(25.4,27.94,50.8,25.4)]
    if case=='merged':segments.append((38.1,25.4,38.1,27.94))
    if case=='connected-nc':segments.append((25.4,53.34,50.8,53.34))
    wires=''.join(f'(wire (pts (xy {x1} {y1}) (xy {x2} {y2})) (stroke (width 0) (type default)) (uuid "{uid()}"))'
                  for x1,y1,x2,y2 in segments)
    if case=='merged':
        wires+=''.join(f'(junction (at 38.1 {y}) (diameter 0) (color 0 0 0 0) (uuid "{uid()}"))' for y in [25.4,27.94])
    if case=='renamed':
        wires+=f'(label "Renamed_without_changing_pins" (at 38.1 25.4 0) (effects (font (size 1.27 1.27))) (uuid "{uid()}"))'
    nc=''.join(f'(no_connect (at {x} 53.34) (uuid "{uid()}"))' for x in [25.4,50.8]
               if not (case=='missing-nc' and x==25.4) and not (case=='omitted-unit' and x==25.4))
    source=f'''(kicad_sch (version 20250114) (generator "electronics-rules") (uuid "{root}") (paper "A4")
      (lib_symbols {''.join(definitions)}) {''.join(placed)} {wires} {nc}
      (sheet_instances (path "/" (page "1"))))'''
    (folder/'board.kicad_sch').write_text(source,encoding='utf-8')
    library='(kicad_symbol_lib (version 20241209) (generator "electronics-rules") '+''.join(d.replace('Connectivity:','') for d in definitions)+')'
    (folder/'Connectivity.kicad_sym').write_text(library,encoding='utf-8')
    (folder/'sym-lib-table').write_text('(sym_lib_table (version 7) (lib (name "Connectivity") (type "KiCad") (uri "${KIPRJMOD}/Connectivity.kicad_sym") (options "") (descr "")))',encoding='utf-8')
    return intended


if __name__=='__main__':
    folder=ROOT/'.work/connectivity-example'
    write(folder)
    config={'name':'board','kicad_version':'10.0.6','product':{'connectivity_file':'intended-connectivity.json'},
            'source_files':['board.kicad_sch','Connectivity.kicad_sym','sym-lib-table']}
    rules.write(folder/'hardware.json',config)
    report=rules.connectivity.verify(folder,config,rules.cli_path(None),rules.run_tool)
    rules.write(folder/'.work/connectivity.json',report)
    print(json.dumps({'passed':report['passed'],'errors':report['errors']},ensure_ascii=True))
    raise SystemExit(0 if report['passed'] else 1)

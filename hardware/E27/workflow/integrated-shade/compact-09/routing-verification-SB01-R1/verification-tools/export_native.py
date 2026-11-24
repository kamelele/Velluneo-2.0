"""Read-only native verification/exports from an explicitly frozen source directory.

No SaveBoard, SES import, source edits or supplier action. Run with pinned KiCad Python.
"""
from pathlib import Path
import argparse, hashlib, json, subprocess, sys
import pcbnew as k

p=argparse.ArgumentParser()
p.add_argument('--source',required=True,type=Path)
p.add_argument('--output',required=True,type=Path)
a=p.parse_args(); s=a.source.resolve(); o=a.output.resolve()
assert not o.is_relative_to(s), 'Keep generated packet outside source inputs'
o.mkdir(parents=True,exist_ok=True)
assert not (o/'commands.json').exists(), 'Use a new run directory'
pcb=s/'SC09_compact.kicad_pcb'; sch=s/'SC09_compact.kicad_sch'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs={str(f.relative_to(s)):sha(f) for f in s.rglob('*') if f.is_file() and '.work' not in f.parts and f.suffix not in ('.kicad_prl','.lck')}
cli=Path(sys.executable).with_name('kicad-cli.exe'); logs=[]
def run(args):
    r=subprocess.run([str(cli),*map(str,args)],capture_output=True,encoding='utf-8',errors='replace')
    logs.append({'args':list(map(str,args)),'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr})
    (o/'commands.json').write_text(json.dumps(logs,indent=2)+'\n')
    print(args[:3],r.returncode,flush=True)
    return r.returncode
run(['sch','erc','--format','json','--severity-all','--exit-code-violations','-o',o/'ERC.json',sch])
run(['sch','export','netlist','--format','kicadxml','-o',o/'netlist.xml',sch])
run(['pcb','drc','--format','json','--severity-all','--all-track-errors','--schematic-parity','--exit-code-violations','--refill-zones','-o',o/'DRC.json',pcb])
b=k.LoadBoard(str(pcb)); b.BuildConnectivity()
report={'source_files':inputs,'board_sha256':sha(pcb),'native_version':k.GetBuildVersion(),'native_unconnected':b.GetConnectivity().GetUnconnectedCount(False),'zones':sum(not z.GetIsRuleArea() for z in b.Zones()),'rule_areas':sum(z.GetIsRuleArea() for z in b.Zones()),'source_unchanged':all((s/f).exists() and sha(s/f)==h for f,h in inputs.items()),'native_checks_success':all(x['exit_code']==0 for x in logs),'fabrication_exported':False,'order_submitted':False}
# Any actual zone demands a writer-owned saved refill and new source freeze.
if report['native_checks_success'] and report['native_unconnected']==0 and report['zones']==0 and report['source_unchanged']:
    (o/'gerbers').mkdir();(o/'drills').mkdir();(o/'views').mkdir()
    run(['pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts','--precision','6','--subtract-soldermask','--check-zones','-o',o/'gerbers',pcb])
    run(['pcb','export','drill','--format','excellon','--drill-origin','absolute','--excellon-units','mm','--excellon-zeros-format','decimal','--excellon-separate-th','--generate-report','--generate-map','--map-format','pdf','--report-path',o/'drills/drill-report.txt','-o',o/'drills',pcb])
    run(['pcb','export','pdf','--layers','F.Cu,B.Cu','--common-layers','Edge.Cuts','--mode-multipage','-o',o/'views/copper.pdf',pcb])
    for side in ['F','B']:
        args=['pcb','export','pdf','--layers',f'{side}.Fab,{side}.Silkscreen,Edge.Cuts','--mode-single','--exclude-value','--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers']
        if side=='B':args.append('--mirror')
        run([*args,'-o',o/f'views/assembly-{side}.pdf',pcb])
    run(['sch','export','pdf','-o',o/'views/schematic.pdf',sch])
    report['fabrication_exported']=all(x['exit_code']==0 for x in logs)
report['source_unchanged']=all((s/f).exists() and sha(s/f)==h for f,h in inputs.items())
report['artifacts']={f.relative_to(o).as_posix():sha(f) for f in o.rglob('*') if f.is_file()}
(o/'native-export.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({key:report[key] for key in ['native_unconnected','zones','source_unchanged','native_checks_success','fabrication_exported']}))
sys.exit(0 if report['fabrication_exported'] and report['source_unchanged'] else 1)

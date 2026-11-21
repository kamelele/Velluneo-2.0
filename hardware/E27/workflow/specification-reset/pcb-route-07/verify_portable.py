"""Read-only standalone archive/dependency and physical pin checks after extraction."""
from pathlib import Path
import json,hashlib,zipfile,argparse,pcbnew,re
D=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,default=D/'.work/portable');a=ap.parse_args();manifest=json.loads((D/'portable-artifacts.json').read_text());zpath=D/manifest['zip'];assert hashlib.sha256(zpath.read_bytes()).hexdigest()==manifest['sha256']
with zipfile.ZipFile(zpath)as z:
 assert z.testzip()is None
 for r in manifest['members']:assert hashlib.sha256(z.read(r['path'])).hexdigest()==r['sha256']
expected={p['ref']+'.'+n:net for p in json.loads((D/'design/proposed-parts.json').read_text())for n,net in p['pins'].items()};mapping=json.loads((D/'design/full-build-result.json').read_text())['logical_to_native_netnames'];results=[]
for folder,stem,layers in [('two-layer-development','Velluneo_driver',2),('four-layer-UNADOPTED','Velluneo_comparison',4)]:
 root=(a.root/folder).resolve();board=pcbnew.LoadBoard(str(root/(stem+'.kicad_pcb')));assert board.GetCopperLayerCount()==layers;models=[];pads={f.GetReference()+'.'+p.GetNumber():p for f in board.GetFootprints()for p in f.Pads()};assert len(pads)==81 and len(board.GetFootprints())==33
 project=json.loads((root/(stem+'.kicad_pro')).read_text());assert project['meta']['filename']==stem+'.kicad_pro'
 for sheet in project.get('schematic',{}).get('top_level_sheets',[]):assert sheet['filename']==stem+'.kicad_sch'and(root/sheet['filename']).exists()
 for key,p in pads.items():
  net=expected[key]
  if net in mapping:assert p.GetNetname()==mapping[net]
  else:assert p.GetNetname().startswith('unconnected-')
 for f in board.GetFootprints():
  for model in f.Models():
   path=Path(model.m_Filename.replace('${KIPRJMOD}',root.as_posix())).resolve();assert path.is_relative_to(root)and path.exists(),path;models.append(dict(ref=f.GetReference(),path=path.relative_to(root).as_posix(),sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
 assert len(models)==33
 for name in('fp-lib-table','sym-lib-table'):
  for uri in re.findall(r'\(uri "([^"]+)"\)',(root/name).read_text()):
   path=Path(uri.replace('${KIPRJMOD}',root.as_posix())).resolve();assert path.is_relative_to(root)and path.exists()
 results.append(dict(project=folder,footprints=33,pads=81,physical_pin_intent_matches=True,copper_layers=layers,models=models,all_dependencies_local=True))
(D/'design/checks/portable-dependencies.json').write_text(json.dumps(dict(zip_sha256=manifest['sha256'],crc_and_member_hashes_pass=True,projects=results),indent=2)+'\n');print('Verified standalone graph, layer count, local tables and33models per project')

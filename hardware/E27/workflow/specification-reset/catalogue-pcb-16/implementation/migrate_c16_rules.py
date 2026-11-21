from pathlib import Path
import sys,json,hashlib,re,itertools
W=Path(__file__).resolve().parent;sys.path.insert(0,str(W/'toolkit-c11-source/scripts'));import scoped_policy as s
E=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/catalogue-pcb-16/design';f=E/'Velluneo_driver.kicad_dru';old=f.read_bytes();text=old.decode();obsolete=" || A.NetName == 'unconnected-(T1-Pad3)'";obsoleteB=obsolete.replace('A.NetName','B.NetName');new=text.replace(obsolete,'').replace(obsoleteB,'').encode();assert text.count(obsolete)==1 and text.count(obsoleteB)==1
g=json.loads((E/'Velluneo_driver.kicad_pro').read_text())['board']['design_settings']['rules'];before,_=s.generated_clearances(text,g);after,_=s.generated_clearances(new.decode(),g);nets=s.board_nets(E/'Velluneo_driver.kicad_pcb');assert 'unconnected-(T1-Pad3)'not in nets
rows=[]
for a,b in itertools.product(sorted(nets)+['','__UNKNOWN__'],repeat=2):
 x=max([g['min_clearance']]+[v for ast,v in before if s.matches(ast,a,b)]);y=max([g['min_clearance']]+[v for ast,v in after if s.matches(ast,a,b)]);assert x==y;rows.append([a,b,x,y])
C=E.parent/'checks';(C/'rules-before-phantom-cleanup.kicad_dru').write_bytes(old);f.write_bytes(new)
h=json.loads((E/'hardware.json').read_text(encoding='utf-8-sig'))
for r in h['product']['scoped_clearances']:
 for k in ('nets_a','nets_b'):r[k]=[n for n in r[k]if n!='unconnected-(T1-Pad3)']
(E/'hardware.json').write_text(json.dumps(h,indent=2)+'\n')
(C/'bounded-rule-migration.json').write_text(json.dumps(dict(scope='Manual bounded migration of obsolete net literal only; all real directed net-pair constraints unchanged. Toolkit refuses absent literals in old policy; no clearance, severity or waiver relaxed.',reviewed_by='/root coordinator; independent final change review pending',before_sha256=hashlib.sha256(old).hexdigest(),after_sha256=hashlib.sha256(new).hexdigest(),actual_nets=sorted(nets),directed_cases=len(rows),effective_pairs=rows,passed=True),indent=2)+'\n')
print('Bounded migration PASS',len(rows),'identical effective real-net cases')

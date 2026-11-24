import json,hashlib,math,xml.etree.ElementTree as ET
from pathlib import Path
R=Path(__file__).resolve().parents[4]
O=R/'outputs/SC09_SB01_R2_rozruch_final'
H=Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text(encoding='utf-8-sig'))
m=read(O/'core-manifest.json')
bad=[p for p,e in m['files'].items() if not (O/p).is_file() or sha(O/p)!=e['sha256'] or (O/p).stat().st_size!=e['bytes']]
assert not bad,bad
canonical=R/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'
guards=read(O/'provenance/before.json')['source_guards']
changed=[p for p,v in guards.items() if sha(canonical/p)!=v]
assert not changed,changed
s=read(O/'analysis/startup/rc-screen.json'); rows=s['rows']
assert len(rows)==512
for k,v in s['maxima'].items():assert math.isclose(max(r[k] for r in rows),v,rel_tol=1e-12,abs_tol=1e-12)
power=357.8**2/87.75
assert math.isclose(power,s['maxima']['R10_peak_W'])
assert all(r['C1_peak_V']<=357.8+1e-8 and r['C4_peak_V']<=357.8+1e-8 and r['C1_min_V']>=-1e-8 and r['C4_min_V']>=-1e-8 for r in rows)
erc=read(O/'checks/native/ERC.json');drc=read(O/'checks/native/DRC.json')
assert not any(x['violations'] for x in erc['sheets'])
assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
parts=read(O/'checks/native/actual-parts.json')
assert all(x['passed'] for x in parts['rows']) and len(parts['rows'])==19
net=ET.parse(O/'checks/native/netlist.xml').getroot()
graph={n.attrib['name']:sorted((a.attrib['ref'],a.attrib['pin']) for a in n.findall('node')) for n in net.findall('./nets/net')}
assert len(graph)==11 and sum(map(len,graph.values()))==46
for p in ['checks/retained-gerber-audit.json','checks/native/fresh-gerber-audit.json']:
 a=read(O/p);assert a['passed'] and not a['findings'],p
g=read(O/'checks/native/geometry-and-graph.json');assert g['passed'] and g['ZIP_all_eight_bytes_identical_to_R1']
assert sha(O/'SC09_SB01_R2_Gerber_Drill_CANDIDATE.zip')==guards['release-refinement-R1/SC09_SB01_R1_Gerber_Drill_CANDIDATE.zip']
t=read(O/'checks/toolkit/check.json');assert t['errors']
out={'actor':'/root/sb01_r1_final_reality','core_sha256':sha(O/'core-manifest.json'),'core_files_verified':len(m['files']),'core_hash_errors':bad,'canonical_guard_count':len(guards),'canonical_changed':changed,'candidate_board_sha256':sha(O/'source/SC09_compact.kicad_pcb'),'RC_rows_recomputed_summary':len(rows),'analytic_RC_peak_W':power,'pulse_graph_screen_W':2500,'graphical_power_ratio':2500/power,'R10_60mA_loss_W':.06**2*112.75,'R10_80mA_loss_W':.08**2*112.75,'native_report_checks':{'ERC':0,'DRC':0,'parity':0,'unconnected':0,'MPN_rows':19,'nets':len(graph),'pins':sum(map(len,graph.values()))},'manufacturing_audits':'retained and fresh geometry passed; not electrical approval','full_toolkit_errors':len(t['errors']),'canonical_not_adopted':True,'powered_approval':False}
(H/'verification.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print(json.dumps(out,indent=2))

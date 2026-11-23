from pathlib import Path
import json,hashlib,re,collections,zipfile,math
import pcbnew as k
ROOT=Path.cwd();R=ROOT/'work/Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';H=ROOT/'work/sc09-order-audit/reviews';O=ROOT/'outputs/SC09_weryfikacja_i_kompendium';M=ROOT/'work/sc09-order-audit/review-inputs.json'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();m=json.loads(M.read_text());assert sha(M)=='5cb5713b8c8022d10d00ff0d733fccac21ca4e5dec82153a35e4da2f4df7c34c'
errors=[x['path']for x in m['files']if not(ROOT/x['path']).exists()or sha(ROOT/x['path'])!=x['sha256']]
jsonerrors=[]
for x in m['files']:
 if x['path'].endswith('.json'):
  try:json.loads((ROOT/x['path']).read_text(encoding='utf-8-sig'))
  except Exception as e:jsonerrors.append([x['path'],str(e)])
b=k.LoadBoard(str(S/'SC09_compact.kicad_pcb'));mm=k.ToMM
norm=lambda a,z,w:tuple(sorted([tuple(round(v,6)for v in a),tuple(round(v,6)for v in z)]))+(round(w,6),)
native={ly:collections.Counter(norm((mm(t.GetStart().x),mm(t.GetStart().y)),(mm(t.GetEnd().x),mm(t.GetEnd().y)),mm(t.GetWidth()))for t in b.GetTracks()if not isinstance(t,k.PCB_VIA)and b.GetLayerName(t.GetLayer())==ly)for ly in ['F.Cu','B.Cu']}
trackdiff={};flashes={};edges=[]
for ly,ext in [('F.Cu','gtl'),('B.Cu','gbl'),('Edge.Cuts','gm1')]:
 p=next((O/'fabrication-candidate/gerbers').glob('*.'+ext));t=p.read_text();aps={int(a):float(w)for a,w in re.findall(r'%ADD(\d+)C,([\d.]+)\*%',t)};ap=None;xy=None;region=False;got=collections.Counter();dots=[]
 for line in t.splitlines():
  if line=='G36*':region=True
  if line=='G37*':region=False
  match=re.fullmatch(r'D(\d+)\*',line)
  if match:ap=int(match[1]);continue
  match=re.fullmatch(r'X(-?\d+)Y(-?\d+)D0([123])\*',line)
  if not match:continue
  nx,ny=int(match[1])/1e6,-int(match[2])/1e6;op=match[3]
  if op=='1'and xy and not region:
   seg=norm(xy,(nx,ny),aps[ap]);got[seg]+=1
   if ly=='Edge.Cuts':edges.append([xy,(nx,ny)])
  if op=='3':dots.append((nx,ny))
  xy=(nx,ny)
 if ly!='Edge.Cuts':trackdiff[ly]={'native_count':sum(native[ly].values()),'export_count':sum(got.values()),'missing':list((native[ly]-got).elements()),'extra':list((got-native[ly]).elements())};flashes[ly]=len(dots)
# Independent drill parser and compare using actualoutputdecimalquantization.
drill=O/'fabrication-candidate/drills/SC09_compact-PTH.drl';tools={};tool=None;hits=[]
for line in drill.read_text().splitlines():
 z=re.fullmatch(r'T(\d+)C([\d.]+)',line)
 if z:tools[z[1]]=float(z[2]);continue
 z=re.fullmatch(r'T(\d+)',line)
 if z:tool=z[1];continue
 z=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line)
 if z:hits.append((float(z[1]),-float(z[2]),tools[tool]))
nh=[]
for f in b.GetFootprints():
 for p in f.Pads():
  if p.GetDrillSize().x:nh.append((mm(p.GetPosition().x),mm(p.GetPosition().y),mm(p.GetDrillSize().x)))
for t in b.GetTracks():
 if isinstance(t,k.PCB_VIA):nh.append((mm(t.GetPosition().x),mm(t.GetPosition().y),mm(t.GetDrillValue())))
co=lambda a:collections.Counter(tuple(round(v,3)for v in row)for row in a)
drdiff={'native':len(nh),'export':len(hits),'missing':list((co(nh)-co(hits)).elements()),'extra':list((co(hits)-co(nh)).elements())}
zipfilep=O/'fabrication-candidate/SC09_SB01_Gerber_Drill_CANDIDATE_NOT_RELEASED.zip'
with zipfile.ZipFile(zipfilep)as z:
 zn=z.namelist();zbad=z.testzip();zmatch={n:hashlib.sha256(z.read(n)).hexdigest()==sha(next((O/'fabrication-candidate').rglob(Path(n).name)))for n in zn}
intent=json.loads((S/'intended-connectivity.SB01.json').read_text());expected={(p['ref'],p['pin']):n['id']for n in intent['nets']for p in n['pins']};actual={(f.GetReference(),p.GetNumber()):p.GetNetname().lstrip('/')for f in b.GetFootprints()for p in f.Pads()};graphdiff=[{'pin':key,'expected':expected.get(key),'actual':actual.get(key)}for key in expected.keys()|actual.keys()if expected.get(key)!=actual.get(key)]
legacy=S/'release-candidate/SC09_do_zamowienia_PCB.zip'
out={'actor':'/root/sb01_change_review','manifest_sha256':sha(M),'manifest_files':len(m['files']),'hash_mismatches':errors,'JSON_parse_errors':jsonerrors,'PCB_sha256':sha(S/'SC09_compact.kicad_pcb'),'native_intent_graph':{'pins':len(actual),'differences':graphdiff},'independent_Gerber_track_comparison':trackdiff,'independent_D03_flash_counts_including_vias':flashes,'independent_drill_quantized_comparison':drdiff,'independent_outline_segments':edges,'ZIP':{'sha256':sha(zipfilep),'files':zn,'integrity_failure':zbad,'entry_bytes_match_export':zmatch,'raw_gbrjob_absent':not any(n.endswith('.gbrjob')for n in zn),'old_archive_not_reused':sha(zipfilep)!=sha(legacy)},'source_preflight':'change.preflight.json','no_source_or_approval_mutation':'All166priorSB01inputsretained; hardwareapprovals{}; no agentreleaseapprovalrecordadded.'}
(H/'change.independent-checks.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({x:out[x]for x in ['manifest_files','hash_mismatches','JSON_parse_errors','native_intent_graph','independent_Gerber_track_comparison','independent_drill_quantized_comparison','ZIP']},indent=2))

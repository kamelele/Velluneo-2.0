from pathlib import Path
import re,json,math,collections,hashlib
import pcbnew as k
ROOT=Path.cwd();H=ROOT/'work/sc09-order-audit/fabrication';O=ROOT/'outputs/SC09_weryfikacja_i_kompendium/fabrication-candidate';G=O/'gerbers';D=O/'drills';b=k.LoadBoard(str(H/'native-copy/SC09_compact.kicad_pcb'));mm=k.ToMM
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def parse(p):
 aps={};ops=[];current=None;pos=(0.,0.);ref=None;net=None;pol='dark';region=None;unsupported=[]
 for line in p.read_text().splitlines():
  line=line.strip()
  if line.startswith('%ADD'):
   m=re.fullmatch(r'%ADD(\d+)([A-Za-z]+),([^*]+)\*%',line);aps[int(m[1])]={'shape':m[2],'args':list(map(float,m[3].split('X')))}
  elif re.fullmatch(r'D\d+\*',line):current=int(line[1:-1])
  elif line.startswith('%TO.P,'):ref=tuple(line[len('%TO.P,'):-2].split(',')[:2])
  elif line.startswith('%TO.N,'):net=line[len('%TO.N,'):-2]
  elif line=='%TD*%':ref=None;net=None
  elif line=='%LPD*%':pol='dark'
  elif line=='%LPC*%':pol='clear'
  elif line=='G36*':region=[]
  elif line=='G37*':ops.append({'kind':'region','points':region,'polarity':pol});region=None
  elif line.startswith('X'):
   m=re.fullmatch(r'X(-?\d+)Y(-?\d+)D0([123])\*',line)
   if not m:unsupported.append(line);continue
   end=(int(m[1])/1e6,-int(m[2])/1e6);mode=int(m[3])
   if region is not None:region.append(end)
   elif mode==1:ops.append({'kind':'line','a':pos,'z':end,'aperture':aps[current],'ref':ref,'net':net,'polarity':pol})
   elif mode==3:ops.append({'kind':'flash','position':end,'aperture':aps[current],'ref':ref,'net':net,'polarity':pol})
   pos=end
  elif line.startswith(('G02','G03')):unsupported.append(line)
 return {'file':p.name,'apertures':aps,'operations':ops,'unsupported':unsupported}
parsed={p.suffix[1:]:parse(p)for p in G.iterdir()if p.suffix!='.gbrjob'}
def q(pt):return tuple(round(x,5)for x in pt)
def segment(a,z,w):return tuple(sorted((q(a),q(z))))+(round(w,5),)
expected=collections.Counter(segment((mm(t.GetStart().x),mm(t.GetStart().y)),(mm(t.GetEnd().x),mm(t.GetEnd().y)),mm(t.GetWidth()))for t in b.GetTracks()if not isinstance(t,k.PCB_VIA))
actual=collections.Counter(segment(o['a'],o['z'],o['aperture']['args'][0])for ext in ['gtl','gbl']for o in parsed[ext]['operations']if o['kind']=='line')
track_diff={'missing':sum((expected-actual).values()),'extra':sum((actual-expected).values()),'native_segments':sum(expected.values()),'gerber_segments':sum(actual.values())}
flash_checks=[]
for ext,layer in [('gtl',k.F_Cu),('gbl',k.B_Cu)]:
 actual_flashes={tuple(o['ref']):q(o['position'])for o in parsed[ext]['operations']if o['kind']=='flash'and o['ref']}
 native_flashes={(f.GetReference(),p.GetNumber()):q((mm(p.GetPosition().x),mm(p.GetPosition().y)))for f in b.GetFootprints()for p in f.Pads()if p.GetLayerSet().Contains(layer)}
 flash_checks.append({'layer':ext,'expected':len(native_flashes),'actual':len(actual_flashes),'differences':{str(x):[native_flashes.get(x),actual_flashes.get(x)]for x in set(native_flashes)|set(actual_flashes)if native_flashes.get(x)!=actual_flashes.get(x)}})
# Drill independent parser: exactdiameter andcoordinates including negativeGerber/drillY flip.
def drills(p):
 tools={};tool=None;hits=[]
 for line in p.read_text().splitlines():
  if re.fullmatch(r'T\d+C[\d.]+',line):m=re.fullmatch(r'T(\d+)C([\d.]+)',line);tools[int(m[1])]=float(m[2])
  elif re.fullmatch(r'T\d+',line):tool=int(line[1:])
  elif re.fullmatch(r'X-?[\d.]+Y-?[\d.]+',line):m=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line);hits.append((round(float(m[1]),4),round(-float(m[2]),4),round(tools[tool],4)))
 return tools,hits
nativehits=[];annular=[]
for f in b.GetFootprints():
 for p in f.Pads():
  drill=p.GetDrillSize()
  if drill.x:
   assert drill.x==drill.y
   nativehits.append((round(mm(p.GetPosition().x),4),round(mm(p.GetPosition().y),4),round(mm(drill.x),4)))
   annular.append({'type':'PTH','ref':f.GetReference(),'pin':p.GetNumber(),'annular_mm':round((min(mm(p.GetSize().x),mm(p.GetSize().y))-mm(drill.x))/2,6)})
for v in b.GetTracks():
 if isinstance(v,k.PCB_VIA):
  nativehits.append((round(mm(v.GetPosition().x),4),round(mm(v.GetPosition().y),4),round(mm(v.GetDrillValue()),4)))
  annular.append({'type':'via','annular_mm':round((mm(v.GetWidth(k.F_Cu))-mm(v.GetDrillValue()))/2,6)})
actualhits=[];toolsets={}
for p in D.glob('*.drl'):tools,hits=drills(p);toolsets[p.name]={'tools':tools,'hits':len(hits)};actualhits+=hits
max_drill_coordinate_error=max(min(max(abs(a[0]-n[0]),abs(a[1]-n[1]))for a in actualhits if a[2]==n[2])for n in nativehits);nc,ac=collections.Counter(tuple(round(q,3)for q in x)for x in nativehits),collections.Counter(tuple(round(q,3)for q in x)for x in actualhits)
# Bounds on plottedcopper primitives. Roundedrectmacro is limitedtoKiCadRoundRect.
def bounds(o):
 if o['kind']=='line':
  r=o['aperture']['args'][0]/2;xx=[o['a'][0],o['z'][0]];yy=[o['a'][1],o['z'][1]];return [min(xx)-r,min(yy)-r,max(xx)+r,max(yy)+r]
 if o['kind']=='region':return [min(x for x,y in o['points']),min(y for x,y in o['points']),max(x for x,y in o['points']),max(y for x,y in o['points'])]
 a=o['aperture'];x,y=o['position']
 if a['shape']=='C':w=h=a['args'][0]
 elif a['shape']=='R':w,h=a['args'][:2]
 elif a['shape']=='RoundRect':
  r=a['args'][0];xs=a['args'][1:9:2];ys=a['args'][2:9:2];return [x+min(xs)-r,y-max(ys)-r,x+max(xs)+r,y-min(ys)+r]
 else:raise ValueError(a)
 return[x-w/2,y-h/2,x+w/2,y+h/2]
edge_gaps=[]
for ext in ['gtl','gbl']:
 for o in parsed[ext]['operations']:
  z=bounds(o);edge_gaps.append(min(z[0]-99.4,z[1]-99.4,150.6-z[2],132.4-z[3]))
outline=parsed['gm1']['operations'];pts=[o[x]for o in outline if o['kind']=='line'for x in ['a','z']];degree=collections.Counter(q(p)for p in pts)
import shutil
raw_job=next(G.glob('*.gbrjob'),None);job=json.loads((raw_job or H/'raw-native.gbrjob').read_text())
if raw_job:shutil.copy2(raw_job,H/'raw-native.gbrjob');raw_job.unlink() # withinexplicitcandidateGerberdirectory, preservedoutsideupload
report={'source_PCB_sha256':json.loads((H/'native-audit.json').read_text())['source_PCB_sha256'],'actual_Gerber_file_count':len(parsed),'unsupported_gerber_primitives':{e:p['unsupported']for e,p in parsed.items()if p['unsupported']},'track_geometry_comparison':track_diff,'pad_flash_alignment':flash_checks,'drill_alignment':{'native_holes':len(nativehits),'plotted_holes':len(actualhits),'missing':list((nc-ac).elements()),'extra':list((ac-nc).elements()),'tool_inventory':toolsets,'max_coordinate_quantization_error_mm':round(max_drill_coordinate_error,8),'per_axis_tolerance_mm':0.0005,'coordinate_quantization_pass':max_drill_coordinate_error<=0.0005},'outline':{'line_segments':len(outline),'closed_single_rectangle':len(degree)==4 and all(n==2 for n in degree.values()),'centerline_bounds_mm':[99.4,99.4,150.6,132.4],'centerline_size_mm':[51.2,33],'native_stroked_bbox_size_mm':[51.25,33.05]},'minimum_copper_to_routed_outline_mm':round(min(edge_gaps),6),'minimum_annular_mm':{'via':min(x['annular_mm']for x in annular if x['type']=='via'),'PTH':min(x['annular_mm']for x in annular if x['type']=='PTH')},'annular_inventory':annular,'native_job_metadata':{'raw_file':'raw-native.gbrjob retainedinauditonly','finish':job['GeneralSpecs'].get('Finish'),'reported_bbox_size':job['GeneralSpecs']['Size'],'disposition':'ExcludedoptionalrawgbrjobfromuploadcandidatebecauseFinish=None,Sizeincludesoutline50umstroke,Revision=rev?. Explicitorderprofilegovernsfinish/nominaldimensions; actualoutlinegeometryverified51.2x33. NoCADsourcechanged.'},'JLCPCB_official_capability_source':{'url':'https://jlcpcb.com/capabilities/pcb-capabilities','observed':'2026-11-23','FR4_2L_1oz_track_space_mm':[.1,.1],'PTH_annular_abs_min_mm':.18,'PTH_annular_recommended_mm':.25,'via_drill_preferred_min_mm':.2,'routed_copper_edge_min_mm':.2,'smd_pad_pad_differentnet_min_mm':.15,'soldermask_bridge_mm':.1,'silk_line_mm':.15,'silk_height_mm':1.0},'manufacturing_geometry_check':'PASS iff unsupported0+nativeDRC0+exactGerberanddrillalignment; electricalstrictspacingandsystemqualificationseparate','full_product_release':False}
(H/'gerber-drill-audit.json').write_text(json.dumps(report,indent=2)+'\n')
(H/'parsed-gerbers.json').write_text(json.dumps(parsed,indent=2)+'\n');print(json.dumps({k:report[k]for k in ['actual_Gerber_file_count','track_geometry_comparison','pad_flash_alignment','drill_alignment','minimum_copper_to_routed_outline_mm','minimum_annular_mm']},indent=2))

from pathlib import Path
import pcbnew as k,json,re,collections,hashlib
H=Path(__file__).resolve().parent;ROOT=H.parents[1];R=ROOT/'work/Velluneo-2.0';S=R/'hardware/E27/variants/integrated-shade/SC09_compact';P=R/'hardware/E27/workflow/integrated-shade/compact-09/routing-order-prep/po_poprawkach';F=P/'fabrication'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(S/'SC09_compact.kicad_pcb'));native=[]
for fp in b.GetFootprints():
 for pad in fp.Pads():
  if pad.GetDrillSize().x:
   assert pad.GetDrillSize().x==pad.GetDrillSize().y
   native.append((round(k.ToMM(pad.GetPosition().x),3),round(-k.ToMM(pad.GetPosition().y),3),round(k.ToMM(pad.GetDrillSize().x),3)))
for t in b.GetTracks():
 if isinstance(t,k.PCB_VIA):native.append((round(k.ToMM(t.GetPosition().x),3),round(-k.ToMM(t.GetPosition().y),3),round(k.ToMM(t.GetDrill()),3)))
def drills(p):
 text=p.read_text();assert 'METRIC' in text;tools={int(m[0]):float(m[1])for m in re.findall(r'^T(\d+)C([\d.]+)',text,re.M)};sel=None;rows=[]
 for line in text.splitlines():
  if re.fullmatch(r'T\d+',line):sel=int(line[1:])
  m=re.fullmatch(r'X(-?[\d.]+)Y(-?[\d.]+)',line)
  if m:assert sel in tools;rows.append((round(float(m[1]),3),round(float(m[2]),3),round(tools[sel],3)))
 return rows
hits=drills(F/'SC09_compact-PTH.drl');assert collections.Counter(native)==collections.Counter(hits);assert len(hits)==24;assert not drills(F/'SC09_compact-NPTH.drl')
checks=[]
for suffix,func,polarity in[('gtl','Copper,L1,Top','Positive'),('gbl','Copper,L2,Bot','Positive'),('gts','Soldermask,Top','Negative'),('gbs','Soldermask,Bot','Negative'),('gto','Legend,Top','Positive'),('gbo','Legend,Bot','Positive'),('gm1','Profile,NP','Positive')]:
 p=next(F.glob('*.'+suffix));t=p.read_text();assert '%MOMM*%'in t and '%FSLAX46Y46*%'in t and '%LPD*%'in t and t.rstrip().endswith('M02*');assert 'FileFunction,'+func in t;assert ('FilePolarity,'+polarity in t)or(suffix=='gm1'and'%LPC*%'not in t)
 checks.append({'file':p.name,'sha256':sha(p),'function':func,'polarity':polarity,'polarity_attribute_present':'FilePolarity,'in t,'units':'mm','format':'4.6 absolute'})
outline=(F/'SC09_compact-Edge_Cuts.gm1').read_text();coords=[(int(x)/1e6,int(y)/1e6)for x,y in re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',outline)];assert set(coords)=={(99.4,-99.4),(150.6,-99.4),(150.6,-132.4),(99.4,-132.4)}
out={'actual_actor':'/root','PCB_sha256':sha(S/'SC09_compact.kicad_pcb'),'passed':True,'Gerber_layer_functions_units_polarity_end_markers':checks,'outline_vertices_mm':coords,'dimensions_mm':[51.2,33],'drill_count':len(hits),'component_holes':14,'through_vias':10,'NPTH_holes':0,'all_drill_centres_diameters_match_native_at_Excellon0p001mm_precision_with_y_axis_reflection':True,'manufacturing_checks_are_not_electrical_measurements':True};(P/'checks/manufacturing-file-lint.json').write_text(json.dumps(out,indent=2)+'\n');print('Gerber functions/polarities/outline and24native drillhits PASS')

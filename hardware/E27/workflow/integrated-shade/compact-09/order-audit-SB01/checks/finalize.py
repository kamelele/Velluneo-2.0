from pathlib import Path
import json,math,hashlib,zipfile,shutil,collections
import pcbnew as k
ROOT=Path.cwd();H=ROOT/'work/sc09-order-audit/fabrication';O=ROOT/'outputs/SC09_weryfikacja_i_kompendium/fabrication-candidate';S=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';b=k.LoadBoard(str(H/'native-copy/SC09_compact.kicad_pcb'));mm=k.ToMM;parsed=json.loads((H/'parsed-gerbers.json').read_text());audit=json.loads((H/'gerber-drill-audit.json').read_text());native=json.loads((H/'native-audit.json').read_text())
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def inside(p,poly):
 x,y=p;z=False
 for a,q in zip(poly,poly[1:]+poly[:1]):
  if (a[1]>y)!=(q[1]>y)and x<(q[0]-a[0])*(y-a[1])/(q[1]-a[1])+a[0]:z=not z
 return z
coverage=[];shapes=[]
for copper,mask,layer in [('gtl','gts',k.F_Cu),('gbl','gbs',k.B_Cu)]:
 reg=[o['points']for o in parsed[mask]['operations']if o['kind']=='region'];fs={tuple(o['ref']):o for o in parsed[copper]['operations']if o['kind']=='flash'and o['ref']};uncovered=[]
 for f in b.GetFootprints():
  for p in f.Pads():
   if not p.GetLayerSet().Contains(layer):continue
   pos=[mm(p.GetPosition().x),mm(p.GetPosition().y)];ref=(f.GetReference(),p.GetNumber())
   if not any(inside(pos,r)for r in reg):uncovered.append(ref)
   ap=fs[ref]['aperture'];a=ap['args']
   if ap['shape']=='C':size=[a[0],a[0]]
   elif ap['shape']=='R':size=a[:2]
   elif ap['shape']=='RoundRect':size=[max(a[1:9:2])-min(a[1:9:2])+2*a[0],max(a[2:9:2])-min(a[2:9:2])+2*a[0]]
   else:raise ValueError(ap)
   angle=p.GetOrientationDegrees()*math.pi/180;w,h=mm(p.GetSize().x),mm(p.GetSize().y);expected=[abs(w*math.cos(angle))+abs(h*math.sin(angle)),abs(w*math.sin(angle))+abs(h*math.cos(angle))]
   if max(abs(x-y)for x,y in zip(size,expected))>1e-5:shapes.append({'ref':ref,'layer':copper,'gerber_size':size,'native_rotated_bbox':expected})
 coverage.append({'layer':mask,'region_count':len(reg),'uncovered_native_pad_centres':uncovered,'note':'Back43regionscover44pads becauseadjacentconnectedpadopeningsaremerged; notmissingmask.'if mask=='gbs'else'All16padcentrescovered.'})
ports={f.GetReference():[{'pin':p.GetNumber(),'net':p.GetNetname().lstrip('/'),'position_absolute_mm':[mm(p.GetPosition().x),mm(p.GetPosition().y)],'position_relative_to_outline_min_mm':[mm(p.GetPosition().x)-99.4,mm(p.GetPosition().y)-99.4]}for p in f.Pads()]for f in b.GetFootprints()if f.GetReference()in ['J1','J2']}
audit['mask_coverage']=coverage;audit['pad_aperture_dimensions_vs_native_differences']=shapes;audit['native_port_pinmap']=ports;audit['silkscreen_native_board_text']=[{'text':t.GetText(),'height_mm':mm(t.GetTextHeight()),'stroke_mm':mm(t.GetTextThickness())}for t in b.GetDrawings()if isinstance(t,k.PCB_TEXT)];audit['minimum_track_width_mm']=min(native['track_widths_mm']);audit['adopted_min_different_net_clearance_mm']=.3;audit['clearance_basis']='FreshnativeDRC0withunmodifiedsourcecustomrules,notinferredfromrasterpreview.';audit['source_unchanged']=all(sha(S/p)==v for p,v in native['source_files'].items());audit['manufacturing_geometry_pass']=not shapes and all(not c['uncovered_native_pad_centres']for c in coverage)and all(not q['differences']for q in audit['pad_flash_alignment'])and not audit['drill_alignment']['missing']and not audit['drill_alignment']['extra']and audit['drill_alignment']['coordinate_quantization_pass']and not audit['track_geometry_comparison']['missing']and not audit['track_geometry_comparison']['extra']and not audit['unsupported_gerber_primitives']
(H/'gerber-drill-audit.json').write_text(json.dumps(audit,indent=2)+'\n');print(json.dumps({k:audit[k]for k in ['mask_coverage','pad_aperture_dimensions_vs_native_differences','manufacturing_geometry_pass']},indent=2))
profile={'revision':'SC09-SB01 source-bound barelaboratoryPCB candidate','PCB_source_sha256':native['source_PCB_sha256'],'nominal_dimensions_mm':[51.2,33],'layer_count':2,'base_material':'FR-4','thickness_mm':1.6,'outer_copper_oz':1,'finish':'Lead-free HASL','soldermask':'Green','silkscreen':'White, both sides','via_treatment':'Standard through vias, no via-in-pad/filledvia process requested','minimum_via_drill_mm':.3,'panelization':'Single board, routed outline; no Vscore','assembly':'None atJLCPCB; manualassembly separately','NPTH':'None, all26drillsPTH(12vias+14componentholes)','ordering_status':'NOT_RELEASED - no order placed','boundaries':'ManufacturabilityofbarePCBdoesnotestablish230Velectricalsafety orsystemqualification. Strictspacing23andexactcurrentstageacceptancependingrootreview.'}
(O/'ORDER_PROFILE_NOT_RELEASED.json').write_text(json.dumps(profile,indent=2)+'\n')
readme='''# SC09-SB01 fresh bare-PCB fabrication candidate - NOT RELEASED

This package was freshly exported from a read-only copy of PCB SHA256 a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19 using KiCad10.0.6. The electrical source was not edited. Source functional intent is 19references/46pins/11nets. Native ERC/DRC/schematicparity/unconnected findings are zero after copy-only refill. The independent physical pinpartition matches intent and the PCB. All143 Gerbersegments,60 nativepadflashes across bothfaces and26drillhits match native geometry (Excellon1umcoordinatequantization allowed; maxdeviation0.1um).

## Proposed bare-PCB order settings
FR-4,2layers,51.2x33mm nominal outline,1.6mm thickness,1oz copper,lead-freeHASL,greenmask,whitelegendbothfaces,singleCNC-routedboard. Manualassembly; noJLCPCBA/stencil/CPLorder is implied. Minimumtrace0.3mm,viahole0.3mm,viapad0.75mm,viaannular0.225mm,minimumcomponentPTHannular0.5mm,minimumcopperedgegap1.05mm. FreshDRCuses0.3mmdifferent-netmanufacturingfloor and1.0mmedgefloor. These dimensions exceed the cited JLCPCB fabrication minimums; this is not a safetyclearance assessment.

## Candidate upload archive
SC09_SB01_Gerber_Drill_CANDIDATE_NOT_RELEASED.zip contains sevenGerbers (F/Bcopper,F/Bmask,F/Bsilk,EdgeCuts) and the PTHExcellon26holes. The emptyNPTHfile is retained underdrills for audit only; there are noNPTH/slots. Drillmaps/reports and previews are outside the uploadZIP. All layers use absolute consistentcoordinates; Bside plotted files must NOT be manually mirrored.

Optional nativeGerberjob is deliberately excluded from this uploadZIP. Its rawFinish=None and bbox51.25x33.05 include historical/defaultmetadata and the50umoutlineplotstroke; it is preserved as raw-native.gbrjob in the audit directory. The actualrouted centerlineoutline is51.2x33.0. Use explicitorderprofile and verify actualcheckoutsettings; never infer finishfromtherawjob. Copper/outline/drillgeometry is not changed to hide the metadata issue.

## Limits / stop status
This is NOT a released fabrication package. Full strict functionalspacing still has23knownintrinsicpackage/shortescape findings, not waivedbyfabDRC. Updatedexactsource acceptance, outstandingstage/interface/spatialevidence and allphysicaloperating/current/thermal/startup/surge/faulttests remain open. The previousSC09-ROUTE05 fabrication acceptance does NOT automaticallycover the changedSB01 source. Root finalintegration/reviews decide whether this exactcandidate can be presented forbarelaboratoryPCBacceptance. No order orpoweredtest hasbeenperformed.

The old release-candidate Gerbers elsewhere in the project are historical and must not be combined with SB01BOM. J1.1=AC_L,J1.2=AC_N; J2.1=LED_PLUS,J2.2=DC_RETURN. LEDoutputismainsreferenced,notSELV. The earlier lampconcept's illustrative panelwires are not a validatedharness: nativeJ2is atlowX,oppositethehighXinputJ1.

## Official capability reference
https://jlcpcb.com/capabilities/pcb-capabilities, read23Nov2026. 2L1oz track/space0.10/0.10mm; adopteddesignfloor0.3mm. Routedcopperedge0.2mmfabminimum; designfloor1mm. PTHannularabsolute0.18mm,recommended0.25mm; actualcomponentPTH0.5mm. Via0.30/0.75mm exceedsstandardpreferredviahole0.2mm anddiameterdifference0.15mm. Whitelegendheight1.0mm/stroke0.15mm matchespublishedminima.
'''
(O/'README_NOT_RELEASED.md').write_text(readme,encoding='utf-8')
# Archive only exactproductiongeometry, flatnames; nooldrelease, defaultjob ordiagnosticimages.
selected=sorted((O/'gerbers').glob('*'))+[O/'drills/SC09_compact-PTH.drl']
manifest={'revision':'SC09-SB01-fabrication-candidate-2026-11-23','source_PCB_sha256':native['source_PCB_sha256'],'released':False,'upload_files':[{'path':p.name,'sha256':sha(p),'bytes':p.stat().st_size}for p in selected]}
with zipfile.ZipFile(O/'SC09_SB01_Gerber_Drill_CANDIDATE_NOT_RELEASED.zip','w',zipfile.ZIP_DEFLATED)as z:
 for p in selected:z.write(p,p.name)
manifest['upload_zip_sha256']=sha(O/'SC09_SB01_Gerber_Drill_CANDIDATE_NOT_RELEASED.zip');(O/'fabrication-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
for name in ['ERC.json','DRC-refilled.json','native-audit.json','gerber-drill-audit.json']:shutil.copy2(H/name,O/name)
print('Candidatezip',manifest['upload_zip_sha256'])

from pathlib import Path
import sys,json,hashlib,math,warnings,collections
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());sys.path.insert(0,str(W/'cam-libs'));from gerbonara import LayerStack,GerberFile,ExcellonFile
import fitz
D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-cleanup-10';F=D/'fabrication';notes=[]
with warnings.catch_warnings(record=True)as ws:
 warnings.simplefilter('always');stack=LayerStack.open(F);notes=[str(w.message)for w in ws]
assert set(stack.graphic_layers)=={('top','copper'),('inner_1','copper'),('inner_2','copper'),('bottom','copper'),('top','mask'),('bottom','mask'),('top','silk'),('bottom','silk'),('mechanical','outline')}
expected=json.loads((D/'checks/native-fabrication-input.json').read_text());actual=[]
for suffix,plated in(('PTH',True),('NPTH',False)):
 with warnings.catch_warnings(record=True)as ws:
  f=ExcellonFile.open(F/('Velluneo_driver-'+suffix+'.drl'),plated=plated);notes.extend(str(w.message)for w in ws)
 for o in f.objects:
  assert hasattr(o,'x')and hasattr(o,'y'),'No slots expected';actual.append(dict(x_mm=o.x,y_mm=o.y,diameter_mm=o.aperture.diameter,plated=plated))
remaining=list(actual)
for e in expected['expected_drills']:
 matches=[i for i,a in enumerate(remaining)if a['plated']==e['plated']and abs(a['diameter_mm']-e['diameter_mm'])<1e-6 and max(abs(a['x_mm']-e['x_mm']),abs(a['y_mm']-e['y_mm']))<=.000501];assert matches,e;remaining.pop(matches[0])
assert not remaining
outline=stack.outline;assert len(outline.objects)==4;vertices=[]
for o in outline.objects:vertices.extend([(o.x1,o.y1),(o.x2,o.y2)])
assert {tuple(round(x,6)for x in p)for p in vertices}=={(0.,0.),(45.,0.),(45.,60.),(0.,60.)}
layers=[]
for (side,kind),obj in stack.graphic_layers.items():
 key=side+'-'+kind;svg=str(obj.to_svg(force_bounds=((-.3,-.3),(45.3,60.3)),fg={'top':'#d23a36','bottom':'#3264b5','inner_1':'#38a36a','inner_2':'#c27d24'}.get(side,'black')));p=D/('CAM-'+key+'.svg');p.write_text(svg,encoding='utf-8');layers.append(dict(layer=key,objects=len(obj.objects),source_file=Path(obj.original_path).name if getattr(obj,'original_path',None)else None))
 doc=fitz.open(stream=svg.encode(),filetype='svg');pix=doc[0].get_pixmap(matrix=fitz.Matrix(4,4),alpha=False);pix.save(str(D/('CAM-'+key+'.png')))
for side in('top','bottom'):
 svg=str(stack.to_pretty_svg(side=side,force_bounds=((0,0),(45,60))));(D/('CAM-'+side+'-composite.svg')).write_text(svg,encoding='utf-8')
out=dict(parser='gerbonara1.5.0',source_board_sha256=expected['board_sha256'],layers=layers,drills=len(actual),plated=sum(a['plated']for a in actual),nonplated=sum(not a['plated']for a in actual),drills_match_native_positions_within_export_quantization=True,drill_axis_quantization_tolerance_mm=.000501,drill_sizes_plating_exact=True,origin_and_outline_exact_mm=[45,60],outline_closed_four_segments=True,parser_warnings=sorted(set(notes)),warning_disposition='Gerbonara warns on KiCad G90 placement after header; parsed coordinates checked within 3-decimal export rounding (0.0005mm per axis). Empty NPTH is explicitly classified using filename/plating, not heuristic output.',scope='Independent manufacturing-file parse, drill/outline/layer reconciliation and CAM images; not full electrical net extraction, vendor DFM acceptance or physical qualification.')
(D/'checks/CAM-validation.json').write_text(json.dumps(out,indent=2)+'\n');print('Independent CAM passed:',len(layers),'layers',len(actual),'holes')

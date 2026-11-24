"""Read-only native-to-Gerber/Excellon geometry comparison for a 2-layer PCB.

This does not export, save/refill CAD, delete a job file, order, or approve release.
"""
from pathlib import Path
from collections import Counter
import argparse,hashlib,json,math
from decimal import Decimal
import pcbnew as k
import formats as f
import kernel_sc08 as q

HERE=Path(__file__).resolve().parent
KERNEL_SHA='8b77118d3bfa321011991b686681548010032b6fcd95b57c87f0765026aa5d7a'
LAYERS={'F.Cu':k.F_Cu,'B.Cu':k.B_Cu}
FUNCTIONS={'Copper,L1,Top':'F.Cu','Copper,L2,Bot':'B.Cu','Soldermask,Top':'F.Mask','Soldermask,Bot':'B.Mask','Profile,NP':'Edge.Cuts','Legend,Top':'F.Silkscreen','Legend,Bot':'B.Silkscreen'}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def dump(p,x):Path(p).write_text(json.dumps(x,indent=2)+'\n',encoding='utf-8')
def num(x):return round(float(x),6)
def point(p):return num(k.ToMM(p.x)),num(k.ToMM(p.y))
def pt(p):return tuple(num(v)for v in p)
def segment(face,a,z,width):return face,tuple(sorted((pt(a),pt(z)))),num(width)
def geometry(x):return tuple(num(v)if isinstance(v,(int,float))else v for v in x)
def diff(expected,actual):
    e,a=Counter(expected),Counter(actual)
    return {'passed':e==a,'expected':sum(e.values()),'actual':sum(a.values()),'missing':[{'feature':x,'count':n}for x,n in (e-a).items()],'extra':[{'feature':x,'count':n}for x,n in (a-e).items()]}
def union(polys):
    z=k.SHAPE_POLY_SET()
    for p in polys:z.BooleanAdd(p)
    return z
def polygon(points):
    p=k.SHAPE_POLY_SET();p.NewOutline()
    if points[0]==points[-1]:points=points[:-1]
    if len(points)<3:raise f.Unsupported('Degenerate plotted polygon')
    for x,y in points:p.Append(int(round(x*1e6)),int(round(y*1e6)))
    if p.IsSelfIntersecting():raise f.Unsupported('Self-intersecting plotted contour unsupported')
    return p
def regions(ops):
    result=k.SHAPE_POLY_SET()
    for op in ops:
        if op['kind']!='region':raise f.Unsupported('Expected region-only geometry')
        region=k.SHAPE_POLY_SET()
        for contour in op['contours']:region.BooleanXor(polygon(contour))
        if op['polarity']=='dark':result.BooleanAdd(region)
        else:result.BooleanSubtract(region)
    return result

def mask_geometry(ops):
    """Checked Gerber dark geometry denotes openings on negative mask files.
    Preserve sequential dark/clear compositing; no drawing primitive is omitted.
    """
    result=k.SHAPE_POLY_SET()
    for op in ops:
        if op['kind']=='region':shape=regions([dict(op,polarity='dark')])
        elif op['kind']=='flash':
            name,w,h,r=f.aperture_geometry(op['aperture'])
            if not all(math.isfinite(x) for x in (w,h,r)) or min(w,h)<=0 or r<0 or r>min(w,h)/2:
                raise f.Unsupported('Invalid mask flash dimensions')
            p=k.PAD(None);p.SetSize(k.VECTOR2I(k.FromMM(w),k.FromMM(h)))
            p.SetPosition(k.VECTOR2I(*(k.FromMM(v) for v in op['position'])))
            p.SetShape({'C':k.PAD_SHAPE_CIRCLE,'R':k.PAD_SHAPE_RECT,'O':k.PAD_SHAPE_OVAL,'RoundRect':k.PAD_SHAPE_ROUNDRECT}[name])
            if name=='RoundRect':p.SetRoundRectRadiusRatio(r/min(w,h))
            shape=k.SHAPE_POLY_SET();p.TransformShapeToPolygon(shape,k.F_Cu,0,k.FromMM(.001),k.ERROR_OUTSIDE)
        else:raise f.Unsupported('Unsupported plotted mask primitive '+str(op['kind']))
        if op['polarity']=='dark':result.BooleanAdd(shape)
        elif op['polarity']=='clear':result.BooleanSubtract(shape)
        else:raise f.Unsupported('Unsupported mask primitive polarity')
    return result
def compare_polys(expected,actual,tol):
    def envelope(p):
        z=k.SHAPE_POLY_SET(p)
        if not z.IsEmpty():z.Inflate(k.FromMM(tol),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(.001))
        return z
    missing=q.clipped(expected,envelope(actual),False);extra=q.clipped(actual,envelope(expected),False)
    return {'passed':missing.IsEmpty()and extra.IsEmpty(),'comparison_envelope_mm':tol,'expected_area_mm2':expected.Area()/1e12,'actual_area_mm2':actual.Area()/1e12,'missing_outside_envelope_mm2':missing.Area()/1e12,'extra_outside_envelope_mm2':extra.Area()/1e12,'missing_bbox_mm':None if missing.IsEmpty()else[k.ToMM(v)for v in q.bbox(missing)],'extra_bbox_mm':None if extra.IsEmpty()else[k.ToMM(v)for v in q.bbox(extra)]}
def predict_mask_plot(b, layer):
    """Read-only mask closing prediction for pinned KiCad10.0.6.

    Plot behavior basis: plot_board_layers.cpp GenerateLayerPoly, GenerateLayerPoly function.
    Python does not expose DISABLE_ARC_RADIUS_CORRECTION. Native outside arc
    polygons are therefore compared under the EXISTING plot-error envelope;
    no larger tolerance or copper-spacing credit is introduced.
    Unsupported artwork/zone features stop rather than being omitted.
    """
    for item in b.GetDrawings():
        if item.IsOnLayer(layer):raise f.Unsupported('Mask drawing prediction unsupported')
    for fp in b.GetFootprints():
        if any(item.IsOnLayer(layer)for item in list(fp.GraphicalItems())+list(fp.GetFields())):
            raise f.Unsupported('Mask footprint artwork/text prediction unsupported')
    if any(z.IsOnLayer(layer)for z in b.Zones()):raise f.Unsupported('Mask zone prediction unsupported')
    width=b.GetDesignSettings().m_SolderMaskMinWidth
    if width<0:raise f.Unsupported('Negative mask min-width unsupported')
    if width==0:
        # Native simple mask plotting does not run the min-width closing path.
        exact=k.SHAPE_POLY_SET();error=b.GetDesignSettings().m_MaxError
        for fp in b.GetFootprints():fp.TransformPadsToPolySet(exact,layer,0,error,k.ERROR_OUTSIDE)
        for item in b.GetTracks():
            if isinstance(item,k.PCB_VIA):
                if item.IsTented(layer):continue
                copper=k.F_Cu if layer==k.F_Mask else k.B_Cu
                item.TransformShapeToPolygon(exact,copper,item.GetSolderMaskExpansion(),error,k.ERROR_OUTSIDE)
            elif item.IsOnLayer(layer):
                item.TransformShapeToPolygon(exact,layer,item.GetSolderMaskExpansion(),error,k.ERROR_OUTSIDE)
        return exact
    inflate=width//2-1
    if inflate<=0:raise f.Unsupported('Mask min-width must exceed2nm')
    error=b.GetDesignSettings().m_MaxError
    exact=k.SHAPE_POLY_SET();closed=k.SHAPE_POLY_SET()
    for fp in b.GetFootprints():
        fp.TransformPadsToPolySet(exact,layer,0,error,k.ERROR_OUTSIDE)
        fp.TransformPadsToPolySet(closed,layer,inflate,error,k.ERROR_OUTSIDE)
    for item in b.GetTracks():
        if not item.IsOnLayer(layer):continue
        clearance=item.GetSolderMaskExpansion()
        item.TransformShapeToPolygon(exact,layer,clearance,error,k.ERROR_OUTSIDE)
        item.TransformShapeToPolygon(closed,layer,clearance+inflate,error,k.ERROR_OUTSIDE)
    closed.Simplify()
    closed.Deflate(inflate,k.CORNER_STRATEGY_CHAMFER_ALL_CORNERS,error)
    closed.BooleanAdd(exact)
    return closed

def native_pad_geometry(p):
    angle=p.GetOrientationDegrees()%360
    if min(angle%90,90-angle%90)>1e-6:raise f.Unsupported('Non-orthogonal native pad unsupported')
    w,h=map(k.ToMM,(p.GetSize().x,p.GetSize().y))
    if round(angle/90)%2:w,h=h,w
    shape=p.GetShape()
    if shape==k.PAD_SHAPE_CIRCLE:
        if abs(w-h)>1e-6:raise f.Unsupported('Noncircular circle pad')
        return 'C',w,h,w/2
    if shape==k.PAD_SHAPE_RECT:return 'R',w,h,0.
    if shape==k.PAD_SHAPE_OVAL:return 'O',w,h,min(w,h)/2
    if shape==k.PAD_SHAPE_ROUNDRECT:
        r=k.ToMM(p.GetRoundRectCornerRadius());return ('RoundRect'if r else'R'),w,h,r
    raise f.Unsupported('Unsupported native pad shape '+str(shape))
def shape_bounds(op):
    if op['kind']=='line':
        if op['aperture']['shape']!='C':raise f.Unsupported('Line without circular aperture')
        r=op['aperture']['args'][0]/2;xs=[op['a'][0],op['z'][0]];ys=[op['a'][1],op['z'][1]]
        return min(xs)-r,min(ys)-r,max(xs)+r,max(ys)+r
    if op['kind']=='region':
        points=[p for c in op['contours']for p in c];return min(p[0]for p in points),min(p[1]for p in points),max(p[0]for p in points),max(p[1]for p in points)
    name,w,h,r=f.aperture_geometry(op['aperture']);x,y=op['position'];return x-w/2,y-h/2,x+w/2,y+h/2
def drill_match(expected,actual,tol=.0005):
    remaining=list(actual);missing=[];maximum=0.
    for native in expected:
        candidates=[(max(abs(Decimal(str(hit['position'][axis]))-Decimal(str(native['position'][axis]))) for axis in (0,1)),i)for i,hit in enumerate(remaining)if hit['plated']==native['plated']and abs(hit['diameter']-native['diameter'])<=.000001]
        if not candidates or min(candidates)[0]>Decimal(str(tol)):missing.append(native);continue
        error,index=min(candidates);maximum=max(maximum,float(error));remaining.pop(index)
    return {'passed':not missing and not remaining,'native_holes':len(expected),'plotted_holes':len(actual),'missing':missing,'extra':remaining,'per_axis_tolerance_mm':tol,'coordinate_comparison':'Exact Decimal of parsed/native decimal coordinates; unchanged inclusive per-axis tolerance','maximum_matched_coordinate_error_mm':maximum}
def outline(board):
    edges=[]
    for x in board.GetDrawings():
        if x.GetLayer()!=k.Edge_Cuts:continue
        if x.GetShape()!=k.SHAPE_T_SEGMENT:raise f.Unsupported('Only a closed native rectangular straight outline is supported')
        edges.append((point(x.GetStart()),point(x.GetEnd()),k.ToMM(x.GetWidth())))
    vertices={p for a,z,w in edges for p in (a,z)};degree=Counter(p for a,z,w in edges for p in (a,z))
    if len(edges)!=4 or len(vertices)!=4 or set(degree.values())!={2}:raise f.Unsupported('Native outline is not one four-edge rectangle')
    xs=sorted({p[0]for p in vertices});ys=sorted({p[1]for p in vertices})
    if len(xs)!=2 or len(ys)!=2 or vertices!={(x,y)for x in xs for y in ys}or any(a[0]!=z[0]and a[1]!=z[1]for a,z,w in edges):raise f.Unsupported('Unsupported native profile shape')
    return edges,[xs[0],ys[0],xs[1],ys[1]]
def mask_web(poly):
    pieces=[]
    for i in range(poly.OutlineCount()):
        ring=poly.COutline(i);pieces.append(polygon([point(ring.CPoint(j))for j in range(ring.PointCount())]))
    best=None
    for i,a in enumerate(pieces):
        aa=q.bbox(a)
        for b in pieces[i+1:]:
            bb=q.bbox(b);lower=math.hypot(max(aa[0]-bb[2],bb[0]-aa[2],0),max(aa[1]-bb[3],bb[1]-aa[3],0))/1e6
            if best is not None and lower>=best:continue
            best=q.actual_gap(a,b,math.hypot(max(abs(aa[0]-bb[2]),abs(bb[0]-aa[2])),max(abs(aa[1]-bb[3]),abs(bb[1]-aa[3])))/1e6+.01)
    return best

def audit(board,gerber_dir,drill_dir,profile):
    board=Path(board).resolve();gd=Path(gerber_dir).resolve();dd=Path(drill_dir).resolve();profile=Path(profile).resolve()
    artifacts=sorted([p for p in gd.iterdir()if p.is_file()]+[p for p in dd.iterdir()if p.is_file()]);inputs=[board,profile]+artifacts;before={str(p):sha(p)for p in inputs};result={'tool':'SB02 generic read-only fabrication geometry audit','checker_sha256':sha(__file__),'formats_sha256':sha(HERE/'formats.py'),'native_kernel_sha256':sha(HERE/'kernel_sc08.py'),'inputs':before,'passed':False,'full_product_release':False,'order_submitted':False,'limits':['Source-bound geometry comparison is not native ERC/DRC, electrical acceptance, insulation/thermal/EMC qualification or human fabrication approval.','Copper pad contacts and drill hits are preserved as multisets; duplicate ref/pin identities are never deduplicated.','Straight tracks, orthogonal circle/rectangle/oval/roundrect pads, through round drills and rectangular outline only; unsupported geometry or commands fail closed.','Mask/zone polygon comparisons use an explicitly reported source plot-error envelope, not manufacturing spacing credit.','Silkscreen file metadata/presence are checked; its detailed artwork and text quality remain separate native DRC and visual review.','No native CAD export/save/refill, gbrjob deletion or modification of input artifacts is performed.']}
    findings=[]
    try:
        if k.GetBuildVersion()!='10.0.6'or sha(HERE/'kernel_sc08.py')!=KERNEL_SHA:raise f.Unsupported('Pinned KiCad10.0.6/frozen kernel required')
        cfg=load(profile)
        required={'copper_layers','thickness_mm','copper_oz','finish','minimum_copper_edge_mm','minimum_mask_web_mm'}
        if not required<=cfg.keys()or cfg['copper_layers']!=2 or cfg['copper_oz']!=1 or not cfg['finish']:raise f.Unsupported('Explicit 2-layer/1oz fabrication profile required')
        b=q.load_native(board)
        if q.raw_track_nets(board)!={t.m_Uuid.AsString():t.GetNetname()for t in b.GetTracks()}:raise f.Unsupported('Raw track net identity changed during native load')
        if b.GetCopperLayerCount()!=2 or abs(k.ToMM(b.GetDesignSettings().GetBoardThickness())-cfg['thickness_mm'])>1e-6:raise f.Unsupported('Native layer count/thickness differs from fabrication profile')
        filemap={};jobs=[]
        for p in gd.iterdir():
            if not p.is_file():continue
            if p.suffix=='.gbrjob':jobs.append({'file':p.name,'metadata':load(p)});continue
            meta=f.metadata(p);function=meta.get('FileFunction')
            if function not in FUNCTIONS:raise f.Unsupported('Unexpected fabrication-layer file/function '+p.name+' '+str(function))
            face=FUNCTIONS[function]
            if face in filemap:raise f.Unsupported('Duplicate Gerber face '+face)
            filemap[face]={'path':p,'metadata':meta}
        if set(filemap)!=set(FUNCTIONS.values()):raise f.Unsupported('Exactly seven required Gerber layer functions must be present')
        parsed={face:f.gerber(x['path'])for face,x in filemap.items()if face not in ('F.Silkscreen','B.Silkscreen')}
        for face,entry in filemap.items():
            want='Negative'if face.endswith('.Mask')else'Positive'
            actual_polarity=entry['metadata'].get('FilePolarity','Positive'if face=='Edge.Cuts'else None)
            if actual_polarity!=want:raise f.Unsupported('Unexpected Gerber file polarity '+face)
        edge_native,bounds=outline(b);edge_ops=parsed['Edge.Cuts']['operations']
        if any(o['kind']!='line'or o['polarity']!='dark'or o['aperture']['shape']!='C'for o in edge_ops):raise f.Unsupported('Unsupported plotted profile primitive')
        result['outline']=diff([segment('Edge.Cuts',a,z,w)for a,z,w in edge_native],[segment('Edge.Cuts',o['a'],o['z'],o['aperture']['args'][0])for o in edge_ops]);result['outline'].update(centerline_bounds_mm=bounds,centerline_size_mm=[bounds[2]-bounds[0],bounds[3]-bounds[1]])
        expected_tracks=[];actual_tracks=[];expected_pads=[];actual_pads=[];expected_vias=[];actual_vias=[];drills=[];pad_inventory=[];masks={x:[]for x in ('F.Mask','B.Mask')};zone_expected={x:[]for x in LAYERS}
        for g in b.GetDrawings():
            if g.GetLayer()in LAYERS.values():raise f.Unsupported('Free native copper graphics/text unsupported')
        for fp in b.GetFootprints():
            for g in list(fp.GraphicalItems())+[fp.Reference(),fp.Value()]:
                if g.GetLayer()in LAYERS.values():raise f.Unsupported('Footprint copper graphics/text unsupported')
            for p in fp.Pads():
                if p.GetAttribute()==k.PAD_ATTRIB_NPTH:raise f.Unsupported('NPTH native pads need a separately qualified export adapter')
                contacts=[]
                for face,ly in LAYERS.items():
                    if p.IsOnLayer(ly):
                        record=(face,fp.GetReference(),p.GetNumber(),point(p.GetPosition()),geometry(native_pad_geometry(p)),p.GetNetname());expected_pads.append(record);contacts.append(face)
                if contacts:pad_inventory.append({'ref':fp.GetReference(),'pin':p.GetNumber(),'uuid':p.m_Uuid.AsString(),'position_mm':point(p.GetPosition()),'faces':contacts})
                drill=p.GetDrillSize()
                if drill.x or drill.y:
                    if drill.x!=drill.y or drill.x<=0:raise f.Unsupported('Slotted/unsupported native drill')
                    drills.append({'position':point(p.GetPosition()),'diameter':k.ToMM(drill.x),'plated':True,'source':fp.GetReference()+'.'+p.GetNumber(),'uuid':p.m_Uuid.AsString()})
                for face,ly in [('F.Mask',k.F_Mask),('B.Mask',k.B_Mask)]:
                    if p.IsOnLayer(ly):
                        poly=k.SHAPE_POLY_SET();p.TransformShapeToPolygon(poly,ly,p.GetSolderMaskExpansion(ly),k.FromMM(.002),k.ERROR_OUTSIDE);masks[face].append(poly)
        for t in b.GetTracks():
            if isinstance(t,k.PCB_VIA):
                if t.GetViaType()!=k.VIATYPE_THROUGH:raise f.Unsupported('Blind/buried via unsupported')
                for face,ly in LAYERS.items():expected_vias.append((face,point(t.GetPosition()),geometry(('C',k.ToMM(t.GetWidth(ly)),k.ToMM(t.GetWidth(ly)),k.ToMM(t.GetWidth(ly))/2)),t.GetNetname()))
                drills.append({'position':point(t.GetPosition()),'diameter':k.ToMM(t.GetDrillValue()),'plated':True,'source':'via','uuid':t.m_Uuid.AsString()})
                for face,ly in [('F.Mask',k.F_Mask),('B.Mask',k.B_Mask)]:
                    if not t.IsTented(ly):
                        poly=k.SHAPE_POLY_SET();t.TransformShapeToPolygon(poly,k.F_Cu if face=='F.Mask'else k.B_Cu,t.GetSolderMaskExpansion(),k.FromMM(.002),k.ERROR_OUTSIDE);masks[face].append(poly)
            else:
                if isinstance(t,k.PCB_ARC)or t.GetLayer()not in LAYERS.values():raise f.Unsupported('Unsupported native copper track')
                expected_tracks.append(segment(k.LayerName(t.GetLayer()),point(t.GetStart()),point(t.GetEnd()),k.ToMM(t.GetWidth())))
        for z in b.Zones():
            if z.GetIsRuleArea():continue
            if not z.IsFilled()or z.NeedRefill():raise f.Unsupported('Unfilled/stale native copper zone')
            for face,ly in LAYERS.items():
                if z.IsOnLayer(ly):zone_expected[face].append(k.SHAPE_POLY_SET(z.GetFilledPolysList(ly)))
        gaps=[];zones_actual={x:[]for x in LAYERS}
        for face in LAYERS:
            for op in parsed[face]['operations']:
                if op['kind']=='region':zones_actual[face].append(op)
                else:
                    if op['polarity']!='dark':raise f.Unsupported('Clear copper line/flash unsupported')
                    if op['kind']=='line':
                        if op['aperture']['shape']!='C':raise f.Unsupported('Copper line requires circular aperture')
                        actual_tracks.append(segment(face,op['a'],op['z'],op['aperture']['args'][0]))
                    else:
                        geo=geometry(f.aperture_geometry(op['aperture']));function=op['aperture']['function']or''
                        if function.startswith('ViaPad')and op['ref']is None:actual_vias.append((face,pt(op['position']),geo,op['net']))
                        elif function.startswith(('ComponentPad','SMDPad'))and op['ref']is not None:actual_pads.append((face,*op['ref'],pt(op['position']),geo,op['net']))
                        else:raise f.Unsupported('Unclassified copper flash '+str(op))
                if op['polarity']=='dark':
                    z=shape_bounds(op);gaps.append(min(z[0]-bounds[0],z[1]-bounds[1],bounds[2]-z[2],bounds[3]-z[3]))
        result['track_geometry_by_face']=diff(expected_tracks,actual_tracks);result['physical_pad_flashes_by_face']=diff(expected_pads,actual_pads);result['via_flashes_by_face']=diff(expected_vias,actual_vias);result['physical_contact_inventory']=pad_inventory
        plotted_drills=[];toolsets=[]
        for p in dd.glob('*.drl'):
            x=f.excellon(p);toolsets.append({'file':p.name,'tools':x['tools'],'hits':len(x['hits']),'plated':x['plated']});plotted_drills.extend(dict(hit,plated=x['plated'])for hit in x['hits'])
        result['drill_alignment']=drill_match(drills,plotted_drills);result['drill_alignment']['tool_inventory']=toolsets
        plot_error=k.ToMM(b.GetDesignSettings().m_MaxError)
        if not 0<plot_error<=.01:raise f.Unsupported('Unsupported source plot-error envelope')
        envelope=2*plot_error+.002;result['mask_profile']={};result['zone_regions']={}
        for face in LAYERS:result['zone_regions'][face]=compare_polys(union(zone_expected[face]),regions(zones_actual[face]),envelope)
        for face in masks:
            mask_ops=parsed[face]['operations']
            actual=mask_geometry(mask_ops);expected_mask=predict_mask_plot(b,k.F_Mask if face=='F.Mask'else k.B_Mask);entry=compare_polys(expected_mask,actual,envelope);entry['prediction']='KiCad10.0.6 direct openings when min-width zero, otherwise original min-width closing; unchanged numeric envelope';entry['plotted_primitive_counts']=dict(Counter(o['kind'] for o in mask_ops));entry['native_mask_min_width_mm']=k.ToMM(b.GetDesignSettings().m_SolderMaskMinWidth);entry['minimum_separate_opening_web_mm']=mask_web(actual);entry['minimum_web_target_mm']=cfg['minimum_mask_web_mm']
            if entry['minimum_separate_opening_web_mm']is not None and entry['minimum_separate_opening_web_mm']<cfg['minimum_mask_web_mm']:entry['passed']=False
            result['mask_profile'][face]=entry
        result['minimum_plotted_copper_edge_mm']=min(gaps)if gaps else None;result['copper_edge_target_mm']=cfg['minimum_copper_edge_mm']
        if not gaps or min(gaps)+1e-6<cfg['minimum_copper_edge_mm']:findings.append('Plotted copper-to-routed-edge target not met')
        for key in ('outline','track_geometry_by_face','physical_pad_flashes_by_face','via_flashes_by_face','drill_alignment'):
            if not result[key]['passed']:findings.append(key+' mismatch')
        for group in ('mask_profile','zone_regions'):
            for face,entry in result[group].items():
                if not entry['passed']:findings.append(group+' '+face+' mismatch')
        result['fabrication_profile']=cfg;result['raw_job_metadata_read_only']=jobs;result['gerber_layer_inventory']={face:{'file':x['path'].name,'metadata':x['metadata']}for face,x in filemap.items()};result['findings']=findings;result['passed']=not findings
    except Exception as e:result.update(passed=False,stopped=True,error=type(e).__name__+': '+str(e),findings=findings)
    result['inputs_after']={str(p):sha(p)for p in inputs};result['input_unchanged']=before==result['inputs_after'];result['artifact_inventory_unchanged']=artifacts==sorted([p for p in gd.iterdir()if p.is_file()]+[p for p in dd.iterdir()if p.is_file()])
    if not result['input_unchanged']or not result['artifact_inventory_unchanged']:result['passed']=False
    return result

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--board',required=True);p.add_argument('--gerbers',required=True);p.add_argument('--drills',required=True);p.add_argument('--profile',required=True);p.add_argument('--report',required=True);a=p.parse_args();r=audit(a.board,a.gerbers,a.drills,a.profile);dump(a.report,r);print(json.dumps({x:r.get(x)for x in ('passed','stopped','error','findings','input_unchanged','artifact_inventory_unchanged')}));raise SystemExit(0 if r['passed']else 1)

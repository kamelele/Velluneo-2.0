"""Read/propose native KiCad geometry in the matching pcbnew Python runtime."""
import base64
import html
import json
import re
import sys
import uuid
from pathlib import Path
import pcbnew as pcb


def vector(x,y):return pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y))
def xy(v):return [v.x,v.y]
def items(container):
    # Ubuntu's pcbnew DRAWINGS/PADS wrappers call the removed iterator.next().
    # Indexed native-container access works on both validated runtimes.
    values=[container[i] for i in range(len(container))]
    return [value.Cast() if hasattr(value,'Cast') else value for value in values]
def segments(rect):
    a,b,c,d=rect
    points=[vector(a,b),vector(c,b),vector(c,d),vector(a,d)]
    return {tuple(sorted((tuple(xy(points[i])),tuple(xy(points[(i+1)%4]))))) for i in range(4)}


def run(request,output):
    version=pcb.Version()
    if version not in ['10.0.6','10.0.6+dfsg-1']:raise ValueError('Unsupported pcbnew runtime: '+version)
    board_path=Path(request['board']);before=board_path.read_bytes();board=pcb.LoadBoard(str(board_path))
    data=request['model']['payload'];propose=request['propose'];errors=[];changed=False
    declared=data.get('copper_layers',['F.Cu','B.Cu'])
    if len(declared) not in [2,4]:raise ValueError('Only validated two/four-layer spatial stacks supported')
    actual_layers=[board.GetLayerName(layer) for layer in items(board.GetEnabledLayers().Seq()) if pcb.IsCopperLayer(layer)]
    if set(actual_layers)!=set(declared) or board.GetCopperLayerCount()!=len(declared):
        raise ValueError('Declared copper stack differs from enabled native layers')
    def native_layer(name):
        layer=board.GetLayerID(name)
        if not pcb.IsCopperLayer(layer) or not board.GetEnabledLayers().Contains(layer):
            raise ValueError('Disabled or non-copper spatial layer: '+name)
        return layer
    expected=segments(data['outline_mm']);edges=[x for x in items(board.Drawings()) if x.GetLayer()==pcb.Edge_Cuts]
    actual={tuple(sorted((tuple(xy(x.GetStart())),tuple(xy(x.GetEnd()))))) for x in edges if x.GetShape()==pcb.SHAPE_T_SEGMENT}
    if not edges and propose:
        for start,end in sorted(expected):
            edge=pcb.PCB_SHAPE(board);edge.SetShape(pcb.SHAPE_T_SEGMENT);edge.SetLayer(pcb.Edge_Cuts)
            edge.SetUuid(pcb.KIID(str(uuid.uuid5(uuid.NAMESPACE_URL,'electronics-rules/outline/'+str((start,end))))))
            edge.SetStart(pcb.VECTOR2I(*start));edge.SetEnd(pcb.VECTOR2I(*end));edge.SetWidth(pcb.FromMM(.05));board.Add(edge)
        changed=True
    elif actual!=expected or len(edges)!=4:errors.append('Saved outline differs or uses unsupported arcs/cutouts; existing outline preserved')
    expected_names={'HW-SPATIAL-'+area['id'] for area in data['areas']}
    for area in data['areas']:
        name='HW-SPATIAL-'+area['id'];found=[z for z in items(board.Zones()) if z.GetZoneName()==name]
        expected_uuid=str(uuid.uuid5(uuid.NAMESPACE_URL,'electronics-rules/spatial/'+area['id']))
        if not found and propose:
            zone=pcb.ZONE(board);zone.SetUuid(pcb.KIID(expected_uuid));zone.SetZoneName(name);zone.SetIsRuleArea(True)
            layer_set=pcb.LSET()
            for layer in area['layers']:layer_set.AddLayer(native_layer(layer))
            zone.SetLayerSet(layer_set)
            for setter in ['SetDoNotAllowTracks','SetDoNotAllowVias','SetDoNotAllowPads','SetDoNotAllowFootprints','SetDoNotAllowZoneFills']:getattr(zone,setter)(False)
            polygon=zone.Outline();polygon.NewOutline();a,b,c,d=area['rectangle_mm']
            for x,y in [(a,b),(c,b),(c,d),(a,d)]:polygon.Append(pcb.FromMM(x),pcb.FromMM(y))
            board.Add(zone);found=[zone];changed=True
        if len(found)!=1:
            errors.append('Missing or duplicate named spatial area: '+name);continue
        zone=found[0];poly=zone.Outline()
        wanted_layers={native_layer(x) for x in area['layers']}
        points=[]
        if poly.OutlineCount()==1 and poly.HoleCount(0)==0:
            outline=poly.Outline(0)
            points=[tuple(xy(outline.CPoint(i))) for i in range(outline.PointCount())]
        polygon_segments={tuple(sorted((points[i],points[(i+1)%len(points)]))) for i in range(len(points))} if points else set()
        if (str(zone.m_Uuid.AsString())!=expected_uuid or not zone.GetIsRuleArea() or
            set(items(zone.GetLayerSet().Seq()))!=wanted_layers or polygon_segments!=segments(area['rectangle_mm']) or len(points)!=4 or
            any(getattr(zone,getter)() for getter in ['GetDoNotAllowTracks','GetDoNotAllowVias','GetDoNotAllowPads','GetDoNotAllowFootprints','GetDoNotAllowZoneFills'])):
            errors.append('Spatial area geometry/identity/flags differ; manual migration required: '+name)
    for zone in items(board.Zones()):
        if zone.GetZoneName().startswith('HW-SPATIAL-') and zone.GetZoneName() not in expected_names:
            errors.append('Unexpected managed spatial area; manual migration required: '+zone.GetZoneName())
    # Schematic net labels need not be simple identifiers, but exception scopes must
    # resolve to an actual named PCB net rather than an ineffectual wildcard.
    net_names={str(n.GetNetname()) for n in board.GetNetsByNetcode().values()}
    for area in data['areas']:
        for exception in area['exceptions']:
            if exception['net'] not in net_names:errors.append('Exception net missing from PCB: '+exception['net'])
    xmin,ymin,xmax,ymax=data['outline_mm'];svg=[];footprints=[];pads={}
    svg.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="black" stroke-width="0.15"/>'%(xmin,ymin,xmax-xmin,ymax-ymin))
    for area in data['areas']:
        a,b,c,d=area['rectangle_mm'];svg.append('<rect x="%s" y="%s" width="%s" height="%s" fill="red" fill-opacity="0.12" stroke="red" stroke-width="0.12"/>'%(a,b,c-a,d-b))
        svg.append('<text x="%s" y="%s" font-size="0.9">%s</text>'%(a,b,html.escape(area['id'])))
    for fp in items(board.Footprints()):
        bbox=fp.GetBoundingBox();x,y=pcb.ToMM(bbox.GetX()),pcb.ToMM(bbox.GetY());w,h=pcb.ToMM(bbox.GetWidth()),pcb.ToMM(bbox.GetHeight())
        footprints.append({'reference':fp.GetReference(),'envelope_mm':[x,y,w,h]})
        xmin=min(xmin,x);ymin=min(ymin,y);xmax=max(xmax,x+w);ymax=max(ymax,y+h)
        svg.append('<rect x="%s" y="%s" width="%s" height="%s" fill="none" stroke="blue" stroke-width="0.1"/>'%(x,y,w,h))
        svg.append('<text x="%s" y="%s" font-size="0.9">%s</text>'%(x,y,html.escape(fp.GetReference())))
        for pad in items(fp.Pads()):
            x,y=pcb.ToMM(pad.GetPosition().x),pcb.ToMM(pad.GetPosition().y)
            svg.append('<circle cx="%s" cy="%s" r="0.22" fill="blue"/>'%(x,y))
            if pad.GetNetname():pads.setdefault(pad.GetNetname(),[]).append((x,y))
    for points in pads.values():
        for x,y in points[1:]:
            a,b=points[0];svg.append('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="green" stroke-width="0.08" stroke-dasharray="0.4 0.3"/>'%(a,b,x,y))
    image='<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s %s %s %s">%s</svg>'%(xmin-2,ymin-2,xmax-xmin+4,ymax-ymin+4,''.join(svg))
    result={'errors':errors,'svg':image,'inventory':{'footprints':footprints,'area_count':len(data['areas']),'pcbnew_version':version},'proposed_board':None}
    if changed and propose and not errors:
        proposed=output.with_name('spatial-proposed.kicad_pcb');pcb.SaveBoard(str(proposed),board)
        result['proposed_board']=base64.b64encode(proposed.read_bytes()).decode()
    if board_path.read_bytes()!=before:raise ValueError('Board changed during spatial inspection')
    output.write_text(json.dumps(result),encoding='utf-8')


if __name__=='__main__':
    run(json.loads(Path(sys.argv[1]).read_text(encoding='utf-8')),Path(sys.argv[2]))

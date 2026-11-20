"""Independent native-shape boundary coverage diagnostic; no customer CAD writes."""
import json,hashlib,math
from pathlib import Path
import pcbnew as k
OUT=Path(__file__).resolve().parent
S=OUT.parent/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC08_prototype'
P=S/'SC08_prototype.kicad_pcb'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
before=sha(P)
assert before=='c503ff1b7660022d665ed4fabbc536c8f05d72899694a1d2da2c8a84ec6357d5'
b=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(P))
fp=next(f for f in b.GetFootprints() if f.GetReference()=='U1')
edges=[((g.GetStart().x,g.GetStart().y),(g.GetEnd().x,g.GetEnd().y)) for g in fp.GraphicalItems() if g.GetLayer()==k.F_CrtYd]
edge=edges.pop();vertices=[edge[0],edge[1]]
while edges:
    edge=next(e for e in edges if vertices[-1] in e);edges.remove(edge)
    vertices.append(edge[1] if vertices[-1]==edge[0] else edge[0])
assert vertices[0]==vertices[-1]
region=k.SHAPE_POLY_SET();region.NewOutline()
for x,y in vertices[:-1]:region.Append(x,y)
ERROR=.0002;STEP=.0025
region.Inflate(k.FromMM(1.0),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,k.FromMM(ERROR))
foreign=[]
for pad in fp.Pads():
    if pad.GetNumber()=='4':continue
    poly=k.SHAPE_POLY_SET()
    pad.TransformShapeToPolygon(poly,k.F_Cu,0,k.FromMM(ERROR),k.ERROR_INSIDE)
    foreign.append((pad.GetNumber(),poly))
samples=[];max_d=-1;max_info=None
for oi in range(region.OutlineCount()):
    line=region.Outline(oi)
    for j in range(line.PointCount()):
        a=line.CPoint(j);z=line.CPoint((j+1)%line.PointCount())
        count=max(1,math.ceil(math.hypot(z.x-a.x,z.y-a.y)/k.FromMM(STEP)))
        for n in range(count):
            point=k.VECTOR2I(round(a.x+(z.x-a.x)*n/count),round(a.y+(z.y-a.y)*n/count))
            distances=[(k.ToMM(poly.Distance(point)),pin) for pin,poly in foreign]
            distance,pin=min(distances)
            if distance>max_d:
                max_d=distance;max_info={'point_mm':[k.ToMM(point.x),k.ToMM(point.y)],'nearest_foreign_pin':pin,'minimum_gap_mm':distance}
            samples.append({'point_mm':[k.ToMM(point.x),k.ToMM(point.y)],'nearest_foreign_pin':pin,'minimum_gap_mm':distance})
upper=max_d+STEP/2+2*ERROR+.000002
report={'source_board_sha256':before,'tool':'KiCad '+k.GetBuildVersion(),'scope':'Independent native U1 foreign-pad coverage of maximum one-mm rounded courtyard escape boundary; no routed copper','sampling_pitch_max_mm':STEP,'polygon_error_mm':ERROR,'sample_count':len(samples),'maximum_minimum_pad_distance_sample':max_info,'conservative_continuous_upper_bound_mm':upper,'generic_required_gap_mm':4.0,'whole_escape_boundary_covered_by_foreign_pad_4mm_neighborhood':upper<4.0,'foreign_pins':[pin for pin,poly in foreign],'method':'Native inward foreign pad polygon distances upper-bound true pad distance. Segment sampling is bounded by 1-Lipschitz distance with half pitch; two polygon-error reserves plus coordinate rounding are added. A covered closed maximum-escape boundary prevents even a zero-width continuous drain conductor from reaching exterior without violating a generic pair gap. Actual nonzero conductor width cannot improve this.'}
assert sha(P)==before
(OUT/'boundary-report.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
(OUT/'boundary-samples.json').write_text(json.dumps(samples,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report,indent=2))
disk_results=[]
for width in (.6,.3):
    radius=width/2-.005
    worst=None;failures=[];checked=0
    for sample in samples:
        # An inside-radius witness, >.005mm outside the envelope and within4mm
        # of a foreign pad proves violation for a nearby centerline crossing.
        # This is only a diagnostic until every boundary sample is covered.
        px,py=sample['point_mm'];best=None
        for i in range(64):
            theta=2*math.pi*i/64
            point=k.VECTOR2I(k.FromMM(px+radius*math.cos(theta)),k.FromMM(py+radius*math.sin(theta)))
            outside=k.ToMM(region.Distance(point))
            if outside<.005:continue
            distance,pin=min((k.ToMM(poly.Distance(point)),pin) for pin,poly in foreign)
            candidate={'foreign_gap_mm':distance,'foreign_pin':pin,'outside_region_mm':outside,'witness_mm':[k.ToMM(point.x),k.ToMM(point.y)]}
            if best is None or distance<best['foreign_gap_mm']:best=candidate
        checked+=1
        if best is None or best['foreign_gap_mm']>=3.995:
            failures.append({'center_mm':[px,py],'best':best})
        if best and (worst is None or best['foreign_gap_mm']>worst['best']['foreign_gap_mm']):worst={'center_mm':[px,py],'best':best}
    disk_results.append({'width_mm':width,'witness_radius_mm':radius,'sample_count':checked,'uncovered_centers':failures,'worst_witness':worst,'closed_with_witness_margin':not failures})
(OUT/'disk-boundary-report.json').write_text(json.dumps(disk_results,indent=2)+'\n',encoding='utf-8')
print(json.dumps([{'width_mm':r['width_mm'],'uncovered_count':len(r['uncovered_centers']),'worst_witness':r['worst_witness']} for r in disk_results],indent=2))

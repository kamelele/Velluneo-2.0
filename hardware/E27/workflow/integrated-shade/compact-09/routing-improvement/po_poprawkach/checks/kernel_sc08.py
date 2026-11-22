"""Independent, read-only SC08 saved-copper geometry check; KiCad 10.0.6 only.

Not a creepage, insulation, circuit, thermal, or manufacturing qualification.
Conservative outward native polygon approximation; unsupported geometry fails.
"""
from pathlib import Path
from dataclasses import dataclass, field
import argparse, hashlib, itertools, json, math, sys
import pcbnew as k

ERROR_MM = .002
ZONE_BOUNDARY_ENVELOPE_MM = .002
LAYERS = {'F.Cu': k.F_Cu, 'B.Cu': k.B_Cu}
ALL_CU = set(k.LSET.AllCuMask().Seq())
LOCAL = {'SOURCE', 'SENSE_FB', 'BP', 'BP_RELAY', 'BP2_RELAY'}
ROUTE2_INTENT = 'e229ed9dd0a8a593837efcfeaac4fe11b63160d5ceab293653b18370dc764dc8'
ROUTE2_BASIS = 'e60b1955b8020a29cec67bd66634ff6a86455526ef6dba29718c97e58cbe238d'

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()).hexdigest()

def exact_route2_pair(e):
    return all(e.get(key)==value for key,value in {
        'ref':'U1','pins':['2','4'],'nets':['SENSE_FB','DRAIN_BLOCKED'],
        'layers':['F.Cu'],'escape_layers':['F.Cu'],'except_object_types':['pad','track'],
        'escape_margin_mm':1.5,'proposed_drawn_floor_mm':1.9}.items())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def load_native(path):
    # LoadBoard convenience API builds connectivity and propagates connected track
    # nets, concealing deliberately different-net crossings. Raw format loader does
    # not. Never BuildConnectivity/PropagateNets in this independent checker.
    return k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(path))

def raw_track_nets(path):
    """Bounded S-expression reader, used only to verify raw UUID/native-net parity."""
    text=Path(path).read_text(encoding='utf-8')
    if len(text)>50_000_000:raise Unsupported('Saved-board parser size bound exceeded')
    stack=[];root=None;i=0;nodes=0
    while i<len(text):
        if text[i].isspace():i+=1;continue
        if text[i]=='(':
            nodes+=1
            if nodes>2_000_000 or len(stack)>256:raise Unsupported('Saved-board parser complexity bound exceeded')
            value=[]
            if stack:stack[-1].append(value)
            elif root is None:root=value
            else:raise Unsupported('Multiple saved-board roots')
            stack.append(value);i+=1;continue
        if text[i]==')':
            if not stack:raise Unsupported('Unbalanced saved-board closing bracket')
            stack.pop();i+=1;continue
        if not stack:raise Unsupported('Saved-board atom outside root')
        if text[i]=='"':
            start=i;i+=1
            while i<len(text):
                if text[i]=='\\':i+=2;continue
                if text[i]=='"':break
                i+=1
            if i==len(text):raise Unsupported('Unclosed saved-board string')
            value=json.loads(text[start:i+1]);i+=1
        else:
            start=i
            while i<len(text) and not text[i].isspace() and text[i] not in '()':i+=1
            value=text[start:i]
        stack[-1].append(value)
    if stack or not root or root[0]!='kicad_pcb':raise Unsupported('Invalid native board expression')
    result={}
    for node in root[1:]:
        if not isinstance(node,list) or not node or node[0] not in ('segment','via','arc'):continue
        def field(key):
            values=[v for v in node if isinstance(v,list) and v and v[0]==key]
            if len(values)!=1 or len(values[0])!=2:raise Unsupported('Unexpected raw copper '+key)
            return values[0][1]
        uid=field('uuid');net=field('net')
        if uid in result:raise Unsupported('Duplicate raw track UUID')
        result[uid]=net
    return result

def mm(v):
    return k.FromMM(v)

def point(v):
    return [k.ToMM(v.x), k.ToMM(v.y)]

def rectangle(values):
    x0, y0, x1, y1 = map(mm, values)
    p = k.SHAPE_POLY_SET(); p.NewOutline()
    for x, y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]:
        p.Append(x, y)
    return p

def clipped(a, b, inside=True):
    p = k.SHAPE_POLY_SET(a)
    if inside:
        p.BooleanIntersection(b)
    else:
        p.BooleanSubtract(b)
    return p

def valid_zone_outline(poly):
    """Exact integer straight-ring validation; native IsSelfIntersecting can
    report valid disjoint rounded holes as intersecting in pinned KiCad 10.0.6.
    No geometry normalization, inflation or area change is performed here.
    """
    if poly.IsEmpty() or poly.TotalVertices()>2000:return False
    def vertices(line):return [(line.CPoint(i).x,line.CPoint(i).y) for i in range(line.PointCount())]
    def cross(a,b,c):return (b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    def on(a,b,p):return cross(a,b,p)==0 and min(a[0],b[0])<=p[0]<=max(a[0],b[0]) and min(a[1],b[1])<=p[1]<=max(a[1],b[1])
    def intersects(a,b,c,d):
        if max(min(a[0],b[0]),min(c[0],d[0]))>min(max(a[0],b[0]),max(c[0],d[0])) or max(min(a[1],b[1]),min(c[1],d[1]))>min(max(a[1],b[1]),max(c[1],d[1])):return False
        x,y,z,w=cross(a,b,c),cross(a,b,d),cross(c,d,a),cross(c,d,b)
        return (x*y<0 and z*w<0) or on(a,b,c) or on(a,b,d) or on(c,d,a) or on(c,d,b)
    def contains(r,p):
        inside=False
        for a,b in zip(r,r[1:]+r[:1]):
            if on(a,b,p):return False
            if (a[1]>p[1])!=(b[1]>p[1]):
                v=cross(a,b,p)
                if (v>0)==(b[1]>a[1]):inside=not inside
        return inside
    groups=[];rings=[]
    for outer in range(poly.OutlineCount()):
        group=[vertices(poly.COutline(outer))]+[vertices(poly.CHole(outer,h)) for h in range(poly.HoleCount(outer))]
        groups.append(group);rings.extend(group)
    edges=[]
    for index,ring in enumerate(rings):
        if len(ring)<3 or len(set(ring))!=len(ring):return False
        if sum(a[0]*b[1]-b[0]*a[1] for a,b in zip(ring,ring[1:]+ring[:1]))==0:return False
        for i,(a,b) in enumerate(zip(ring,ring[1:]+ring[:1])):edges.append((index,i,len(ring),a,b))
    for e,f in itertools.combinations(edges,2):
        ri,i,n,a,b=e;rj,j,_,c,d=f
        if ri==rj and ((i-j)%n in (1,n-1)):
            # Adjacent edges may share just their declared endpoint, never overlap.
            shared=set((a,b))&set((c,d))
            if len(shared)!=1:return False
            other1=next(p for p in (a,b) if p not in shared);other2=next(p for p in (c,d) if p not in shared)
            if on(a,b,other2) or on(c,d,other1):return False
        elif intersects(a,b,c,d):return False
    for group in groups:
        if any(not contains(group[0],hole[0]) for hole in group[1:]):return False
        if any(contains(a,b[0]) or contains(b,a[0]) for a,b in itertools.combinations(group[1:],2)):return False
    # Separate outer contours must not contain each other (nested islands stop).
    if any(contains(a[0],b[0][0]) or contains(b[0],a[0][0]) for a,b in itertools.combinations(groups,2)):return False
    return True

def zone_boundary_envelope(outline, distance=ZONE_BOUNDARY_ENVELOPE_MM):
    """Comparison-only outward envelope, never substituted for saved copper.
    Reserve 2 nm inside the declared limit for 1 nm native offset approximation.
    """
    region=k.SHAPE_POLY_SET(outline)
    radius=mm(distance)-2
    if radius>0:region.Inflate(radius,k.CORNER_STRATEGY_ROUND_ALL_CORNERS,1)
    return region

def bbox(p):
    q = p.BBox()
    return [q.GetX(), q.GetY(), q.GetRight(), q.GetBottom()]

def close(a, b, distance):
    if a.IsEmpty() or b.IsEmpty():
        return False
    aa, bb = bbox(a), bbox(b); d = mm(distance)
    dx = max(aa[0]-bb[2], bb[0]-aa[2], 0)
    dy = max(aa[1]-bb[3], bb[1]-aa[3], 0)
    if dx*dx+dy*dy > d*d:
        return False
    return bool(a.Collide(b, d))

def actual_gap(a,b, upper):
    lo, hi = 0., upper
    if close(a,b,0):
        return 0.
    for _ in range(22):
        mid=(lo+hi)/2
        if close(a,b,mid): hi=mid
        else: lo=mid
    return round(lo,6)

@dataclass
class Copper:
    id: str
    kind: str
    net: str
    native_net: str
    layer: str
    shape: object
    owner: object = None
    uuid: str = ''
    source: object = None
    meta: dict = field(default_factory=dict)

class Unsupported(Exception):
    pass

class Contract:
    """Explicit input data; only tests use synthetic=True, never CLI customer mode."""
    def __init__(self, project):
        self.project=Path(project); self.synthetic=False; self.input_hashes={}
        def read(name):
            p=self.project/name; self.input_hashes[name]=sha(p)
            return json.loads(p.read_text(encoding='utf-8'))
        binding=read('pcb-basis/intent-native-net-binding.json')
        if sha(self.project/'intended-connectivity.json') != binding['approved_intent']['sha256']:
            raise Unsupported('Approved-intent hash differs from native binding')
        self.input_hashes['pcb-basis/native-binding-export.xml']=sha(self.project/'pcb-basis/native-binding-export.xml')
        if self.input_hashes['pcb-basis/native-binding-export.xml'] != binding['native_export']['sha256']:
            raise Unsupported('Native binding export hash mismatch')
        intent=read('intended-connectivity.json')
        binding_members={r['intent_net']:sorted((p['ref'],p['pin']) for p in r['pins']) for r in binding['records']}
        intent_members={r['id']:sorted((p['ref'],p['pin']) for p in r['pins']) for r in intent['nets']}
        if binding_members!=intent_members or sorted((p['ref'],p['pin']) for p in binding['no_connects'])!=sorted((p['ref'],p['pin']) for p in intent['no_connects']):
            raise Unsupported('Binding pin sets do not equal independent approved intent')
        self.mapping={r['native_net']:r['intent_net'] for r in binding['records']}
        self.expected={(p['ref'],p['pin']):r['native_net'] for r in binding['records'] for p in r['pins']}
        for p in binding['no_connects']:
            self.mapping[p['native_net']]='EXPLICIT_NC'
            self.expected[(p['ref'],p['pin'])]=p['native_net']
        self.refs=set(binding['physical_component_refs']) if 'physical_component_refs' in binding else set(r for r,p in self.expected)
        if len(self.mapping)!=len(binding['records'])+len(binding['no_connects']):
            raise Unsupported('Non-bijective binding')
        hardware=read('hardware.json')
        spatial=read(hardware['product']['spatial_file'])
        spatial_digest=digest({key:value for key,value in spatial.items() if key!='approval'})
        approval=spatial.get('approval') or {}
        if approval.get('intent_digest')!=spatial_digest or not all(isinstance(approval.get(key),str) and approval[key].strip() for key in ('approved_by','evidence')):
            raise Unsupported('Selected spatial intent lacks matching recorded approval')
        bases=[r for r in spatial['basis_sources'] if Path(r['path']).name.startswith('routing-and-isolation-')]
        if len(bases)!=1:raise Unsupported('Selected spatial intent must name exactly one routing basis')
        basis=bases[0]
        rules=read(basis['path'])
        if self.input_hashes[basis['path']]!=basis['sha256']:raise Unsupported('Selected routing basis hash mismatch')
        self.exceptions=rules['package_exceptions_proposed']
        self.route2_authorized=spatial_digest==ROUTE2_INTENT and basis['sha256']==ROUTE2_BASIS
        domains=read('pcb-basis/domain-matrix.json')
        self.domains={n:d['id'] for d in domains['domains'] for n in d['nets']}
        self.domains['EXPLICIT_NC']='CONTROL_RETURN'
        routing_input=read('.electronics-rules/routing-input.json')
        consumer=routing_input['constraints']
        if consumer['intent_digest']!=spatial_digest or digest(consumer)!=routing_input['constraints_digest']:
            raise Unsupported('Routing consumer differs from selected approved spatial intent')
        self.areas=consumer['areas']; self.outline=consumer['outline_mm']; self.minimum=consumer['minimums_mm']
        self.thermal=[68,62,88,82]
        self.class_settings=consumer['net_settings']

    def width(self,native):
        classes={r['name']:r for r in self.class_settings['classes']}
        found=['Default']
        for rule in self.class_settings.get('netclass_patterns',[]):
            if any(x in rule['pattern'] for x in '*?['):raise Unsupported('Wildcard netclass pattern unsupported')
            if rule['pattern']==native:found.append(rule['netclass'])
        return max(self.minimum['track_width'],*(classes[name]['track_width'] for name in found))

    def gap(self,a,b):
        if a==b:return 0.
        if self.domains[a]==self.domains[b]=='CONTROL_RETURN' or a in LOCAL and b in LOCAL:return .3
        if self.domains[a] in ('AC_FRONT','BUS_DRAIN','SWITCH_FLOAT') or self.domains[b] in ('AC_FRONT','BUS_DRAIN','SWITCH_FLOAT'):return 4.
        return 2.

class Checker:
    def __init__(self, board, contract, provenance=None):
        self.board=board; self.c=contract; self.objects=[]; self.findings=[]; self.courts={}
        self.provenance=provenance; self.prov={}; self.owner_cache={}; self.used=set()
        self.inner_shapes={};self.ambiguities=[]
        self.stats={'per_face_objects':{}, 'different_net_face_pairs':0, 'clipped_piece_pairs':0}

    def fail(self, finding_type, **detail):
        self.findings.append(dict(type=finding_type,**detail))

    def native_poly(self,item,layer,inside=False):
        p=k.SHAPE_POLY_SET()
        item.TransformShapeToPolygon(p,LAYERS[layer],0,mm(ERROR_MM),k.ERROR_INSIDE if inside else k.ERROR_OUTSIDE)
        if p.IsEmpty():raise Unsupported('Empty copper polygon: '+str(item))
        return p

    def object(self,item,kind,net,layer,owner=None,ident=None):
        if net not in self.c.mapping:raise Unsupported('Unbound native net: '+net)
        if layer not in LAYERS:raise Unsupported('Unsupported copper layer '+layer)
        uid=str(item.m_Uuid.AsString())
        return Copper(ident or uid,kind,self.c.mapping[net],net,layer,self.native_poly(item,layer),owner,uid,item)

    def collect(self):
        # Validate every scope, even unused concessions, before inspecting copper.
        for e in self.c.exceptions:self.validate_exception(e)
        if self.board.GetCopperLayerCount()!=2:raise Unsupported('Only exactly two copper layers supported')
        for graphic in self.board.GetDrawings():
            if graphic.GetLayer() in ALL_CU:raise Unsupported('Free copper graphics/text unsupported')
        actual={}; refs=[]
        for f in self.board.GetFootprints():
            ref=f.GetReference(); refs.append(ref)
            for graphic in list(f.GraphicalItems())+[f.Reference(),f.Value()]:
                if graphic.GetLayer() in ALL_CU:raise Unsupported('Footprint copper graphics/text unsupported '+ref)
            if any(e["ref"]==ref for e in self.c.exceptions):
                graphics=[g for g in f.GraphicalItems() if g.GetLayer()==k.F_CrtYd]
                if not graphics:raise Unsupported('Missing F courtyard '+ref)
                # Reconstruct the exact closed courtyard, including U1/Q2 notches.
                # A bounding box would improperly enlarge those local concessions.
                edges=[]
                for g in graphics:
                    if len(graphics)==1 and g.GetShape()==k.SHAPE_T_RECT:
                        a,b=g.GetStart(),g.GetEnd()
                        edges=[((a.x,a.y),(b.x,a.y)),((b.x,a.y),(b.x,b.y)),((b.x,b.y),(a.x,b.y)),((a.x,b.y),(a.x,a.y))]
                        break
                    if g.GetShape()!=k.SHAPE_T_SEGMENT:raise Unsupported('Non-segment courtyard '+ref)
                    a,b=g.GetStart(),g.GetEnd()
                    edges.append(((a.x,a.y),(b.x,b.y)))
                pts=set(p for edge in edges for p in edge)
                if len(edges)!=len(pts) or any(sum(p in edge for edge in edges)!=2 for p in pts):
                    raise Unsupported('Non-closed/branched courtyard '+ref)
                remaining=list(edges);first=remaining.pop();vertices=[first[0],first[1]]
                while remaining:
                    match=next((edge for edge in remaining if vertices[-1] in edge),None)
                    if match is None:raise Unsupported('Disconnected courtyard '+ref)
                    remaining.remove(match);vertices.append(match[1] if match[0]==vertices[-1] else match[0])
                if vertices[-1]!=vertices[0]:raise Unsupported('Open courtyard '+ref)
                court=k.SHAPE_POLY_SET();court.NewOutline()
                for x,y in vertices[:-1]:court.Append(x,y)
                if court.IsSelfIntersecting():raise Unsupported('Self-intersecting courtyard '+ref)
                self.courts[ref]=court
            for p in f.Pads():
                faces=[name for name,layer in LAYERS.items() if p.IsOnLayer(layer)]
                if not faces:
                    if set(p.GetLayerSet().Seq())&ALL_CU:raise Unsupported('Pad on inactive copper layer '+ref+'.'+p.GetNumber())
                    if p.GetAttribute()!=k.PAD_ATTRIB_SMD or p.GetDrillSize().x or p.GetDrillSize().y:raise Unsupported('Non-copper drilled pad unsupported '+ref+'.'+p.GetNumber())
                    self.stats['noncopper_undrilled_paste_pads_excluded']=self.stats.get('noncopper_undrilled_paste_pads_excluded',0)+1
                    continue
                if p.GetAttribute()==k.PAD_ATTRIB_NPTH:raise Unsupported('NPTH unsupported')
                key=(ref,p.GetNumber())
                if not key[1] or key in actual:raise Unsupported('Unnumbered/duplicate pad '+str(key))
                actual[key]=p.GetNetname()
                if p.GetAttribute()==k.PAD_ATTRIB_PTH:
                    drill=p.GetDrillSize();size=p.GetSize()
                    if min(drill.x,drill.y)<mm(self.c.minimum['hole_size']):self.fail('pad_drill',pad=list(key))
                    if min(size.x-drill.x,size.y-drill.y)/2<mm(self.c.minimum['annular_width']):self.fail('pad_annulus',pad=list(key))
                for face in faces:self.objects.append(self.object(p,'pad',p.GetNetname(),face,key,ref+'.'+key[1]))
        if len(refs)!=len(set(refs)) or set(refs)!=self.c.refs:raise Unsupported('Missing/extra/duplicate physical references')
        if actual!=self.c.expected:raise Unsupported('Exact native pad/net binding mismatch')
        tracks=list(self.board.GetTracks())
        if self.provenance:
            for rec in self.provenance.get('native_track_provenance',[]):
                if rec['uuid'] in self.prov:raise Unsupported('Duplicate provenance UUID')
                self.prov[rec['uuid']]=rec
        track_ids=set()
        for item in tracks:
            if isinstance(item,k.PCB_VIA):
                if item.GetViaType()!=k.VIATYPE_THROUGH or not item.HasValidLayerPair(2):raise Unsupported('Only valid through vias supported')
                diameter=min(k.ToMM(item.GetWidth(ly)) for ly in LAYERS.values());drill=k.ToMM(item.GetDrillValue())
                if drill<self.c.minimum['hole_size'] or (diameter-drill)/2<self.c.minimum['annular_width']:
                    self.fail('via_drill_or_annulus',uuid=str(item.m_Uuid.AsString()))
                for face in LAYERS:
                    if not item.IsOnLayer(LAYERS[face]):raise Unsupported('Through-via layer set mismatch')
                    self.objects.append(self.object(item,'via',item.GetNetname(),face))
                continue
            if isinstance(item,k.PCB_ARC) or item.GetClass()!='PCB_TRACK':raise Unsupported('Only straight PCB_TRACK segments supported')
            layer=k.LayerName(item.GetLayer())
            obj=self.object(item,'track',item.GetNetname(),layer)
            obj.meta={'a':point(item.GetStart()),'b':point(item.GetEnd()),'width':k.ToMM(item.GetWidth())}
            required_width=self.c.width(obj.native_net)
            if obj.meta['width']<required_width:self.fail('track_width',id=obj.id,actual=obj.meta['width'],target_mm=required_width)
            if obj.net=='EXPLICIT_NC':self.fail('routed_explicit_nc',id=obj.id)
            track_ids.add(obj.uuid)
            if obj.uuid in self.prov:
                rec=self.prov[obj.uuid]
                expected={'uuid':obj.uuid,'net':obj.native_net,'layer':obj.layer,**obj.meta}
                if any(rec.get(key)!=value for key,value in expected.items()):raise Unsupported('Track provenance geometry mismatch '+obj.uuid)
                owner=rec.get('owner')
                if owner is not None:
                    owner=tuple(owner)
                    if self.c.expected.get(owner)!=obj.native_net:raise Unsupported('Provenance owner pin/net mismatch '+obj.uuid)
                obj.owner=owner
            self.objects.append(obj)
        if self.provenance and set(self.prov)!=track_ids:raise Unsupported('Provenance missing/extra tracks')
        for zone in self.board.Zones():
            if zone.GetIsRuleArea():continue
            if not zone.IsFilled() or zone.NeedRefill():raise Unsupported('Copper zone unfilled or marked stale')
            if (set(zone.GetLayerSet().Seq())&ALL_CU)-set(LAYERS.values()):raise Unsupported('Zone on inactive copper layer')
            faces=[name for name,layer in LAYERS.items() if zone.IsOnLayer(layer)]
            if not faces:raise Unsupported('Unsupported zone layer')
            for face in faces:
                if not zone.HasFilledPolysForLayer(LAYERS[face]):raise Unsupported('Missing saved zone fill '+face)
                native=zone.GetNetname()
                if native not in self.c.mapping:raise Unsupported('Unbound zone net')
                poly=k.SHAPE_POLY_SET(zone.GetFilledPolysList(LAYERS[face]))
                if poly.IsEmpty():raise Unsupported('Empty saved zone fill')
                outline=k.SHAPE_POLY_SET(zone.Outline())
                if not valid_zone_outline(outline):raise Unsupported('Invalid actual zone outline')
                residual=clipped(poly,outline,False)
                if not clipped(poly,zone_boundary_envelope(outline),False).IsEmpty():
                    raise Unsupported('Saved zone fill outside actual zone outline')
                if not residual.IsEmpty():
                    lo,hi=0.,ZONE_BOUNDARY_ENVELOPE_MM
                    for _ in range(12):
                        mid=(lo+hi)/2
                        if clipped(poly,zone_boundary_envelope(outline,mid),False).IsEmpty():hi=mid
                        else:lo=mid
                    self.stats.setdefault('zone_boundary_numeric_residuals',[]).append({
                        'zone':str(zone.m_Uuid.AsString()),'layer':face,
                        'residual_area_mm2':residual.Area()/1e12,
                        'conservative_offset_upper_bound_mm':hi,
                        'comparison_envelope_mm':ZONE_BOUNDARY_ENVELOPE_MM})
                self.objects.append(Copper(str(zone.m_Uuid.AsString()),'zone',self.c.mapping[native],native,face,poly,source=zone))
        if len(self.objects)>2000 or sum(o.shape.TotalVertices() for o in self.objects)>100000:
            raise Unsupported('Geometry complexity exceeds bounded checker (2000 face objects/100000 vertices)')
        self.check_outline()

    def check_outline(self):
        x0,y0,x1,y1=map(mm,self.c.outline)
        expected={frozenset(((x0,y0),(x1,y0))),frozenset(((x1,y0),(x1,y1))),frozenset(((x1,y1),(x0,y1))),frozenset(((x0,y1),(x0,y0)))}
        actual=[]
        for edge in self.board.GetDrawings():
            if edge.GetLayer()!=k.Edge_Cuts:continue
            if edge.GetShape()!=k.SHAPE_T_SEGMENT:raise Unsupported('Only exact rectangular outline supported')
            a,b=edge.GetStart(),edge.GetEnd();actual.append(frozenset(((a.x,a.y),(b.x,b.y))))
        if len(actual)!=4 or set(actual)!=expected:raise Unsupported('Native outline does not match rectangular contract')

    def validate_exception(self,e):
        margin=e['escape_margin_mm']
        extended=getattr(self.c,'route2_authorized',False) and exact_route2_pair(e)
        if margin<0 or (margin>1 and not extended) or set(e['except_object_types'])!={'pad','track'}:raise Unsupported('Unsupported exception scope')

    def exception_region(self,e):
        self.validate_exception(e)
        margin=e['escape_margin_mm']
        region=k.SHAPE_POLY_SET(self.courts[e['ref']])
        if margin:
            # Offset approximation never earns extra exception space: reserve twice
            # max approximation error radially inside the authorized maximum.
            if margin<=2*ERROR_MM:raise Unsupported('Exception margin too small for bounded offset')
            region.Inflate(mm(margin-2*ERROR_MM),k.CORNER_STRATEGY_ROUND_ALL_CORNERS,mm(ERROR_MM))
        return region

    def roots(self,obj,index,region):
        key=(obj.id,obj.layer,index)
        if key in self.owner_cache:return self.owner_cache[key]
        e=self.c.exceptions[index]
        # Graph comprises only same-layer same-net pad/track geometry CLIPPED to the
        # finite escape region. Vias/zones cannot extend or establish ownership.
        candidates=[x for x in self.objects if x.layer==obj.layer and x.net==obj.net and x.kind in ('pad','track')]
        pieces={}
        for x in candidates:
            # Outward approximations are correct for spacing failures, but must not
            # invent a connection across a tiny real gap. Ownership uses inward
            # polygons, conservatively proving a local copper path instead.
            if id(x) not in self.inner_shapes:self.inner_shapes[id(x)]=self.native_poly(x.source,x.layer,True)
            pieces[id(x)]=clipped(self.inner_shapes[id(x)],region)
        live=[x for x in candidates if not pieces[id(x)].IsEmpty()]
        reached={id(obj)}; pending=[obj]
        while pending:
            node=pending.pop()
            for other in live:
                if id(other) not in reached and close(pieces[id(node)],pieces[id(other)],0):
                    reached.add(id(other));pending.append(other)
        roots={x.owner for x in live if id(x) in reached and x.kind=='pad' and x.owner[0]==e['ref']}
        self.owner_cache[key]=roots
        return roots

    def eligible(self,obj,index,side,region):
        e=self.c.exceptions[index]; root=(e['ref'],e['pins'][side])
        if obj.kind not in e['except_object_types'] or obj.layer not in e['layers'] or obj.net!=e['nets'][side]:return False
        if obj.kind=='pad':return obj.owner==root
        if obj.layer not in e['escape_layers']:return False
        if clipped(obj.shape,region).IsEmpty():return False
        roots=self.roots(obj,index,region)
        if obj.owner is not None:return obj.owner==root and root in roots
        if len(roots)>1:
            detail={'track':obj.id,'layer':obj.layer,'exception_id':index,'local_pad_roots':[list(p) for p in sorted(roots)]}
            if detail not in self.ambiguities:self.ambiguities.append(detail)
        # Unique proven local pad root only. Same net membership/proximity alone is
        # insufficient, and multiple roots do not select the more lenient floor.
        return roots=={root}

    def spacing(self,a,b):
        target=self.c.gap(a.net,b.net)
        if not target or not close(a.shape,b.shape,target):return
        eligible=[]
        for i,e in enumerate(self.c.exceptions):
            if set(e['nets'])!={a.net,b.net} or a.layer not in e['layers']:continue
            region=self.exception_region(e)
            side=0 if a.net==e['nets'][0] else 1
            if self.eligible(a,i,side,region) and self.eligible(b,i,1-side,region):eligible.append((i,region,e['proposed_drawn_floor_mm']))
        pieces_a=[(a.shape,frozenset())];pieces_b=[(b.shape,frozenset())]
        for i,region,floor in eligible:
            def split(pieces):
                out=[]
                for poly,scopes in pieces:
                    inside=clipped(poly,region);outside=clipped(poly,region,False)
                    if not inside.IsEmpty():out.append((inside,scopes|{i}))
                    if not outside.IsEmpty():out.append((outside,scopes))
                return out
            pieces_a=split(pieces_a);pieces_b=split(pieces_b)
        floors={i:floor for i,region,floor in eligible}
        for pa,sa in pieces_a:
            for pb,sb in pieces_b:
                self.stats['clipped_piece_pairs']+=1
                common=sa&sb; required=min([target]+[floors[i] for i in common])
                if close(pa,pb,required):
                    self.fail('copper_spacing',a=a.id,b=b.id,kinds=[a.kind,b.kind],layer=a.layer,nets=[a.net,b.net],target_mm=required,conservative_gap_mm=actual_gap(pa,pb,required),exception_ids=sorted(common),generic_target_mm=target,ownership_ambiguities=[r for r in self.ambiguities if r['track'] in (a.id,b.id)])
                    return
        self.used.update(i for i,region,floor in eligible)

    def run(self):
        self.collect()
        edge=self.c.minimum['edge_clearance']; x0,y0,x1,y1=self.c.outline
        safe=rectangle([x0+edge,y0+edge,x1-edge,y1-edge])
        for obj in self.objects:
            self.stats['per_face_objects'][obj.kind]=self.stats['per_face_objects'].get(obj.kind,0)+1
            if obj.net=='EXPLICIT_NC' and obj.kind!='pad':self.fail('routed_explicit_nc',id=obj.id,kind=obj.kind)
            if not clipped(obj.shape,safe,False).IsEmpty():self.fail('copper_edge_setback',id=obj.id,layer=obj.layer,target_mm=edge)
            for area in self.c.areas:
                rect=area.get('rectangle_mm',area.get('rectangle'))
                if obj.layer in area['layers'] and obj.kind in area['disallow'] and close(obj.shape,rectangle(rect),0):self.fail('protected_area',id=obj.id,layer=obj.layer,area=area['id'])
            if obj.layer=='B.Cu' and obj.net!='DC_RETURN' and close(obj.shape,rectangle(self.c.thermal),self.c.gap(obj.net,'DC_RETURN')):
                self.fail('U3_backside_reservation',id=obj.id,kind=obj.kind,net=obj.net,target_mm=self.c.gap(obj.net,'DC_RETURN'))
        for a,b in itertools.combinations(self.objects,2):
            if a.layer!=b.layer or a.net==b.net:continue
            self.stats['different_net_face_pairs']+=1;self.spacing(a,b)
        return {'passed':not self.findings,'findings':self.findings,'stats':self.stats,'finite_exception_ids_used':sorted(self.used)}

def check_saved(board_path,contract,provenance_path=None):
    board_path=Path(board_path);before=sha(board_path)
    version=k.GetBuildVersion()
    report={'tool':'independent saved-copper geometry validator','version':version,'board_sha256':before,'checker_sha256':sha(__file__),'synthetic_contract':contract.synthetic,'contract_input_hashes':contract.input_hashes,'polygon_outward_error_mm':ERROR_MM,'saved_fill_boundary_comparison_envelope_mm':ZONE_BOUNDARY_ENVELOPE_MM,'limits':['Flat-board geometric target only; not physical creepage/clearance qualification or standards compliance','No electrical, transient, thermal-performance or manufacturing qualification','Saved zone fill must lie within the declared 0.002 mm comparison envelope of a valid actual outline and not be marked stale; actual copper spacing is unchanged; historical freshness still requires independent native refill evidence','Only straight tracks, two copper layers, rectangular outline and closed straight-segment/rect native courtyards supported; anything else stops','Conservative native outward polygon approximation and bounded courtyard offset can produce false failures near boundaries; no inward copper tolerance relaxation']}
    try:
        if version!='10.0.6':raise Unsupported('Pinned KiCad 10.0.6 required')
        provenance=json.loads(Path(provenance_path).read_text(encoding='utf-8')) if provenance_path else None
        if provenance and provenance.get('output_sha256')!=before:raise Unsupported('Provenance saved-board hash mismatch')
        board=load_native(board_path)
        raw=raw_track_nets(board_path)
        loaded={str(t.m_Uuid.AsString()):t.GetNetname() for t in board.GetTracks()}
        if raw!=loaded:raise Unsupported('Raw saved track/via net identity differs after native load')
        report['raw_native_track_net_parity']=True
        checker=Checker(board,contract,provenance)
        report.update(checker.run())
    except Exception as error:
        report.update(passed=False,stopped=True,error=type(error).__name__+': '+str(error))
    report['board_sha256_after']=sha(board_path)
    report['input_unchanged']=before==report['board_sha256_after']
    if not report['input_unchanged']:report['passed']=False
    return report

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--project',required=True);parser.add_argument('--board',required=True);parser.add_argument('--report',required=True);parser.add_argument('--provenance')
    args=parser.parse_args()
    try:report=check_saved(args.board,Contract(args.project),args.provenance)
    except Exception as error:report={'passed':False,'stopped':True,'error':type(error).__name__+': '+str(error)}
    Path(args.report).write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:report.get(key) for key in ['passed','stopped','error','stats','board_sha256','input_unchanged']}))
    return 0 if report['passed'] else 1

if __name__=='__main__':sys.exit(main())

"""Conservative two-layer routing candidate generator for the SC08 laboratory board.

Not an insulation, thermal, EMC or manufacturing qualification tool. Customer writes
require current spatial attestation, matching consumer digests and a separate actual
routing authorization receipt. No customer board is touched by fixture tests.
"""
from __future__ import annotations
import argparse, collections, fnmatch, hashlib, heapq, itertools, json, math, time
from dataclasses import dataclass, field
from pathlib import Path

F, B = 0, 1
LAYER_NAMES = ('F.Cu', 'B.Cu')
LOCAL_FLOAT = {'SOURCE','SENSE_FB','BP','BP_RELAY','BP2_RELAY'}

def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()).hexdigest()

def file_sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def save(path, value): Path(path).write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8')

class NetBinding:
    """Exact pin-set bijection. Never infer an anonymous native net from its label."""
    def __init__(self,doc):
        self.native_to_intent={};self.net_pins={};self.nc_pins={};self.all_pins={}
        for record in doc['records']:
            native=record['native_net'];intent=record['intent_net']
            pins={(p['ref'],str(p['pin'])) for p in record['pins']}
            if not native or not intent or not pins or native in self.native_to_intent or intent in self.native_to_intent.values():raise ValueError('Invalid/nonbijective native net binding')
            self.native_to_intent[native]=intent;self.net_pins[native]=pins
            for p in pins:
                if p in self.all_pins:raise ValueError('Pin duplicated in net binding')
                self.all_pins[p]=native
        for p in doc.get('no_connects',[]):
            owner=(p['ref'],str(p['pin']));native=p['native_net']
            if owner in self.all_pins or native in self.native_to_intent or native in self.nc_pins:raise ValueError('Invalid NC binding')
            self.nc_pins[native]={owner};self.all_pins[owner]=native

    def name(self,native):
        if native in self.native_to_intent:return self.native_to_intent[native]
        if native in self.nc_pins:return '__NC_CONTROL'
        raise ValueError('Unknown native net; no exact pin-set binding: '+native)

    def validate_pads(self,pads):
        actual=collections.defaultdict(set);seen=set()
        for p in pads:
            if p.owner in seen:raise ValueError('Duplicated numbered board pad: '+str(p.owner))
            seen.add(p.owner);actual[p.net].add(p.owner)
        expected={**self.net_pins,**self.nc_pins}
        if dict(actual)!=expected:raise ValueError('PCB physical pin/net membership differs from frozen binding')

    def validate_intent(self,intent):
        expected={n['id']:{(p['ref'],str(p['pin'])) for p in n['pins']} for n in intent['nets']}
        actual={self.native_to_intent[n]:pins for n,pins in self.net_pins.items()}
        if actual!=expected:raise ValueError('Binding does not match current independent intended graph')
        if {(p['ref'],str(p['pin'])) for p in intent['no_connects']}!={p for ps in self.nc_pins.values() for p in ps}:raise ValueError('Binding NC differs from intended NC')

def inside(p, rect, margin=0):
    return rect[0]-margin <= p[0] <= rect[2]+margin and rect[1]-margin <= p[1] <= rect[3]+margin

def point_rect_distance(p, rect):
    return math.hypot(max(rect[0]-p[0], 0, p[0]-rect[2]), max(rect[1]-p[1],0,p[1]-rect[3]))

def point_segment_distance(p, a, b):
    dx,dy=b[0]-a[0],b[1]-a[1]
    den=dx*dx+dy*dy
    t=max(0.,min(1.,((p[0]-a[0])*dx+(p[1]-a[1])*dy)/den)) if den else 0.
    return math.hypot(p[0]-a[0]-t*dx,p[1]-a[1]-t*dy)

def segment_hits_rect(a,b,rect):
    """Closed Liang-Barsky rectangle intersection, including tangent contact."""
    t0,t1=0.,1.;dx,dy=b[0]-a[0],b[1]-a[1]
    for p,q in [(-dx,a[0]-rect[0]),(dx,rect[2]-a[0]),(-dy,a[1]-rect[1]),(dy,rect[3]-a[1])]:
        if abs(p)<1e-15:
            if q<0:return False
        else:
            t=q/p
            if p<0:t0=max(t0,t)
            else:t1=min(t1,t)
            if t0>t1:return False
    return True

def subsegments(a,b,rect):
    """Split at exception-box boundary so no lower gap leaks outside its box."""
    ts=[0.,1.];dx,dy=b[0]-a[0],b[1]-a[1]
    for axis,delta in [(0,dx),(1,dy)]:
        if abs(delta)>1e-12:
            for v in [rect[axis],rect[axis+2]]:
                t=(v-a[axis])/delta
                if 0<t<1:ts.append(t)
    ts=sorted(set(ts))
    for t,u in zip(ts,ts[1:]):
        p=(a[0]+dx*t,a[1]+dy*t);q=(a[0]+dx*u,a[1]+dy*u)
        yield p,q,inside(((p[0]+q[0])/2,(p[1]+q[1])/2),rect)

def segment_rect_distance(a,b,rect):
    """Exact Euclidean distance to closed AABB; zero for contact/intersection.

    For disjoint segment/rectangle the closest pair includes either a segment
    endpoint or a rectangle vertex. This retains conservative native pad AABBs
    without adding the square corners of an L-infinity clearance inflation.
    """
    if segment_hits_rect(a,b,rect):return 0.
    x0,y0,x1,y1=rect
    return min(point_rect_distance(a,rect),point_rect_distance(b,rect),
               *(point_segment_distance(c,a,b) for c in
                 [(x0,y0),(x0,y1),(x1,y0),(x1,y1)]))

@dataclass(frozen=True)
class Pad:
    ref:str; pin:str; net:str; x:float; y:float
    box:tuple; layers:tuple
    @property
    def owner(self):return (self.ref,self.pin)

@dataclass
class Copper:
    net:str; layer:int; a:tuple; b:tuple; width:float
    owner:tuple|None=None
    kind:str='track'
    uuid:str|None=None

class Rules:
    def __init__(self, domain_doc, routing_doc, spatial_payload, courtyards, binding, boundaries_doc=None):
        self.domains={n:d['id'] for d in domain_doc['domains'] for n in d['nets']}
        self.binding=binding
        if set(self.domains)!=set(binding.native_to_intent.values()):raise ValueError('Domain inventory and exact binding differ')
        self.routing=routing_doc;self.payload=spatial_payload;self.courtyards=courtyards
        self.minima=spatial_payload.get('minimums_mm',{})
        settings=spatial_payload.get('net_settings',{});classes={c['name']:c for c in settings.get('classes',[])}
        self.native_class={}
        for native in list(binding.native_to_intent)+list(binding.nc_pins):
            assigned=[p['netclass'] for p in settings.get('netclass_patterns',[]) if fnmatch.fnmatchcase(native,p['pattern'])]
            if len(set(assigned))>1:raise ValueError('Ambiguous native class pattern membership')
            self.native_class[native]=classes.get(assigned[0] if assigned else 'Default',{})
        self.outline=tuple(spatial_payload['outline_mm']);self.areas=spatial_payload['areas']
        self.reservations=[]
        u3=(boundaries_doc or {}).get('U3_target',{})
        if u3.get('reserved_backside_region_mm'):
            self.reservations.append({'layer':B,'rect':tuple(u3['reserved_backside_region_mm']),'allowed':set(u3['reserved_backside_allowed_intent_nets'])})
        for area in self.areas:
            if set(area.get('layers',LAYER_NAMES))!=set(LAYER_NAMES) or area.get('exceptions'):raise ValueError('This adapter currently requires two-layer, no-net-exception protected areas')
        self.exceptions=[]
        for e in routing_doc.get('package_exceptions_proposed',[]):
            # A missing machine-readable layer list is a stop, not inferred approval.
            if not e.get('layers') or 'escape_layers' not in e:
                raise ValueError('Exception needs explicit layers/escape_layers: '+str(e.get('ref')))
            if any(v not in LAYER_NAMES for v in e['layers']+e['escape_layers']):raise ValueError('Unsupported exception layer')
            limit=1.5 if e.get('ref')=='U1' and set(map(str,e.get('pins',[])))=={'2','4'} else 1.
            if 'escape_margin_mm' not in e or not 0<=e['escape_margin_mm']<=limit:raise ValueError('Finite escape_margin_mm exceeds exact package/pin bound')
            if not e.get('except_object_types') or not set(e['except_object_types'])<={'pad','track'}:raise ValueError('Exception may authorize pads/tracks only')
            if e['ref'] not in courtyards:raise ValueError('Exception ref has no courtyard: '+e['ref'])
            self.exceptions.append(e)

    def domain(self,net):
        n=self.binding.name(net)
        if n=='__NC_CONTROL':return 'CONTROL_RETURN'
        if n not in self.domains:raise ValueError('Unknown native net for domain lookup: '+net)
        return self.domains[n]

    def gap(self,a,b):
        if a==b:return 0.
        na,nb=self.binding.name(a),self.binding.name(b);da,db=self.domain(a),self.domain(b)
        if da==db=='CONTROL_RETURN' or (na in LOCAL_FLOAT and nb in LOCAL_FLOAT):target=.30
        elif da in ('AC_FRONT','BUS_DRAIN','SWITCH_FLOAT') or db in ('AC_FRONT','BUS_DRAIN','SWITCH_FLOAT'):target=4.
        elif da=='OUTPUT_AUX' or db=='OUTPUT_AUX':target=2.
        else:raise ValueError('Unclassified pair '+a+' / '+b)
        return max(target,self.native_gap(a,b))

    def native_gap(self,a,b):
        return max(float(self.minima.get('clearance',0)),float(self.native_class[a].get('clearance',0)),float(self.native_class[b].get('clearance',0)))

    def width(self,net):
        n=self.binding.name(net)
        target=.6 if self.domain(net) in ('AC_FRONT','BUS_DRAIN','OUTPUT_AUX') or n in ('SOURCE','SENSE_FB','L2_MID') else .3
        return max(target,float(self.minima.get('track_width',0)),float(self.native_class[net].get('track_width',0)))

    def hard_width(self,net):
        # Netclass track_width is a routing default, not a native hard constraint.
        return max(float(self.minima.get('track_width',0)),.6 if self.binding.name(net)=='AC_BUS' else 0.)

    def exception(self,owner,other_owner,layer,escape=True):
        if not owner or not other_owner or owner[0]!=other_owner[0]:return None
        for e in self.exceptions:
            if e['ref']==owner[0] and set(e['pins'])=={owner[1],other_owner[1]}:
                if LAYER_NAMES[layer] not in e['escape_layers' if escape else 'layers']:return None
                if not set(['track','pad'] if escape else ['pad'])<=set(e['except_object_types']):return None
                c=self.courtyards[owner[0]]
                m=float(e['escape_margin_mm']) if escape else 0.
                return float(e['proposed_drawn_floor_mm']),(c[0]-m,c[1]-m,c[2]+m,c[3]+m)
        return None

    def boundary_ok(self,p,radius,kind='track'):
        x0,y0,x1,y1=self.outline
        if not (x0+radius<=p[0]<=x1-radius and y0+radius<=p[1]<=y1-radius):return False
        for area in self.areas:
            if kind in area['disallow'] and point_rect_distance(p,area['rectangle_mm'])<=radius+1e-8:return False
        return True

    def pad_box_ok(self,pad):
        """Every numbered copper pad, including NC, must fit as a full box."""
        a,b,c,d=pad.box;x0,y0,x1,y1=self.outline
        if not (x0<=a<=c<=x1 and y0<=b<=d<=y1):return False
        for area in self.areas:
            if 'pad' not in area['disallow']:continue
            if not any(LAYER_NAMES[layer] in area.get('layers',LAYER_NAMES) for layer in pad.layers):continue
            x0,y0,x1,y1=area['rectangle_mm']
            # Closed intersection includes copper just touching a forbidden region.
            if not (c<x0 or a>x1 or d<y0 or b>y1):return False
        return True

    def boundary_segment_ok(self,a,b,radius,kind='track'):
        if not self.boundary_ok(a,radius,kind) or not self.boundary_ok(b,radius,kind):return False
        for area in self.areas:
            if kind in area['disallow']:
                x0,y0,x1,y1=area['rectangle_mm']
                if segment_hits_rect(a,b,(x0-radius,y0-radius,x1+radius,y1+radius)):return False
        return True

    def reservation_gap(self,net,reservation):
        if self.binding.name(net) in reservation['allowed']:return None
        allowed_native=[n for n,intent in self.binding.native_to_intent.items() if intent in reservation['allowed']]
        if not allowed_native:raise ValueError('Reserved thermal copper has no explicit allowed native net')
        return max(self.gap(net,n) for n in allowed_native)

    def reservation_segment_ok(self,a,b,net,radius,layer,via=False):
        for r in self.reservations:
            if not via and layer!=r['layer']:continue
            gap=self.reservation_gap(net,r)
            if gap is None:continue
            x0,y0,x1,y1=r['rect'];d=gap+radius
            if segment_hits_rect(a,b,(x0-d,y0-d,x1+d,y1+d)):return False
        return True

class Router:
    def __init__(self,pads,rules,copper=(),grid=.25,via_diameter=None,via_drill=None):
        self.pads=list(pads);self.rules=rules;self.copper=list(copper);self.grid=grid
        rules.binding.validate_pads(self.pads)
        for pad in self.pads:
            if not rules.pad_box_ok(pad):raise ValueError('Numbered copper pad violates board bounds or pad-prohibited region: '+str(pad.owner))
        for c in self.copper:
            rules.binding.name(c.net)
            kind='via' if c.kind=='via' else 'track'
            if not rules.boundary_segment_ok(c.a,c.b,c.width/2,kind):raise ValueError('Existing copper violates accepted protected geometry')
            if not rules.reservation_segment_ok(c.a,c.b,c.net,c.width/2,c.layer,via=kind=='via'):raise ValueError('Existing foreign copper violates reserved thermal-copper space')
            if kind=='track' and c.width+1e-8<rules.hard_width(c.net):raise ValueError('Existing track is below native hard width')
        owners={p.owner:p for p in self.pads}
        for pad in self.pads:
            for r in rules.reservations:
                if r['layer'] not in pad.layers:continue
                gap=rules.reservation_gap(pad.net,r)
                if gap is not None:
                    a,b,c,d=pad.box;x0,y0,x1,y1=r['rect']
                    if not (c<x0-gap or a>x1+gap or d<y0-gap or b>y1+gap):raise ValueError('Placed foreign pad violates reserved thermal-copper space: '+str(pad.owner))
        for e in rules.exceptions:
            selected=[owners[(e['ref'],str(pin))] for pin in e['pins']]
            actual={rules.binding.name(p.net) for p in selected}
            if actual!=set(e['nets']):raise ValueError('Exception net membership differs from exact ref/pins')
            if e['proposed_drawn_floor_mm']+1e-8<rules.native_gap(selected[0].net,selected[1].net):raise ValueError('Package exception would violate a native DRC floor')
        self.via_drill=max(.3,float(rules.minima.get('hole_size',0))) if via_drill is None else via_drill
        self.via_diameter=max(.8,self.via_drill+2*float(rules.minima.get('annular_width',0))+.1) if via_diameter is None else via_diameter
        if self.via_drill<float(rules.minima.get('hole_size',0))-1e-8 or (self.via_diameter-self.via_drill)/2<float(rules.minima.get('annular_width',0))-1e-8:raise ValueError('Via geometry violates resolved drill/annular floor')
        self.vias=[];self.stubs={}
        x0,y0,x1,y1=rules.outline;self.origin=(x0,y0)
        self.nx=int(round((x1-x0)/grid))+1;self.ny=int(round((y1-y0)/grid))+1
        self.port_failures=[];self.unrouted=[];self.events=[];self.component_goals={};self.reused_pads=set()

    def existing_components(self):
        """Union only actual same-net centerline contacts; never label equality.

        Deliberately under-approximates pad contact using the pad center, avoiding
        invented connectivity through conservative rounded-pad bounding boxes.
        Via exports have one coincident centerline item on each copper layer.
        """
        items=list(self.copper);parent=list(range(len(items)+len(self.pads)))
        def root(i):
            while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
            return i
        def join(i,j):parent[root(i)]=root(j)
        def touch(a,b):
            if a.net!=b.net:return False
            if a.layer!=b.layer:return a.kind==b.kind=='via' and a.a==b.a and (a.uuid==b.uuid or a.uuid is None and b.uuid is None)
            # Intersecting centerlines imply real copper contact even at crossings.
            ax,ay=a.a;bx,by=a.b;cx,cy=b.a;dx,dy=b.b
            cross=lambda x,y,u,v:x*v-y*u
            den=cross(bx-ax,by-ay,dx-cx,dy-cy)
            if abs(den)>1e-12:
                t=cross(cx-ax,cy-ay,dx-cx,dy-cy)/den;u=cross(cx-ax,cy-ay,bx-ax,by-ay)/den
                if 0<=t<=1 and 0<=u<=1:return True
            return min(point_segment_distance(a.a,b.a,b.b),point_segment_distance(a.b,b.a,b.b),point_segment_distance(b.a,a.a,a.b),point_segment_distance(b.b,a.a,a.b))<1e-7
        for i,a in enumerate(items):
            for j in range(i):
                if touch(a,items[j]):join(i,j)
            for j,p in enumerate(self.pads):
                if p.net==a.net and a.layer in p.layers and point_segment_distance((p.x,p.y),a.a,a.b)<1e-7:join(i,len(items)+j)
        groups=collections.defaultdict(lambda:{'copper':[],'pads':[]})
        for i,c in enumerate(items):groups[root(i)]['copper'].append(c)
        for i,p in enumerate(self.pads):groups[root(len(items)+i)]['pads'].append(p)
        return list(groups.values())

    def reuse_existing(self):
        for component in self.existing_components():
            if not component['copper'] or not component['pads']:continue
            net=component['pads'][0].net;width=self.rules.width(net);goals=set()
            if self.rules.reservations and self.rules.binding.name(net)=='DC_RETURN':continue
            for c in component['copper']:
                steps=max(1,math.ceil(math.dist(c.a,c.b)/self.grid))
                for k in range(steps+1):
                    t=k/steps;q=(c.a[0]+t*(c.b[0]-c.a[0]),c.a[1]+t*(c.b[1]-c.a[1]));node=self.node(q,c.layer);p=self.point(node)
                    if node in goals or not self.anchor_safe(p,net,width,c.layer):continue
                    if math.dist(p,q)>1e-7:
                        if not self.segment_ok(q,p,net,width,c.layer,c.owner):continue
                        self.copper.append(Copper(net,c.layer,q,p,width,c.owner))
                    goals.add(node)
            if not goals:continue
            port=min(goals)
            for pad in component['pads']:
                self.stubs[pad.owner]=(port,component['copper'][0]);self.component_goals[pad.owner]=goals;self.reused_pads.add(pad.owner)

    def point(self,node):return (self.origin[0]+node[0]*self.grid,self.origin[1]+node[1]*self.grid)
    def node(self,p,layer=F):return (round((p[0]-self.origin[0])/self.grid),round((p[1]-self.origin[1])/self.grid),layer)

    def pad_blocked(self,a,b,net,width,layer,owner=None):
        for pad in self.pads:
            if layer not in pad.layers or pad.net==net:continue
            gap=self.rules.gap(net,pad.net);exception=self.rules.exception(owner,pad.owner,layer)
            segments=[(a,b,False)] if not exception else list(subsegments(a,b,exception[1]))
            for p,q,in_box in segments:
                dist=(exception[0] if in_box else gap)+width/2+1e-7
                if segment_rect_distance(p,q,pad.box)<=dist:return True
        return False

    def segment_ok(self,a,b,net,width,layer,owner=None):
        if not self.rules.boundary_segment_ok(a,b,width/2):return False
        if not self.rules.reservation_segment_ok(a,b,net,width/2,layer):return False
        if self.pad_blocked(a,b,net,width,layer,owner):return False
        for c in self.copper:
            if c.net==net or c.layer!=layer:continue
            gap=self.rules.gap(net,c.net);ex=self.rules.exception(owner,c.owner,layer) if c.kind=='track' else None
            pieces=[(a,b,False)] if not ex else list(subsegments(a,b,ex[1]))
            other_pieces=[(c.a,c.b,False)] if not ex else list(subsegments(c.a,c.b,ex[1]))
            # Conservative sampled distance with half-step guard; no local exception for vias.
            for p,q,in_box in pieces:
                step=.05;n=max(1,math.ceil(math.dist(p,q)/step))
                for oa,ob,other_in in other_pieces:
                    limit=(ex[0] if in_box and other_in else gap)+(width+c.width)/2+step/2
                    for k in range(n+1):
                        t=k/n;v=(p[0]+(q[0]-p[0])*t,p[1]+(q[1]-p[1])*t)
                        if point_segment_distance(v,oa,ob)<limit-1e-8:return False
        return True

    def anchor_safe(self,p,net,width,layer):
        if not self.rules.boundary_ok(p,width/2+self.grid*.71):return False
        if not self.rules.reservation_segment_ok(p,p,net,width/2+self.grid*.71,layer):return False
        for pad in self.pads:
            if layer in pad.layers and pad.net!=net:
                if point_rect_distance(p,pad.box)<self.rules.gap(net,pad.net)+width/2+self.grid*.71:return False
        for c in self.copper:
            if c.net!=net and c.layer==layer and point_segment_distance(p,c.a,c.b)<self.rules.gap(net,c.net)+(width+c.width)/2+self.grid*.71:return False
        return True

    def make_port(self,pad):
        width=self.rules.width(pad.net);a=(pad.x,pad.y);c=self.rules.courtyards[pad.ref]
        candidates=set()
        # Different rays let high-voltage pins fan apart within their exact finite box.
        for distance in [1.,2.,3.,4.,5.,6.,8.]:
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
                v=(a[0]+dx*distance,a[1]+dy*distance)
                n=self.node(v);candidates.add((n[0],n[1]))
        choices=[]
        for x,y in candidates:
            p=self.point((x,y,F))
            if inside(p,c,.99):continue
            for layer in pad.layers:
                if self.anchor_safe(p,pad.net,width,layer) and self.segment_ok(a,p,pad.net,width,layer,pad.owner):
                    choices.append((math.dist(a,p)+(.05 if layer==B else 0),p,layer))
        if not choices:
            # Joining an already generated same-net stub is an electrical path,
            # not an assumption that equal-net package pins are internally tied.
            joins=[]
            for existing_port,existing_stub in self.stubs.values():
                layer=existing_stub.layer;target=existing_stub.a
                if existing_stub.net!=pad.net or layer not in pad.layers or a==target:continue
                if self.anchor_safe(self.point(existing_port),pad.net,width,layer) and self.segment_ok(a,target,pad.net,width,layer,pad.owner):
                    joins.append((math.dist(a,target),existing_port,target,layer))
            if joins:
                _,port,target,layer=min(joins)
                copper=Copper(pad.net,layer,a,target,width,pad.owner)
                self.copper.append(copper);self.stubs[pad.owner]=(port,copper)
                return port
        if not choices:
            # Large THT courtyards can exceed the historical eight-mm rays.
            # Add only finite boundary-derived fallback anchors; all unchanged
            # global/local clearance and protection checks still apply.
            fallback=set()
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1),
                          (2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]:
                exits=[]
                if dx:exits.append(((c[2]+.99+self.grid-a[0]) if dx>0 else (a[0]-c[0]+.99+self.grid))/abs(dx))
                if dy:exits.append(((c[3]+.99+self.grid-a[1]) if dy>0 else (a[1]-c[1]+.99+self.grid))/abs(dy))
                distance=max(self.grid,min(exits))
                for extra in [0.,1.,2.,4.]:
                    n=self.node((a[0]+dx*(distance+extra),a[1]+dy*(distance+extra)))
                    fallback.add((n[0],n[1]))
            for x,y in fallback-candidates:
                p=self.point((x,y,F))
                if inside(p,c,.99):continue
                for layer in pad.layers:
                    if self.anchor_safe(p,pad.net,width,layer) and self.segment_ok(a,p,pad.net,width,layer,pad.owner):
                        choices.append((math.dist(a,p)+(.05 if layer==B else 0),p,layer))
        if not choices:return None
        _,p,layer=min(choices)
        copper=Copper(pad.net,layer,a,p,width,pad.owner)
        self.copper.append(copper);port=self.node(p,layer);self.stubs[pad.owner]=(port,copper)
        return port

    def prepare_ports(self):
        self.reuse_existing()
        # Critical component escapes first; remaining pads sorted deterministically.
        critical={(e['ref'],pin) for e in self.rules.exceptions for pin in e['pins']}
        pads=sorted(self.pads,key=lambda p:(p.owner not in critical,-self.rules.width(p.net),p.ref,p.pin))
        for pad in pads:
            if pad.net in self.rules.binding.nc_pins:continue
            if self.rules.reservations and self.rules.binding.name(pad.net)=='DC_RETURN':
                if not any(e.get('net')==pad.net for e in self.unrouted):self.unrouted.append({'net':pad.net,'reason':'DC_RETURN topology deferred: root must preserve quiet U3 branch and main power return explicitly','routed':False})
                continue
            if pad.owner in self.reused_pads:continue
            if self.make_port(pad) is None:self.port_failures.append({'ref':pad.ref,'pin':pad.pin,'net':pad.net,'reason':'No conservative finite package escape found; manual review/placement change required'})
        return self.port_failures

    def blocked_masks(self,net,width):
        n=self.nx*self.ny;masks=[bytearray(n),bytearray(n)];vm=bytearray(n)
        guard=self.grid*math.sqrt(2)/2+1e-6
        def index(x,y):return y*self.nx+x
        for y in range(self.ny):
            for x in range(self.nx):
                p=self.point((x,y,F));i=index(x,y)
                if not self.rules.boundary_ok(p,width/2+guard):masks[0][i]=masks[1][i]=1
                if not self.rules.boundary_ok(p,self.via_diameter/2+guard,'via'):vm[i]=1
                for layer in [F,B]:
                    if not self.rules.reservation_segment_ok(p,p,net,width/2+guard,layer):masks[layer][i]=1
                if not self.rules.reservation_segment_ok(p,p,net,self.via_diameter/2+guard,F,via=True):vm[i]=1
        def rect_cells(rect):
            a,b,c,d=rect
            return range(max(0,math.floor((a-self.origin[0])/self.grid)),min(self.nx-1,math.ceil((c-self.origin[0])/self.grid))+1),range(max(0,math.floor((b-self.origin[1])/self.grid)),min(self.ny-1,math.ceil((d-self.origin[1])/self.grid))+1)
        for pad in self.pads:
            if pad.net==net:continue
            gap=self.rules.gap(net,pad.net);r=max(width/2,self.via_diameter/2)+gap+guard
            a,b,c,d=pad.box;xs,ys=rect_cells((a-r,b-r,c+r,d+r))
            for y in ys:
                for x in xs:
                    p=self.point((x,y,F));dist=point_rect_distance(p,pad.box);i=index(x,y)
                    if dist<gap+width/2+guard:
                        for layer in pad.layers:masks[layer][i]=1
                    if dist<gap+self.via_diameter/2+guard:vm[i]=1
        for c in self.copper:
            if c.net==net:continue
            gap=self.rules.gap(net,c.net);r=gap+(max(width,self.via_diameter)+c.width)/2+guard
            xs,ys=rect_cells((min(c.a[0],c.b[0])-r,min(c.a[1],c.b[1])-r,max(c.a[0],c.b[0])+r,max(c.a[1],c.b[1])+r))
            for y in ys:
                for x in xs:
                    p=self.point((x,y,F));dist=point_segment_distance(p,c.a,c.b);i=index(x,y)
                    if dist<gap+(width+c.width)/2+guard:masks[c.layer][i]=1
                    if dist<gap+(self.via_diameter+c.width)/2+guard:vm[i]=1
        return masks,vm

    def astar(self,start,goals,masks,vm,max_nodes=500000):
        goals=set(goals);coords=[self.point(n) for n in goals]
        goalbox=(min(p[0] for p in coords),min(p[1] for p in coords),max(p[0] for p in coords),max(p[1] for p in coords))
        def h(n):
            return point_rect_distance(self.point(n),goalbox)
        def good(n):return 0<=n[0]<self.nx and 0<=n[1]<self.ny and not masks[n[2]][n[1]*self.nx+n[0]]
        if not good(start):return None,{'reason':'Port anchor blocked by earlier copper','expanded':0}
        if not any(good(g) for g in goals):return None,{'reason':'All target tree nodes blocked','expanded':0}
        queue=[(h(start),0.,start)];cost={start:0.};parent={};count=0
        while queue and count<max_nodes:
            _,g,n=heapq.heappop(queue)
            if g!=cost.get(n):continue
            count+=1
            if n in goals:
                path=[n]
                while n in parent:n=parent[n];path.append(n)
                return path[::-1],{'expanded':count}
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]:
                q=(n[0]+dx,n[1]+dy,n[2])
                if not good(q):continue
                d=self.grid*math.hypot(dx,dy)
                new=g+d
                if new<cost.get(q,math.inf):cost[q]=new;parent[q]=n;heapq.heappush(queue,(new+h(q),new,q))
            i=n[1]*self.nx+n[0];q=(n[0],n[1],1-n[2])
            if not vm[i] and good(q):
                new=g+4.
                if new<cost.get(q,math.inf):cost[q]=new;parent[q]=n;heapq.heappush(queue,(new+h(q),new,q))
        return None,{'reason':'Search exhausted' if not queue else 'Node budget exhausted','expanded':count}

    def commit_path(self,net,path):
        width=self.rules.width(net);new=[];run_start=None;run_end=None;direction=None
        def flush():
            nonlocal run_start,run_end,direction
            if run_start is not None and run_start!=run_end:new.append(Copper(net,run_start[2],self.point(run_start),self.point(run_end),width))
            run_start=run_end=direction=None
        for a,b in zip(path,path[1:]):
            p,q=self.point(a),self.point(b)
            if a[2]!=b[2]:
                flush()
                if p!=q:raise AssertionError('Layer transition moved position')
                self.vias.append({'net':net,'point':p,'diameter':self.via_diameter,'drill':self.via_drill})
                for layer in [F,B]:new.append(Copper(net,layer,p,p,self.via_diameter,kind='via'))
            else:
                d=(b[0]-a[0],b[1]-a[1],a[2])
                if d!=direction:flush();run_start=a;direction=d
                run_end=b
        flush()
        self.copper.extend(new)

    def route(self,max_nodes=500000,checkpoint=None):
        self.prepare_ports()
        groups=collections.defaultdict(list)
        for p in self.pads:
            if p.owner in self.stubs:groups[p.net].append(p)
        def span(net):
            ps=groups[net];return max(p.x for p in ps)-min(p.x for p in ps)+max(p.y for p in ps)-min(p.y for p in ps)
        for net in sorted(groups,key=lambda n:(-self.rules.width(n),-span(n),n)):
            pads=groups[net]
            if len(pads)<2:continue
            if self.rules.reservations and self.rules.binding.name(net)=='DC_RETURN':
                self.unrouted.append({'net':net,'reason':'DC_RETURN topology deferred: root must preserve quiet U3 branch and main power return explicitly','routed':False})
                continue
            pads.sort(key=lambda p:(p.x,p.y,p.ref,p.pin));first=pads.pop(0);tree=set(self.component_goals.get(first.owner,{self.stubs[first.owner][0]}))
            while pads:
                pad=min(pads,key=lambda p:min(math.dist((p.x,p.y),self.point(t)) for t in tree));pads.remove(pad)
                goals=self.component_goals.get(pad.owner,{self.stubs[pad.owner][0]})
                if tree.intersection(goals):tree.update(goals);continue
                start=self.stubs[pad.owner][0];t0=time.monotonic();masks,vm=self.blocked_masks(net,self.rules.width(net));path,stat=self.astar(start,tree,masks,vm,max_nodes)
                event={'net':net,'terminal':[pad.ref,pad.pin],'seconds':time.monotonic()-t0,**stat,'routed':path is not None};self.events.append(event)
                print(json.dumps({'routing_progress':event}),flush=True)
                if path:
                    self.commit_path(net,path);tree.update(path);tree.update(goals)
                else:self.unrouted.append(event)
                if checkpoint:checkpoint(self.report())
        return self.report()

    def report(self):
        return {'kind':'Conservative routing candidate; native DRC/parity and independent final copper checks still required','grid_mm':self.grid,'pad_count':len(self.pads),'via_geometry_mm':{'diameter':self.via_diameter,'drill':self.via_drill,'annulus':(self.via_diameter-self.via_drill)/2},'port_failures':self.port_failures,'unrouted_branches':self.unrouted,'via_count':len(self.vias),'events':self.events,'tracks':[{'net':c.net,'layer':LAYER_NAMES[c.layer],'a':list(c.a),'b':list(c.b),'width':c.width,'owner':list(c.owner) if c.owner else None,'kind':c.kind} for c in self.copper],'vias':self.vias,'claims_complete':False,'limitations':['Routing uses conservative pad AABBs, not exact rounded/custom shapes; this can fail feasible escapes.','No zones, arcs, arbitrary-layer stacks, blind/buried vias, manufacturing fillet or true creepage model.','No native DRC/thermal/EMC/insulation qualification inferred from pathfinding.','No automatic rule relaxation or DRC exclusions. Unrouted and failed escapes require root review.']}

def validate_customer(project,board_path,receipt_path):
    project=Path(project).resolve();h=json.loads((project/'hardware.json').read_text(encoding='utf-8-sig'))
    if h.get('kicad_version')!='10.0.6':raise ValueError('Requires pinned KiCad10.0.6')
    si=h.get('product',{}).get('spatial_file')
    if not si:raise ValueError('No active spatial contract')
    sp=json.loads((project/si).read_text(encoding='utf-8-sig'));dg=digest({k:v for k,v in sp.items() if k!='approval'});approval=sp.get('approval') or {}
    if not approval.get('approved_by') or not approval.get('evidence') or approval.get('intent_digest')!=dg:raise ValueError('Spatial contract has no current actual human approval')
    data=json.loads((project/'.electronics-rules/routing-input.json').read_text(encoding='utf-8-sig'))
    if data.get('constraints_digest')!=digest(data.get('constraints')) or data['constraints'].get('intent_digest')!=dg:raise ValueError('Routing consumer digest mismatch')
    other=json.loads((project/'.electronics-rules/placement-input.json').read_text(encoding='utf-8-sig'))
    if data!=other:raise ValueError('Placement/routing consumers diverged')
    for b in sp.get('basis_sources',[]):
        p=(project/b['path']).resolve()
        if not p.is_relative_to(project) or file_sha(p)!=b['sha256']:raise ValueError('Spatial basis mismatch')
    receipt=json.loads(Path(receipt_path).read_text(encoding='utf-8-sig'))
    required={'scope':'routing_experimental_lab_board','source_board_sha256':file_sha(board_path),'spatial_intent_digest':dg,'constraints_digest':data['constraints_digest']}
    if not all(receipt.get(k)==v for k,v in required.items()) or not receipt.get('approved_by') or not receipt.get('evidence'):raise ValueError('Actual placement/routing authorization receipt missing or stale')
    return data,sp,receipt

def native_track_record(item,owner=None):
    import pcbnew
    return {'uuid':item.m_Uuid.AsString(),'net':item.GetNetname(),'layer':'F.Cu' if item.GetLayer()==pcbnew.F_Cu else 'B.Cu',
            'a':[pcbnew.ToMM(item.GetStart().x),pcbnew.ToMM(item.GetStart().y)],'b':[pcbnew.ToMM(item.GetEnd().x),pcbnew.ToMM(item.GetEnd().y)],
            'width':pcbnew.ToMM(item.GetWidth()),'owner':list(owner) if owner else None}

def native_via_record(item):
    import pcbnew
    return {'uuid':item.m_Uuid.AsString(),'net':item.GetNetname(),'point':[pcbnew.ToMM(item.GetPosition().x),pcbnew.ToMM(item.GetPosition().y)],
            'diameter':pcbnew.ToMM(item.GetWidth(pcbnew.F_Cu)),'drill':pcbnew.ToMM(item.GetDrillValue())}

def validate_previous_provenance(board_path,board,previous):
    import pcbnew
    if previous.get('output_sha256')!=file_sha(board_path):raise ValueError('Previous provenance is not bound to actual input board SHA')
    records=previous.get('native_track_provenance',[]);vias=previous.get('native_via_provenance',[])
    tracks={i.m_Uuid.AsString():native_track_record(i) for i in board.GetTracks() if type(i)==pcbnew.PCB_TRACK}
    expected={r['uuid']:{**r,'owner':None} for r in records}
    if len(expected)!=len(records) or expected!=tracks:raise ValueError('Previous track provenance UUID/net/layer/geometry/width mismatch')
    actual_vias={i.m_Uuid.AsString():native_via_record(i) for i in board.GetTracks() if type(i)==pcbnew.PCB_VIA}
    expected_vias={r['uuid']:r for r in vias}
    if len(expected_vias)!=len(vias) or actual_vias!=expected_vias:raise ValueError('Previous via provenance UUID/net/geometry mismatch')
    owners={(fp.GetReference(),p.GetNumber()):p.GetNetname() for fp in board.GetFootprints() for p in fp.Pads() if p.GetNumber()}
    for r in records:
        owner=r.get('owner')
        if owner is not None and (not isinstance(owner,list) or len(owner)!=2 or owners.get(tuple(owner))!=r['net']):raise ValueError('Previous explicit owner not an actual same-net board pad')
    return {r['uuid']:tuple(r['owner']) if r['owner'] else None for r in records}

def export_pcb(board_path,spatial_payload=None,previous_provenance=None):
    import pcbnew
    if pcbnew.GetBuildVersion()!='10.0.6':raise ValueError('pcbnew must be10.0.6')
    board=pcbnew.LoadBoard(str(board_path))
    owner_by_uuid=validate_previous_provenance(board_path,board,previous_provenance) if previous_provenance is not None else {}
    if board.GetCopperLayerCount()!=2:raise ValueError('Two copper layers only')
    expected_areas={'HW-SPATIAL-'+a['id']:a for a in (spatial_payload or {}).get('areas',[])};seen=set()
    for zone in board.Zones():
        name=zone.GetZoneName()
        if not zone.GetIsRuleArea() or name not in expected_areas or name in seen:raise ValueError('Copper zones/unrecognized or duplicate rule areas unsupported')
        seen.add(name);area=expected_areas[name];poly=zone.Outline()
        if poly.OutlineCount()!=1 or poly.HoleCount(0)!=0:raise ValueError('Nonrectangular managed rule area')
        line=poly.Outline(0);points={(round(pcbnew.ToMM(line.CPoint(i).x),6),round(pcbnew.ToMM(line.CPoint(i).y),6)) for i in range(line.PointCount())}
        a,b,c,d=area['rectangle_mm'];wanted={(a,b),(c,b),(c,d),(a,d)}
        if points!=wanted or line.PointCount()!=4:raise ValueError('Rule area differs from accepted consumer')
        layers={LAYER_NAMES[n] for native,n in [(pcbnew.F_Cu,F),(pcbnew.B_Cu,B)] if zone.GetLayerSet().Contains(native)}
        if layers!=set(area['layers']):raise ValueError('Rule area copper-layer scope differs')
    if set(expected_areas)!=seen:raise ValueError('Accepted managed rule areas absent on saved board')
    pads=[];courts={};native_layers={pcbnew.F_Cu:F,pcbnew.B_Cu:B}
    for fp in board.GetFootprints():
        ref=fp.GetReference();coords=[]
        for g in fp.GraphicalItems():
            if g.GetLayer() not in [pcbnew.F_CrtYd,pcbnew.B_CrtYd]:continue
            if g.GetShape()==pcbnew.SHAPE_T_CIRCLE:
                c=g.GetCenter();r=g.GetRadius();coords.extend([(pcbnew.ToMM(c.x-r),pcbnew.ToMM(c.y-r)),(pcbnew.ToMM(c.x+r),pcbnew.ToMM(c.y+r))])
            elif g.GetShape() in [pcbnew.SHAPE_T_SEGMENT,pcbnew.SHAPE_T_RECT]:
                for p in [g.GetStart(),g.GetEnd()]:coords.append((pcbnew.ToMM(p.x),pcbnew.ToMM(p.y)))
            else:raise ValueError('Unsupported courtyard primitive on '+ref)
        if not coords:raise ValueError('No native courtyard on '+ref)
        courts[ref]=(min(x for x,y in coords),min(y for x,y in coords),max(x for x,y in coords),max(y for x,y in coords))
        for p in fp.Pads():
            layers=tuple(i for native,i in native_layers.items() if p.GetLayerSet().Contains(native))
            if not layers:continue
            if p.GetAttribute()==pcbnew.PAD_ATTRIB_NPTH:raise ValueError('NPTH/hole routing requires separate qualified geometry support')
            if not p.GetNumber():raise ValueError('Unnumbered copper pad cannot be silently ignored: '+ref)
            bb=p.GetBoundingBox();pos=p.GetPosition();net=p.GetNetname()
            if not net:raise ValueError('Numbered copper pad has no net: '+ref+'.'+p.GetNumber())
            pads.append(Pad(ref,p.GetNumber(),net,pcbnew.ToMM(pos.x),pcbnew.ToMM(pos.y),(pcbnew.ToMM(bb.GetLeft()),pcbnew.ToMM(bb.GetTop()),pcbnew.ToMM(bb.GetRight()),pcbnew.ToMM(bb.GetBottom())),layers))
    copper=[]
    for t in board.GetTracks():
        if isinstance(t,pcbnew.PCB_VIA):
            minima=(spatial_payload or {}).get('minimums_mm',{})
            drill=pcbnew.ToMM(t.GetDrillValue());diameter=pcbnew.ToMM(t.GetWidth(pcbnew.F_Cu))
            if drill+1e-8<float(minima.get('hole_size',0)) or (diameter-drill)/2+1e-8<float(minima.get('annular_width',0)):raise ValueError('Existing via violates resolved drill/annular floor')
            p=t.GetPosition();a=(pcbnew.ToMM(p.x),pcbnew.ToMM(p.y))
            for layer in [F,B]:copper.append(Copper(t.GetNetname(),layer,a,a,diameter,kind='via',uuid=t.m_Uuid.AsString()))
        elif isinstance(t,pcbnew.PCB_ARC):raise ValueError('Existing copper arc unsupported')
        else:
            a,b=t.GetStart(),t.GetEnd();copper.append(Copper(t.GetNetname(),native_layers[t.GetLayer()],(pcbnew.ToMM(a.x),pcbnew.ToMM(a.y)),(pcbnew.ToMM(b.x),pcbnew.ToMM(b.y)),pcbnew.ToMM(t.GetWidth()),owner_by_uuid.get(t.m_Uuid.AsString()),uuid=t.m_Uuid.AsString()))
    board._routing_previous_owners=owner_by_uuid
    return board,pads,courts,copper

def write_candidate(board,report,output_path):
    """Root-controlled final invocation only; caller validates actual authorization."""
    import pcbnew
    # Report includes existing copper. Caller passes fresh initial-track count separately.
    nets=board.GetNetsByName();layers={'F.Cu':pcbnew.F_Cu,'B.Cu':pcbnew.B_Cu}
    def native_record(item,owner=None):
        return {'uuid':item.m_Uuid.AsString(),'net':item.GetNetname(),
                'layer':LAYER_NAMES[0 if item.GetLayer()==pcbnew.F_Cu else 1],
                'a':[pcbnew.ToMM(item.GetStart().x),pcbnew.ToMM(item.GetStart().y)],
                'b':[pcbnew.ToMM(item.GetEnd().x),pcbnew.ToMM(item.GetEnd().y)],
                'width':pcbnew.ToMM(item.GetWidth()),'owner':list(owner) if owner else None}
    provenance=[native_record(item,getattr(board,'_routing_previous_owners',{}).get(item.m_Uuid.AsString())) for item in board.GetTracks()
                if type(item)==pcbnew.PCB_TRACK]
    def native_via_record(item):
        return {'uuid':item.m_Uuid.AsString(),'net':item.GetNetname(),
                'point':[pcbnew.ToMM(item.GetPosition().x),pcbnew.ToMM(item.GetPosition().y)],
                'diameter':pcbnew.ToMM(item.GetWidth(pcbnew.F_Cu)),'drill':pcbnew.ToMM(item.GetDrillValue())}
    planned_vias={item.m_Uuid.AsString():native_via_record(item) for item in board.GetTracks()
                  if type(item)==pcbnew.PCB_VIA}
    start=report.get('initial_copper_count',0)
    for t in report['tracks'][start:]:
        if t['kind']!='track':continue
        item=pcbnew.PCB_TRACK(board);item.SetStart(pcbnew.VECTOR2I(*(pcbnew.FromMM(v) for v in t['a'])));item.SetEnd(pcbnew.VECTOR2I(*(pcbnew.FromMM(v) for v in t['b'])));item.SetWidth(pcbnew.FromMM(t['width']));item.SetLayer(layers[t['layer']]);item.SetNetCode(nets[t['net']].GetNetCode());board.Add(item)
        provenance.append(native_record(item,t.get('owner')))
    for v in report['vias']:
        item=pcbnew.PCB_VIA(board);item.SetPosition(pcbnew.VECTOR2I(*(pcbnew.FromMM(a) for a in v['point'])));item.SetWidth(pcbnew.FromMM(v['diameter']));item.SetDrill(pcbnew.FromMM(v['drill']));item.SetViaType(pcbnew.VIATYPE_THROUGH);item.SetLayerPair(pcbnew.F_Cu,pcbnew.B_Cu);item.SetNetCode(nets[v['net']].GetNetCode());board.Add(item)
        planned_vias[item.m_Uuid.AsString()]=native_via_record(item)
    # The caller supplies/reviews the matching project and custom rules separately.
    # SaveBoard's default also saves settings and can replace that .kicad_pro with
    # default rules when this native board has no loaded project association.
    board.BuildConnectivity()
    planned={r['uuid']:r for r in provenance}
    def check_tracks(native_board,stage):
        actual={item.m_Uuid.AsString():native_record(item) for item in native_board.GetTracks()
                if type(item)==pcbnew.PCB_TRACK}
        expected={u:{**r,'owner':None} for u,r in planned.items()}
        if actual!=expected:raise RuntimeError('Native track geometry/net changed from authored plan '+stage)
        actual_vias={item.m_Uuid.AsString():native_via_record(item) for item in native_board.GetTracks()
                     if type(item)==pcbnew.PCB_VIA}
        if actual_vias!=planned_vias:raise RuntimeError('Native via geometry/net changed from authored plan '+stage)
    check_tracks(board,'after BuildConnectivity')
    pcbnew.SaveBoard(str(output_path),board,True)
    # Convenience LoadBoard may propagate a shorted copper net. Raw load must
    # preserve the actual saved identities for a meaningful write parity check.
    raw=pcbnew.PCB_IO_MGR.Load(pcbnew.PCB_IO_MGR.KICAD_SEXP,str(output_path))
    check_tracks(raw,'in raw saved board')
    report['output_sha256']=file_sha(output_path)
    report['native_track_provenance']=provenance
    report['native_via_provenance']=list(planned_vias.values())

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--project',required=True);ap.add_argument('--board',required=True);ap.add_argument('--authorization-receipt',required=True);ap.add_argument('--report',required=True);ap.add_argument('--output-board');ap.add_argument('--previous-provenance');ap.add_argument('--write-output',action='store_true');ap.add_argument('--grid',type=float,default=.25);ap.add_argument('--max-nodes',type=int,default=500000);args=ap.parse_args()
    project=Path(args.project).resolve();board_path=Path(args.board).resolve();before=file_sha(board_path)
    report_path=Path(args.report).resolve()
    if report_path.suffix!='.json' or not (report_path.is_relative_to(project/'.work') or report_path.is_relative_to(Path(__file__).resolve().parent)):raise ValueError('Report must stay in project .work or adapter work folder, never a design source')
    if args.grid<=0 or args.grid>.25:raise ValueError('Qualified candidate grid range is 0<grid<=.25mm')
    consumers,sp,receipt=validate_customer(project,board_path,args.authorization_receipt)
    previous=json.loads(Path(args.previous_provenance).read_text(encoding='utf-8-sig')) if args.previous_provenance else None
    board,pads,courts,copper=export_pcb(board_path,consumers['constraints'],previous)
    bases=[b for b in sp.get('basis_sources',[]) if Path(b['path']).name.startswith('routing-and-isolation') and b['path'].endswith('.json')]
    if len(bases)!=1:raise ValueError('Active spatial contract must bind exactly one routing-and-isolation basis')
    dm=json.loads((project/'pcb-basis/domain-matrix.json').read_text(encoding='utf-8-sig'));rd=json.loads((project/bases[0]['path']).read_text(encoding='utf-8-sig'))
    binding_path=project/'pcb-basis/intent-native-net-binding.json';binding_doc=json.loads(binding_path.read_text(encoding='utf-8-sig'));binding=NetBinding(binding_doc)
    board_refs=[fp.GetReference() for fp in board.GetFootprints()]
    if len(board_refs)!=len(set(board_refs)) or set(board_refs)!=set(binding_doc['component_refs']):raise ValueError('Board component inventory differs from frozen binding')
    for key in ['approved_intent','native_schematic','native_export']:
        source=binding_doc[key];p=(project/source['path']).resolve()
        if not p.is_relative_to(project) or file_sha(p)!=source['sha256']:raise ValueError('Binding source changed: '+key)
    hardware=json.loads((project/'hardware.json').read_text(encoding='utf-8-sig'));intent=json.loads((project/hardware['product']['connectivity_file']).read_text(encoding='utf-8-sig'));binding.validate_intent(intent)
    intent_digest=hashlib.sha256(json.dumps({k:v for k,v in intent.items() if k!='approval'},sort_keys=True,ensure_ascii=False,separators=(',',':'),allow_nan=False).encode()).hexdigest()
    if (intent.get('approval') or {}).get('intent_digest')!=intent_digest or binding_doc['approved_intent']['intent_digest']!=intent_digest:raise ValueError('Independent intent approval/binding stale')
    boundaries=json.loads((project/'pcb-basis/lab-board-boundaries.json').read_text(encoding='utf-8-sig'))
    rules=Rules(dm,rd,consumers['constraints'],courts,binding,boundaries);router=Router(pads,rules,copper,args.grid)
    def checkpoint(report):
        report.update(source_board_sha256=before,constraints_digest=consumers['constraints_digest'],spatial_intent_digest=consumers['constraints']['intent_digest'],net_binding_sha256=file_sha(binding_path),initial_copper_count=len(copper),customer_board_written=False);save(args.report,report)
    report=router.route(args.max_nodes,checkpoint);checkpoint(report)
    if file_sha(board_path)!=before:raise RuntimeError('Input board changed during read-only routing search')
    if args.write_output:
        if not args.output_board:raise ValueError('--output-board required for root-authorized write')
        out=Path(args.output_board).resolve()
        if out==board_path:raise ValueError('Use a distinct candidate output; never overwrite original source')
        if not out.is_relative_to(project):raise ValueError('Customer candidate output must stay inside actual project')
        write_candidate(board,report,out);report['customer_board_written']=str(out);report['output_sha256']=file_sha(out);save(args.report,report)
    print(json.dumps({'report':args.report,'port_failures':len(report['port_failures']),'unrouted_branches':len(report['unrouted_branches']),'via_count':report['via_count'],'native_DRC_not_run':True}))
    if report['port_failures'] or report['unrouted_branches']:raise SystemExit(2)

if __name__=='__main__':main()

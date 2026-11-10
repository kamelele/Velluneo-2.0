from power import *
import heapq
import numpy as np

STEP = .10
NX, NY = [round(v/STEP)+1 for v in SIZE]
LAYERS = [p.F_Cu,p.B_Cu]
VIA_D=.58
VIA_DRILL=.30
DXDY=[(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,1.414),(1,-1,1.414),(-1,1,1.414),(-1,-1,1.414)]
WIDE={'P_0','P_D','P_BULK','P_BR','P_L','P_LF','P_LR','P_N','S_RAW','S_GND','S_RTN','S_SW','S_FUSED','S_LED_PLUS','S_LED_KA','S_LED_KB'}
HV={'P_BULK','P_BR','P_D','P_CL'}
MAINS={'P_L','P_LF','P_LR','P_N'}
MAINS_WIDTH=.29
MAINS_ACROSS=False
EARLY=[]
FRONT_ESCAPE={}
RESERVED_LAYER=None
DEFAULT_CLEARANCE=.19
SIGNAL_WIDTH=.21

def sep(a,b):
    if a==b: return 0
    if MAINS_ACROSS and a in MAINS and b in MAINS: return 1.5
    if (a=='P_N' and b.startswith('P_L')) or (b=='P_N' and a.startswith('P_L')): return 1.5
    if (a in HV and b=='P_0') or (b in HV and a=='P_0'): return 1.1
    return DEFAULT_CLEARANCE

def rel(v):
    return v.x/1e6-ORIGIN[0], v.y/1e6-ORIGIN[1]
def abspt(x,y):
    return (x+ORIGIN[0],y+ORIGIN[1])
def grid_coord(x,y):
    return round(x/STEP),round(y/STEP)

def window(x0,y0,x1,y1,margin):
    ax=max(0,math.floor((x0-margin)/STEP)); bx=min(NX,math.ceil((x1+margin)/STEP)+1)
    ay=max(0,math.floor((y0-margin)/STEP)); by=min(NY,math.ceil((y1+margin)/STEP)+1)
    return slice(ax,bx),slice(ay,by), np.ogrid[ax:bx,ay:by]

def stamp_rect(field, limits, extra):
    x0,y0,x1,y1=limits
    xs,ys,(a,b)=window(x0,y0,x1,y1,extra)
    xx,yy=a*STEP,b*STEP
    dx=np.maximum(np.maximum(x0-xx,xx-x1),0)
    dy=np.maximum(np.maximum(y0-yy,yy-y1),0)
    field[xs,ys] |= dx*dx+dy*dy <= extra*extra

def stamp_segment(field,a,b,r):
    x1,y1=a; x2,y2=b
    xs,ys,(x,y)=window(min(x1,x2),min(y1,y2),max(x1,x2),max(y1,y2),r)
    x=x*STEP-x1; y=y*STEP-y1
    dx=x2-x1; dy=y2-y1
    h=dx*dx+dy*dy
    t=np.clip((x*dx+y*dy)/h,0,1) if h else 0
    field[xs,ys] |= (x-t*dx)**2+(y-t*dy)**2 <= r*r

def via(b,net,x,y):
    v=p.PCB_VIA(b)
    v.SetViaType(p.VIATYPE_THROUGH)
    v.SetLayerPair(p.F_Cu,p.B_Cu)
    v.SetPosition(pt(*abspt(x,y)))
    v.SetDrill(p.FromMM(VIA_DRILL))
    v.SetWidth(p.FromMM(VIA_D))
    v.SetFrontTentingMode(p.TENTING_MODE_TENTED)
    v.SetBackTentingMode(p.TENTING_MODE_TENTED)
    v.SetNet(net)
    b.Add(v)
    return v

def get_pad_data(fx):
    pads=[]
    for ref,fp in fx.items():
        for pad in fp.Pads():
            if pad.GetNumber()=='' and not any(pad.IsOnLayer(l) for l in LAYERS): continue
            net=pad.GetNetname().removeprefix('/')
            if not net: net='NC_'+ref+'_'+pad.GetNumber()
            x,y=rel(pad.GetPosition())
            box=pad.GetBoundingBox()
            x0,y0=rel(box.GetOrigin())
            x1,y1=rel(box.GetEnd())
            mask=tuple(i for i,l in enumerate(LAYERS) if pad.IsOnLayer(l))
            if mask:
                pads.append((ref,pad.GetNumber(),net,x,y,(x0,y0,x1,y1),mask))
    return pads

def fields(net,pads,routes,width):
    blocked=np.zeros((len(LAYERS),NX,NY),dtype=bool)
    via_bad=np.zeros((NX,NY),dtype=bool)
    m=round(1.0/STEP)
    blocked[:,:m,:]=blocked[:,-m:,:]=blocked[:,:,:m]=blocked[:,:,-m:]=True
    via_bad[:m,:]=via_bad[-m:,:]=via_bad[:,:m]=via_bad[:,-m:]=True
    if net.startswith('P_'):
        i=int((BOUNDARY-4.25)/STEP)+1
        blocked[:,i:,:]=True; via_bad[i:,:]=True
    else:
        i=math.ceil((BOUNDARY+4.25)/STEP)
        blocked[:,:i,:]=True; via_bad[:i,:]=True
    if RESERVED_LAYER is not None:
        layer, allowed_net = RESERVED_LAYER
        if net != allowed_net: blocked[LAYERS.index(layer),:,:]=True
    for ref,num,n,x,y,box,mask in pads:
        if n!=net:
            g=sep(net,n)+.035
            for k in mask: stamp_rect(blocked[k],box,g+width/2)
            stamp_rect(via_bad,box,g+VIA_D/2)
        else:
            stamp_rect(via_bad,box,VIA_D/2+.15)
    for n,z,a,c,w in routes:
        if n==net:
            if z is None: stamp_segment(via_bad,a,c,.68)
            continue
        g=sep(net,n)+.035
        for k in range(len(LAYERS)) if z is None else (z,):
            stamp_segment(blocked[k],a,c,g+w/2+width/2)
        stamp_segment(via_bad,a,c,g+w/2+VIA_D/2)
    return blocked,via_bad

def search(starts,ends,blocked,via_bad):
    ex,ey,_=ends[0]
    h=lambda x,y: max(abs(x-ex),abs(y-ey))+.414*min(abs(x-ex),abs(y-ey))
    q=[]
    previous={}
    cost={}
    for s in starts:
        cost[s]=0
        heapq.heappush(q,(h(*s[:2]),0,s))
    endset=set(ends)
    pop=heapq.heappop
    push=heapq.heappush
    while q:
        _,g,s=pop(q)
        if g!=cost[s]: continue
        if s in endset:
            route=[s]
            while route[-1] in previous: route.append(previous[route[-1]])
            return route[::-1]
        x,y,k=s
        for dx,dy,d in DXDY:
            X,Y=x+dx,y+dy
            if not (0<=X<NX and 0<=Y<NY) or blocked[k,X,Y]: continue
            if dx and dy and (blocked[k,X,y] or blocked[k,x,Y]): continue
            t=X,Y,k
            G=g+d
            if G<cost.get(t,math.inf):
                previous[t]=s
                cost[t]=G
                push(q,(G+h(X,Y),G,t))
        if not via_bad[x,y]:
            for side in range(len(blocked)):
                if side == k or blocked[side,x,y]:
                    continue
                t=x,y,side
                G=g+14
                if G<cost.get(t,math.inf):
                    previous[t]=s
                    cost[t]=G
                    push(q,(G+h(x,y),G,t))
    return None

def squish(path):
    if len(path)<3: return path
    small=[path[0]]
    for a,b,c in zip(path,path[1:],path[2:]):
        if tuple(b[i]-a[i] for i in range(3))!=tuple(c[i]-b[i] for i in range(3)):
            small.append(b)
    small.append(path[-1])
    return small

def route_board(b,fx,nets,controller_fanout=True,seed_routes=(),term_filter=None,anchors=None):
    pads=get_pad_data(fx)
    names=list(nets)
    preferred=['P_D','P_CL','S_VO','S_FB','S_EN','S_OVP','S_ILIM','S_SLEW','S_FUSED','S_SET_A','S_SET_B',
       'S_LED_KA','S_LED_KB','S_LED_PLUS','S_RTN','S_GND','S_SW','P_BPP','S_FWD','S_BPS',
       'P_L','P_LF','P_LR','P_N','P_0','P_BULK','S_RAW']
    names=EARLY+[n for n in preferred if n not in EARLY]+[n for n in names if n not in preferred and n not in EARLY]
    routes=list(seed_routes)
    failed=[]
    # Fan out the seven controller pins in a staggered row of tented vias.
    # Every pin has a dedicated escape. This prevents a routed ground from
    # surrounding a neighbour before its own route is considered.
    ports={}
    escape_vias=[]
    for ref,num,net,x,y,box,mask in pads:
        if (ref,num) in FRONT_ESCAPE:
            dx=FRONT_ESCAPE[ref,num]
            a=(x,y)
            elbow=(round((x+dx)/STEP)*STEP-math.copysign(.20,dx),y)
            target=(round((x+dx)/STEP)*STEP,round(y/STEP)*STEP)
            track(b,nets[net],[abspt(*a),abspt(*elbow),abspt(*target)],.30,p.F_Cu)
            escape_vias.append((net,target,via(b,nets[net],*target),1))
            routes.extend([(net,0,a,elbow,.30),(net,0,elbow,target,.30),(net,None,target,target,VIA_D)])
            ports[(ref,num)]=(ref,num,net,*target,box,(0,1))
            continue
        if not controller_fanout or ref!='U1' or not num.isdigit() or not 1<=int(num)<=7:
            continue
        target=(BOUNDARY+(6.7 if int(num)%2 else 7.5),round(y/STEP)*STEP)
        elbow=(target[0]-.25,y)
        a=(x,y)
        track(b,nets[net],[abspt(*a),abspt(*elbow),abspt(*target)],.21,p.B_Cu)
        escape_vias.append((net,target,via(b,nets[net],*target),0))
        routes.extend([(net,1,a,elbow,.21),(net,1,elbow,target,.21),(net,None,target,target,VIA_D)])
        ports[(ref,num)]=(ref,num,net,*target,box,(0,1))
    for name in names:
        terms=[ports.get((d[0],d[1]),d) for d in pads
               if d[2]==name and (term_filter is None or term_filter(d[0],d[1]))]
        if anchors:
            terms=[*anchors.get(name,()),*terms]
        if len(terms)<2: continue
        width=MAINS_WIDTH if name in MAINS else .29 if name in WIDE else SIGNAL_WIDTH
        group=[terms.pop(0)]
        tries=0
        while terms and tries<len(terms):
            A,B=min(((a,c) for a in group for c in terms),key=lambda v:(v[0][3]-v[1][3])**2+(v[0][4]-v[1][4])**2+(0 if set(v[0][6])&set(v[1][6]) else 16))
            field,vfield=fields(name,pads,routes,width)
            starts=[(*grid_coord(A[3],A[4]),k) for k in A[6]]
            ends=[(*grid_coord(B[3],B[4]),k) for k in B[6]]
            # Route from the exact centres with a short in-pad connection to the grid.
            def endpoint(x,y,k): return (x*STEP,y*STEP)
            def port(positions):
                return [s for s in positions if not field[s[2],s[0],s[1]]]
            start=port(starts); end=port(ends)
            path=search(start,end,field,vfield) if start and end else None
            if not path:
                failed.append((name,A[:2],B[:2],start,end))
                terms.remove(B)
                continue
            vertices=squish(path)
            k=vertices[0][2]
            a0=(A[3],A[4]); a1=endpoint(*vertices[0])
            if math.dist(a0,a1)>1e-5:
                routes.append((name,k,a0,a1,width))
                track(b,nets[name],[abspt(*a0),abspt(*a1)],width,LAYERS[k])
            for a,c in zip(vertices,vertices[1:]):
                x,y,k=a; X,Y,K=c
                aa=endpoint(*a); cc=endpoint(*c)
                if k==K:
                    routes.append((name,k,aa,cc,width))
                    track(b,nets[name],[abspt(*aa),abspt(*cc)],width,LAYERS[k])
                else:
                    routes.append((name,None,aa,aa,VIA_D))
                    via(b,nets[name],*aa)
            k=vertices[-1][2]
            b0=(B[3],B[4]); b1=endpoint(*vertices[-1])
            if math.dist(b0,b1)>1e-5:
                routes.append((name,k,b0,b1,width))
                track(b,nets[name],[abspt(*b0),abspt(*b1)],width,LAYERS[k])
            group.append(B)
            terms.remove(B)
    for n,xy,v,side in escape_vias:
        if not any(rn==n and z==side and min(math.dist(xy,a),math.dist(xy,c))<.00001 for rn,z,a,c,w in routes):
            b.Remove(v)
    print(f'{len(routes)} objects; {len(failed)} connections failed')
    for f in failed: print(f)
    return failed

if __name__=='__main__':
    d,b,data,fx,nt=pwr()
    route_board(b,fx,nt)
    p.SaveBoard(str(d/'Zasilacz_RevA.kicad_pcb'),b)
    save(ROOT/'work'/'catalog.json',json.dumps([vars(c) for c in data],ensure_ascii=False,indent=2))

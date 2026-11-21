"""Route disconnected native copper groups using any safe existing branch anchor."""
from pathlib import Path
exec(compile(Path(__file__).with_name('grid_stock.py').read_text(encoding='utf-8-sig').split('\njobs=')[0],str(Path(__file__).with_name('grid_stock.py')),'exec'))
def groups():
 b.BuildConnectivity();conn=b.GetConnectivity();lookup={t.m_Uuid.AsString():t for t in list(b.GetTracks())+list(pads.values())};seen=set();out={}
 for p in pads.values():
  ident=p.m_Uuid.AsString();net=p.GetNetname()
  if ident in seen or not net.startswith('/'):continue
  ids={ident}|{a.m_Uuid.AsString() for a in conn.GetConnectedItems(p)};seen|=ids;out.setdefault(net,[]).append([lookup[i] for i in ids if i in lookup])
 return {n:gs for n,gs in out.items() if len(gs)>1}
def anchors(objects,field):
 result={}
 def add(point,sides):
  x,y=(round(point[0]/STEP),round(point[1]/STEP))
  if not 0<=x<NX or not 0<=y<NY:return
  for side in sides:
   if not field[side,x,y]:result[(x,y,side)]=point
 for t in objects:
  if isinstance(t,k.PAD):add(coords(t.GetPosition()),[i for i,l in enumerate(LAYERS) if t.IsOnLayer(l)])
  elif isinstance(t,k.PCB_VIA):add(coords(t.GetPosition()),[0,1])
  else:
   a=coords(t.GetStart());c=coords(t.GetEnd());m=max(1,math.ceil(math.dist(a,c)/.2));side=LAYERS.index(t.GetLayer())
   for i in range(m+1):add((a[0]+(c[0]-a[0])*i/m,a[1]+(c[1]-a[1])*i/m),[side])
 return result
def multiseek(starts,ends,field,vfield):
 if not starts or not ends:return None,0
 endset=set(ends);xs=[s[0] for s in ends];ys=[s[1] for s in ends];loX,hiX,loY,hiY=min(xs),max(xs),min(ys),max(ys)
 def h(x,y):
  dx=max(loX-x,x-hiX,0);dy=max(loY-y,y-hiY,0);return max(dx,dy)+.41421356237*min(dx,dy)
 costs={s:0 for s in starts};prev={};queue=[(h(*s[:2]),0,s) for s in starts];heapq.heapify(queue);count=0
 while queue:
  _,g,s=heapq.heappop(queue)
  if g!=costs[s]:continue
  count+=1
  if s in endset:
   path=[s]
   while path[-1] in prev:path.append(prev[path[-1]])
   return path[::-1],count
  x,y,side=s
  for dx,dy,dist in [(1,0,1),(-1,0,1),(0,1,1),(0,-1,1),(1,1,math.sqrt(2)),(1,-1,math.sqrt(2)),(-1,1,math.sqrt(2)),(-1,-1,math.sqrt(2))]:
   xx=x+dx;yy=y+dy
   if not 0<=xx<NX or not 0<=yy<NY or field[side,xx,yy] or (dx and dy and (field[side,xx,y] or field[side,x,yy])):continue
   node=(xx,yy,side);gg=g+dist
   if gg<costs.get(node,math.inf):costs[node]=gg;prev[node]=s;heapq.heappush(queue,(gg+h(xx,yy),gg,node))
  if not vfield[x,y] and not field[1-side,x,y]:
   node=(x,y,1-side);gg=g+35
   if gg<costs.get(node,math.inf):costs[node]=gg;prev[node]=s;heapq.heappush(queue,(gg+h(x,y),gg,node))
 return None,count
records=[]
for iteration in range(40):
 gs=groups();count=b.GetConnectivity().GetUnconnectedCount(False);print('Groups',iteration,count,flush=True)
 if not count:break
 connected=False
 priority=['/LED_PLUS', '/DC_RETURN', '/BUS_RECT', '/AC_N', '/AC_FUSED', '/SW_SOURCE', '/FB_INDUCTOR', '/M', '/AC_L', '/BUS_FILTERED']
 for net,clusters in sorted(gs.items(),key=lambda a:priority.index(a[0]) if a[0] in priority else 99):
  width=.3;field,vfield=fields(net,width);candidates=[anchors(g,field) for g in clusters]
  for i in range(len(clusters)):
   for j in range(i+1,len(clusters)):
    aa,cc=candidates[i],candidates[j];path,expanded=multiseek(aa,cc,field,vfield);print(net,i,j,'anchors',len(aa),len(cc),'route',bool(path),'expanded',expanded,flush=True)
    if not path:continue
    raw=path;path=simplify(path);nt=next(p.GetNet() for p in pads.values() if p.GetNetname()==net)
    def tr(a,c,side):
     if math.dist(a,c)<1e-6:return
     t=k.PCB_TRACK(b);t.SetNet(nt);t.SetLayer(LAYERS[side]);t.SetWidth(k.FromMM(width));t.SetStart(v(*a));t.SetEnd(v(*c));b.Add(t)
    xy=lambda s:(s[0]*STEP,s[1]*STEP)
    tr(aa[raw[0]],xy(raw[0]),raw[0][2])
    for a,c in zip(path,path[1:]):
     if a[2]==c[2]:tr(xy(a),xy(c),a[2])
     else:
      vi=k.PCB_VIA(b);vi.SetNet(nt);vi.SetPosition(v(*xy(a)));vi.SetViaType(k.VIATYPE_THROUGH);vi.SetLayerPair(k.F_Cu,k.B_Cu);vi.SetWidth(k.FromMM(VD));vi.SetDrill(k.FromMM(DRILL));b.Add(vi)
    tr(xy(raw[-1]),cc[raw[-1]],raw[-1][2]);records.append({'iteration':iteration,'net':net,'start':aa[raw[0]],'end':cc[raw[-1]],'path':path,'expanded':expanded});connected=True;break
   if connected:break
  if connected:break
 if not connected:break
candidate=D/'generic-candidate.kicad_pcb';assert k.SaveBoard(str(candidate),b,True);saved=k.PCB_IO_MGR.Load(k.PCB_IO_MGR.KICAD_SEXP,str(candidate));expected={(r,n):p.GetNetname() for (r,n),p in pads.items()};actual={(f.GetReference(),p.GetNumber()):p.GetNetname() for f in saved.GetFootprints() for p in f.Pads()};assert expected==actual
shutil.copy2(src,D/'before-generic.kicad_pcb');shutil.copy2(candidate,src);saved.BuildConnectivity();(D/'generic-results.json').write_text(json.dumps({'routes':records,'remaining':saved.GetConnectivity().GetUnconnectedCount(False)},indent=2)+'\n');print('Genericremaining',saved.GetConnectivity().GetUnconnectedCount(False),flush=True)


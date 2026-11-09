from pathlib import Path
import json, math, uuid
import pcbnew as p

ROOT = Path.cwd()
LIB = Path(r'C:\Program Files\KiCad\10.0\share\kicad\footprints')
def uid(): return str(uuid.uuid4())
def q(s): return json.dumps(str(s), ensure_ascii=False)
def fmt(x): return f'{x:.5f}'.rstrip('0').rstrip('.') if x else '0'
def pt(x, y): return p.VECTOR2I(round(x*1e6), round(y*1e6))
def save(path, s): path.write_text(s, encoding='utf-8')
def prop(name, val, x, y, hide=False):
    return f'(property {q(name)} {q(val)} (at {fmt(x)} {fmt(y)} 0) (effects (font (size 1.02 1.02)) {"(hide yes)" if hide else ""}))'
def wire(x1,y1,x2,y2):
    return f'(wire (pts (xy {fmt(x1)} {fmt(y1)}) (xy {fmt(x2)} {fmt(y2)})) (stroke (width 0) (type default)) (uuid "{uid()}"))'
def label(n,x,y,a=0):
    return f'(label {q(n)} (at {fmt(x)} {fmt(y)} {a}) (effects (font (size 0.95 0.95)) (justify {"left" if a==0 else "right"} bottom)) (uuid "{uid()}"))'
def note(s,x,y,size=1.27):
    return f'(text {q(s)} (at {x} {y} 0) (effects (font (size {size} {size})) (justify left)) (uuid "{uid()}"))'
def box(x,y,x2,y2,fill='none'):
    return f'(rectangle (start {x} {y}) (end {x2} {y2}) (stroke (width 0.254) (type default)) (fill (type {fill})))'
def pin(n,name,x,y,a,length=2.54,kind='passive'):
    return f'(pin {kind} line (at {x} {y} {a}) (length {length}) (name {q(name)} (effects (font (size 1.02 1.02)))) (number {q(n)} (effects (font (size 1.02 1.02)))))'
def symbol(name,ref,graphic,pins, show=False, default_fp=""):
    nm=name.split(':')[-1]
    return f'''(symbol {q(name)} (pin_numbers {"" if show else "(hide yes)"}) (pin_names (offset 0.7) {"" if show else "(hide yes)"})
      (exclude_from_sim no) (in_bom yes) (on_board yes)
      {prop('Reference',ref,0,4)} {prop('Value',nm,0,-4)} {prop('Footprint',default_fp,0,0,True)}
      (symbol "{nm}_0_1" {graphic}) (symbol "{nm}_1_1" {" ".join(pins)}))'''
def placed(lib,ref,val,fp,x,y,sid,project,sheet,numbers,hide=False):
    return f'''(symbol (lib_id {q(lib)}) (at {x} {y} 0) (unit 1) (exclude_from_sim no) (in_bom {'no' if lib == 'E27:SpringPad' else 'yes'}) (on_board yes) (dnp no) (uuid "{sid}")
    {prop('Reference',ref,x,y-3.81)}
    {prop('Value',val,x,y+3.81,hide)}
    {prop('Footprint',fp,x,y,True)}
    {" ".join(f'(pin "{n}" (uuid "{uid()}"))' for n in numbers)}
    (instances (project "{project}" (path "/{sheet}" (reference "{ref}") (unit 1)))))'''
def poly(points, fill='none', width=0.254):
    xy=' '.join(f'(xy {x} {y})' for x,y in points)
    return f'(polyline (pts {xy}) (stroke (width {width}) (type default)) (fill (type {fill})))'
LED = 'E27:Cree_JE2835B'
LED_FP = 'E27:Cree_JE2835B'
CONTACT = 'E27:SpringPad'
A = 'LED_PLUS'
def begin(name, subtitle, min_clear, edge, custom_rules=None):
    d=ROOT/'outputs'/name
    (d/'E27.pretty').mkdir(parents=True,exist_ok=True)
    proj={"meta":{"filename":name+".kicad_pro","version":1},"board":{"design_settings":{"rules":{
        "min_clearance":min_clear,"min_copper_edge_clearance":edge,"min_track_width":0.2,"min_through_hole_diameter":0.3,
        "min_via_diameter":0.55,"min_via_annular_width":0.12
    }}}, "net_settings":{"classes":[{"name":"Default","clearance":min_clear,"track_width":0.30,"via_diameter":0.65,"via_drill":0.30}],"meta":{"version":4}}}
    save(d/(name+'.kicad_pro'),json.dumps(proj,indent=2))
    save(d/'fp-lib-table','(fp_lib_table (version 7) (lib (name "E27") (type "KiCad") (uri "${KIPRJMOD}/E27.pretty") (options "") (descr "E27 Rev A")))')
    save(d/'sym-lib-table','(sym_lib_table (version 7) (lib (name "E27") (type "KiCad") (uri "${KIPRJMOD}/E27.kicad_sym") (options "") (descr "E27 Rev A")))')
    if custom_rules: save(d/(name+'.kicad_dru'),custom_rules)
    b=p.BOARD()
    return d,b,uid()
def fpdef(name,desc,pads,body,silk='',models='',attr='smd'):
    return f'''(footprint "{name}" (version 20241229) (generator "pcbnew") (layer "F.Cu") (descr {q(desc)}) (attr {attr})
      (fp_text reference "REF**" (at 0 -2.3) (layer "F.SilkS") (effects (font (size 0.68 0.68) (thickness 0.12))))
      (fp_text value "{name}" (at 0 2.5) (layer "F.Fab") (effects (font (size 0.7 0.7) (thickness 0.12))))
      {body} {silk} {pads} {models})'''
def smd(n,x,y,w,h,paste=True,ratio=None):
    paste_layer = '"F.Paste"' if paste else ''
    return f'(pad "{n}" smd rect (at {x} {y}) (size {w} {h}) (layers "F.Cu" {paste_layer} "F.Mask") {f"(solder_paste_margin_ratio {ratio})" if ratio else ""})'
def fp_rect(x1,y1,x2,y2,layer,width=0.10):
    return f'(fp_rect (start {x1} {y1}) (end {x2} {y2}) (stroke (width {width}) (type default)) (fill none) (layer "{layer}"))'
def fp_line(x1,y1,x2,y2,layer,width=.12):
    return f'(fp_line (start {x1} {y1}) (end {x2} {y2}) (stroke (width {width}) (type default)) (layer "{layer}"))'
def vrml_box(x,y,h,color):
    return f'Transform {{ translation 0 0 {h/(2*2.54):.5f} children [ Shape {{ appearance Appearance {{ material Material {{ diffuseColor {color} }} }} geometry Box {{ size {x/2.54:.5f} {y/2.54:.5f} {h/2.54:.5f} }} }} ] }}'
def led_model(d):
    c='0.91 0.73 0.19'
    lens=f'Transform {{ translation 0 0 {0.59/2.54:.5f} children [ Shape {{ appearance Appearance {{ material Material {{ diffuseColor {c} }} }} geometry Box {{ size {2.55/2.54:.5f} {2.4/2.54:.5f} {0.16/2.54:.5f} }} }} ] }}'
    save(d/'Cree_JE2835B.wrl','#VRML V2.0 utf8\n'+vrml_box(3.5,2.8,.52,'0.92 0.91 0.83')+'\n'+lens)
def footprint(b,d,full,ref,value,x,y,rot,sid,root,nets,hide=True):
    library,name=full.split(':')
    fp=p.FootprintLoad(str(d/'E27.pretty' if library=='E27' else LIB/(library+'.pretty')),name)
    if not fp: raise RuntimeError(full)
    fp.SetFPID(p.LIB_ID(library,name))
    fp.SetReference(ref)
    fp.SetValue(value)
    fp.SetPosition(pt(x,y))
    fp.SetOrientationDegrees(rot)
    fp.Reference().SetVisible(not hide)
    fp.Value().SetVisible(False)
    fp.SetPath(p.KIID_PATH('/'+root+'/'+sid))
    b.Add(fp)
    for pad in fp.Pads():
        n=nets.get(pad.GetNumber())
        if n is not None: pad.SetNet(n)
    return fp
def shape(b,layer,a,c,mid=None):
    s=p.PCB_SHAPE()
    if mid:
        s.SetShape(p.SHAPE_T_ARC)
        s.SetArcGeometry(pt(*a),pt(*mid),pt(*c))
    else:
        s.SetShape(p.SHAPE_T_SEGMENT)
        s.SetStart(pt(*a))
        s.SetEnd(pt(*c))
    s.SetLayer(layer)
    s.SetWidth(p.FromMM(.05 if layer==p.Edge_Cuts else .12))
    b.Add(s)
def txt(b,s,x,y,size=.8,layer=p.F_SilkS):
    t=p.PCB_TEXT(b)
    t.SetText(s)
    t.SetPosition(pt(x,y))
    t.SetTextSize(pt(size,size))
    t.SetTextThickness(p.FromMM(.12))
    t.SetLayer(layer)
    b.Add(t)
def nets_for(b,names):
    out={}
    for name in sorted(set(names)):
        net=p.NETINFO_ITEM(b,'/'+name)
        b.Add(net)
        out[name]=net
    return out
def track(b, net, points,width=.45, layer=p.F_Cu):
    for a,c in zip(points,points[1:]):
        if a==c: continue
        t=p.PCB_TRACK(b)
        t.SetStart(pt(*a))
        t.SetEnd(pt(*c))
        t.SetWidth(p.FromMM(width))
        t.SetLayer(layer)
        t.SetNet(net)
        b.Add(t)
def padpos(fp,num):
    a=fp.FindPadByNumber(str(num)).GetPosition()
    return (a.x/1e6,a.y/1e6)
def schematic(d,name,sheet,title,defs,contents,paper='A4',revision='A'):
    save(d/'E27.kicad_sym','(kicad_symbol_lib (version 20241209) (generator "kicad_symbol_editor")\n'+'\n'.join(s.replace('"E27:','"',1) for s in defs)+'\n)')
    save(d/(name+'.kicad_sch'),f'''(kicad_sch (version 20250114) (generator "eeschema")
     (uuid "{sheet}") (paper "{paper}") (title_block (title {q(title)}) (rev "{revision}") (date "2026-11-09"))
     (lib_symbols {" ".join(defs)})
     {" ".join(contents)})''')
def led():
    name='Wklad_LED'
    d,b,sheet=begin(name,'LED',.24,.6)
    b.SetCopperLayerCount(1)
    pad=smd('1',-.845,0,2.2,1.8,True,-.2)+smd('2',1.395,0,1.1,1.8,True,-.2)
    led_silk=fp_line(-2.02,-1.12,-2.02,1.12,'F.SilkS')
    # Separate body and copper datum. Body follows the datasheet body centre.
    save(d/'E27.pretty/Cree_JE2835B.kicad_mod',fpdef('Cree_JE2835B','JE2835B CLJ-DS40 p57: pad 1 cathode',
         pad,fp_rect(-1.75,-1.4,1.75,1.4,'F.Fab')+fp_rect(-2.2,-1.65,2.2,1.65,'F.CrtYd',.05),
         led_silk,'(model "${KIPRJMOD}/Cree_JE2835B.wrl" (offset (xyz 0 0 0)) (scale (xyz 1 1 1)) (rotate (xyz 0 0 0)))'))
    led_model(d)
    save(d/'E27.pretty/SpringPad.kicad_mod',fpdef('SpringPad','Flat top contact; 2.4 x 1.6; no paste',
          smd('1',0,0,2.4,1.6,False),fp_rect(-1.43,-.81,1.43,.81,'F.CrtYd',.05),attr='smd exclude_from_pos_files exclude_from_bom'))
    # KiCad drawing uses A to the left and K to the right.
    graphics=poly([(-1.27,-1.27),(-1.27,1.27),(1.27,0),(-1.27,-1.27)])+poly([(1.27,1.27),(1.27,-1.27)])
    defs=[symbol(LED,'D',graphics,[pin(2,'A',-3.81,0,0),pin(1,'K',3.81,0,180)],default_fp=LED_FP),
          symbol(CONTACT,'J',box(-1.27,0.85,1.27,-.85,'background'),[pin(1,'Contact',3.81,0,180)],default_fp=CONTACT)]
    items=[note('WYMIENNY MODUL E27 / 16 x JE2835B / Rev A',31.75,31.75,2.1),
           note('Dwa niezalezne szeregi. Wklad nie zawiera ukladu regulacji pradu.',31.75,40.64),
           note('J1: wspolna anoda    J2: powrot A    J3: powrot B',31.75,46.99),
           note('Warianty 2700 / 4000 / 6500 K wedlug BOM. Maks. 150 mA na szereg w prototypie.',31.75,131.445)]
    seq=[[A]+[f'{c}{i}' for i in range(1,8)]+['LED_K'+c] for c in 'AB']
    nt=nets_for(b,sum(seq,[]))
    f=[]
    cx,cy=100,85
    for i in range(16):
        ch,j=divmod(i,8)
        row,col=divmod(i,4)
        x=cx+([-7.5,-2.5,2.5,7.5] if row%2==0 else [7.5,2.5,-2.5,-7.5])[col]
        y=cy+[-7.5,-2.5,2.5,7.5][row]
        ref='D'+str(i+1)
        sid=uid()
        f.append(footprint(b,d,LED_FP,ref,'JE2835B',x,y,180 if row%2==0 else 0,sid,sheet,
                            {'2':nt[seq[ch][j]],'1':nt[seq[ch][j+1]]}))
        sx=49.53+22.86*j
        sy=[74.93,107.95][ch]
        items.append(placed(LED,ref,'JE2835B',LED_FP,sx,sy,sid,name,sheet,[1,2],True))
        if j<7:
            items += [wire(sx+3.81,sy,sx+22.86-3.81,sy),label(seq[ch][j+1],sx+3.81,sy)]
        if j==0:
            items += [wire(sx-3.81,sy,sx-11.43,sy),label(A,sx-11.43,sy)]
        if j==7:
            items += [wire(sx+3.81,sy,sx+11.43,sy),label(seq[ch][8],sx+11.43,sy)]
    contacts=[]
    for i,(net,xx,yy) in enumerate([(A,-11.7,0),('LED_KA',-7.25,0),('LED_KB',-7.25,10.55)],1):
        sid=uid()
        ref='J'+str(i)
        contacts.append(footprint(b,d,CONTACT,ref,net,cx+xx,cy+yy,0,sid,sheet,{'1':nt[net]}))
        x=238.76
        y=66.04+12.7*(i-1)
        items += [placed(CONTACT,ref,net,CONTACT,x,y,sid,name,sheet,[1],True),wire(x+3.81,y,x+10.16,y),label(net,x+10.16,y)]
    for ch in range(2):
        for j in range(7):
            i=ch*8+j
            a=padpos(f[i],1); z=padpos(f[i+1],2)
            if j==3:
                side=cx+11.35
                track(b,nt[seq[ch][j+1]],[a,(side-.65,a[1]),(side,a[1]+.65),(side,z[1]-.65),(side-.65,z[1]),z])
            else:
                track(b,nt[seq[ch][j+1]],[a,z],.52)
    ap=padpos(contacts[0],1)
    for i in (0,8):
        z=padpos(f[i],2)
        t=1 if z[1]>ap[1] else -1
        track(b,nt[A],[ap,(ap[0],z[1]-t*.8),(ap[0]+.8,z[1]),z])
    for k,i,c in [('LED_KA',7,1),('LED_KB',15,2)]:
        a=padpos(f[i],1); z=padpos(contacts[c],1)
        track(b,nt[k],[a,(a[0],z[1]-abs(a[0]-z[0])),z])
    xx=13.4; dy=math.sqrt(15**2-xx**2)
    shape(b,p.Edge_Cuts,(cx+xx,cy-dy),(cx+xx,cy+dy),(cx-15,cy))
    shape(b,p.Edge_Cuts,(cx+xx,cy+dy),(cx+xx,cy-dy))
    txt(b,'A+',cx-11.7,cy-2.45,.8)
    txt(b,'K1',cx-4.65,cy,.8)
    txt(b,'K2',cx-4.65,cy+10.55,.8)
    txt(b,'E27 / REV A',cx+.6,cy-11,.9)
    txt(b,'D30 / KEY',cx+1,cy+11,.8)
    schematic(d,name,sheet,'Wymienny modul LED - Rev A',defs,items)
    p.SaveBoard(str(d/(name+'.kicad_pcb')),b)

if __name__=='__main__': led()

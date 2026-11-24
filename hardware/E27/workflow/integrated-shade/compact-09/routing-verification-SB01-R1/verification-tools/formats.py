"""Fail-closed, bounded readers for the pinned KiCad fabrication export subset."""
from pathlib import Path
import math,re

class Unsupported(ValueError):pass

ROUNDRECT=['4,1,4,$2,$3,$4,$5,$6,$7,$8,$9,$2,$3,0','1,1,$1+$1,$2,$3','1,1,$1+$1,$4,$5','1,1,$1+$1,$6,$7','1,1,$1+$1,$8,$9','20,1,$1+$1,$2,$3,$4,$5,0','20,1,$1+$1,$4,$5,$6,$7,0','20,1,$1+$1,$6,$7,$8,$9,0','20,1,$1+$1,$8,$9,$2,$3,0']

def metadata(path):
    text=Path(path).read_text(encoding='utf-8-sig');return {m[1]:m[2] for m in re.finditer(r'%TF\.([^,*]+),([^*]*)\*%',text)}

def aperture_geometry(ap):
    name=ap['shape'];a=ap['args']
    if name=='C' and len(a)==1:return ('C',a[0],a[0],a[0]/2)
    if name in ('R','O') and len(a)==2:return (name,a[0],a[1],min(a)/2 if name=='O' else 0.)
    if name=='RoundRect' and len(a)==10 and a[-1]==0:
        radius=a[0];xs=a[1:9:2];ys=a[2:9:2]
        if radius<0 or len(set(round(x,6)for x in xs))!=2 or len(set(round(y,6)for y in ys))!=2:raise Unsupported('Non-axis-aligned roundrect aperture')
        corners=list(zip(xs,ys))
        if len(set(corners))!=4 or abs(max(xs)+min(xs))>1e-6 or abs(max(ys)+min(ys))>1e-6 or any((x==u)==(y==v)for (x,y),(u,v)in zip(corners,corners[1:]+corners[:1])):
            raise Unsupported('Off-center or invalid roundrect macro corner ordering')
        return ('RoundRect',max(xs)-min(xs)+2*radius,max(ys)-min(ys)+2*radius,radius)
    raise Unsupported('Unsupported aperture geometry '+str(ap))

def gerber(path):
    path=Path(path);text=path.read_text(encoding='utf-8-sig')
    if len(text)>100_000_000:raise Unsupported('Gerber exceeds bounded reader size')
    lines=text.splitlines();aps={};ops=[];macros={};position=(0.,0.);selected=None;ref=None;net=None;function=None;polarity='dark';region=None;contour=None;seen_format=False;seen_units=False;ended=False;i=0
    while i<len(lines):
        line=lines[i].strip();i+=1
        if not line:continue
        if line.startswith('G04 '):continue
        if ended:raise Unsupported('Data after Gerber end')
        if line.startswith('%TF.'):continue
        if line=='%FSLAX46Y46*%':seen_format=True;continue
        if line=='%MOMM*%':seen_units=True;continue
        if line.startswith('%AM'):
            name=line[3:-1]
            if not line.endswith('*')or name in macros:raise Unsupported('Unsupported/duplicate aperture macro header')
            body=[]
            while i<len(lines):
                row=lines[i].strip();i+=1;last=row.endswith('*%')
                if not row.endswith('*') and not last:raise Unsupported('Malformed aperture macro')
                row=row[:-2]if last else row[:-1]
                if row and not row.startswith('0 '):body.append(row)
                if last:break
            else:raise Unsupported('Unclosed aperture macro')
            if name!='RoundRect'or body!=ROUNDRECT:raise Unsupported('Unsupported or changed aperture macro '+name)
            macros[name]=body;continue
        m=re.fullmatch(r'%TA\.AperFunction,([^*]+)\*%',line)
        if m:function=m[1];continue
        if line.startswith('%TA.'):raise Unsupported('Unsupported aperture attribute '+line)
        m=re.fullmatch(r'%ADD(\d+)([A-Za-z][A-Za-z0-9_]*),([^*]+)\*%',line)
        if m:
            code=int(m[1]);name=m[2]
            if code in aps:raise Unsupported('Duplicate aperture code')
            args=list(map(float,m[3].split('X')))
            if not all(math.isfinite(x)for x in args):raise Unsupported('Nonfinite aperture parameter')
            ap={'shape':name,'args':args,'function':function};aperture_geometry(ap)
            if name=='RoundRect' and name not in macros:raise Unsupported('RoundRect has no exact checked macro')
            aps[code]=ap;continue
        if line=='%TD*%':ref=net=function=None;continue
        m=re.fullmatch(r'%TO\.P,([^*]+)\*%',line)
        if m:
            fields=m[1].split(',')
            if len(fields)<2:raise Unsupported('Malformed physical pad attribute')
            ref=fields[:2];continue
        m=re.fullmatch(r'%TO\.N,([^*]+)\*%',line)
        if m:net=m[1];continue
        if line.startswith('%TO.C,'):continue
        if line.startswith('%TO.'):raise Unsupported('Unsupported object attribute '+line)
        if line=='%LPD*%':polarity='dark';continue
        if line=='%LPC*%':polarity='clear';continue
        if line=='G01*':continue
        if line=='M02*':
            if region is not None:raise Unsupported('Gerber ended in region')
            ended=True;continue
        if line=='G36*':
            if region is not None:raise Unsupported('Nested Gerber region')
            region=[];contour=None;continue
        if line=='G37*':
            if region is None:raise Unsupported('Region end without start')
            if contour:region.append(contour)
            if not region:raise Unsupported('Empty Gerber region')
            if any(len(p)<4 or p[0]!=p[-1]for p in region):raise Unsupported('Unclosed/degenerate Gerber contour')
            ops.append({'kind':'region','contours':region,'polarity':polarity});region=contour=None;continue
        m=re.fullmatch(r'D(\d+)\*',line)
        if m:
            selected=int(m[1])
            if selected not in aps:raise Unsupported('Undeclared aperture selected')
            continue
        m=re.fullmatch(r'X(-?\d+)Y(-?\d+)D0([123])\*',line)
        if m:
            if not seen_format or not seen_units:raise Unsupported('Coordinate before supported format/units')
            end=(int(m[1])/1e6,-int(m[2])/1e6);mode=int(m[3])
            if region is not None:
                if mode==2:
                    if contour:region.append(contour)
                    contour=[end]
                elif mode==1:
                    if contour is None:raise Unsupported('Region drawing before move')
                    contour.append(end)
                else:raise Unsupported('Flash within region')
            elif mode!=2:
                if selected not in aps:raise Unsupported('Drawing without aperture')
                op={'kind':'line'if mode==1 else'flash','aperture':aps[selected],'ref':ref,'net':net,'polarity':polarity}
                if mode==1:op.update(a=position,z=end)
                else:op['position']=end
                ops.append(op)
            position=end;continue
        raise Unsupported('Unsupported Gerber command '+line)
    if not ended or not seen_units or not seen_format:raise Unsupported('Missing Gerber format/units/end')
    return {'file':str(path),'metadata':metadata(path),'apertures':aps,'operations':ops}

def excellon(path):
    tools={};tool=None;hits=[];metric=False;absolute=False;ended=False;header=False;filefunction=None
    for raw in Path(path).read_text(encoding='utf-8-sig').splitlines():
        line=raw.strip()
        if not line:continue
        if line.startswith(';'):
            m=re.search(r'TF\.FileFunction,([^*]+)',line)
            if m:filefunction=m[1]
            continue
        if ended:raise Unsupported('Data after drill end')
        if line=='M48':header=True;continue
        if line=='FMAT,2':continue
        if line=='METRIC':metric=True;continue
        if line=='%':header=False;continue
        if line=='G90':absolute=True;continue
        if line=='G05':continue
        if line in ('M30','M00'):ended=True;continue
        m=re.fullmatch(r'T(\d+)C([\d.]+)',line)
        if m:
            if not header or int(m[1])in tools:raise Unsupported('Invalid drill tool declaration')
            tools[int(m[1])]=float(m[2]);continue
        m=re.fullmatch(r'T(\d+)',line)
        if m:
            tool=int(m[1])
            if tool not in tools:raise Unsupported('Undeclared drill tool')
            continue
        m=re.fullmatch(r'X(-?[\d]+(?:\.[\d]+)?)Y(-?[\d]+(?:\.[\d]+)?)',line)
        if m:
            if not metric or not absolute or tool not in tools:raise Unsupported('Drill hit before supported metric absolute mode/tool')
            hits.append({'position':(float(m[1]),-float(m[2])),'diameter':tools[tool]});continue
        raise Unsupported('Unsupported Excellon command '+line)
    if not metric or not absolute or not ended or not filefunction:raise Unsupported('Incomplete metric absolute Excellon/profile header')
    if filefunction not in ('Plated,1,2,PTH','NonPlated,1,2,NPTH'):raise Unsupported('Unsupported drill plating/layer profile '+filefunction)
    return {'file':str(path),'tools':tools,'hits':hits,'plated':filefunction.startswith('Plated'),'filefunction':filefunction}

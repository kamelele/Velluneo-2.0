"""Build detailed visual package models in millimetres for the KiCad previews."""
import math
from pathlib import Path
import re

MM_PER_WRL = 2.54
METAL = (.72,.73,.75)
TIN = (.68,.66,.58)
BLACK = (.105,.105,.11)
GREY = (.17,.17,.175)
BLUE = (.075,.28,.54)
YELLOW = (.88,.67,.19)
COPPER = (.59,.28,.11)


def unit(value):
    return f'{value/MM_PER_WRL:.5f}'


def render_shape(geometry, pos, color, rotation='0 0 1 0'):
    xyz = ' '.join(map(unit, pos))
    material = ' '.join(map(str,color))
    return (f'Transform {{ translation {xyz} rotation {rotation} children [ Shape {{ '
            f'appearance Appearance {{ material Material {{ diffuseColor {material} '
            f'specularColor 0.23 0.23 0.23 shininess 0.28 }} }} '
            f'geometry {geometry} }} ] }}')


def box(w,d,h,x,y,z,color):
    return render_shape('Box { size '+' '.join(map(unit,(w,d,h)))+' }',(x,y,z),color)


def cyl(d,h,x,y,z,color,axis='z'):
    count = 40
    points = []
    for level in (-h/2,h/2):
        for i in range(count):
            angle = 2*math.pi*i/count
            a,b = d/2*math.cos(angle),d/2*math.sin(angle)
            points.append({'z':(a,b,level), 'y':(b,level,a), 'x':(level,a,b)}[axis])
    faces = []
    for i in range(count):
        j = (i+1) % count
        faces.append((i,j,j+count,i+count))
    faces.extend([tuple(reversed(range(count))),tuple(range(count,2*count))])
    vertices = ', '.join(' '.join(map(unit,p)) for p in points)
    indexes = ', '.join(', '.join(map(str,f))+', -1' for f in faces)
    geometry = (f'IndexedFaceSet {{ creaseAngle 0.5 coord Coordinate {{ point [ {vertices} ] }} '
                f'coordIndex [ {indexes} ] }}')
    return render_shape(geometry,(x,y,z),color)

def pins(points, height, dia):
    return [cyl(dia,height,x,y,(height-3)/2,METAL) for x,y in points]


def tmov():
    return pins([(-3.75,0),(3.75,0)],6,.83) + [
        cyl(17.0,5.4,0,0,11.7,BLUE,'y'), cyl(16.7,1.0,0,2.7,11.7,(.07,.24,.47),'y'),
        box(9,3.1,9,1.8,-3.1,8.25,(.085,.23,.42)),
        box(8,0.08,.36,0,3.23,14.3,(.68,.78,.82)),
        box(5.5,0.08,.28,0,3.23,13.2,(.68,.78,.82)),
    ]


def safety_cap():
    return pins([(-5,0),(5,0)],7.4,.8)+[
        cyl(10.9,5.7,0,0,7.55,(.11,.33,.67),'y'),
        box(6,.08,.28,0,2.87,8.6,(.67,.76,.86)),
    ]


def transformer():
    feet = [(-6.5,-4.8),(-6.5,-1.6),(-6.5,1.6),(-6.5,4.8),(6.5,-4.8),(6.5,4.8)]
    result = pins(feet,3,.77)
    result += [box(16.6,13.6,2,0,0,1.05,BLACK), box(13.2,14.9,2.25,0,0,14.3,GREY),
               box(15.9,15.45,2.5,0,0,2.9,GREY), box(14.2,12.7,9.4,0,0,8.55,YELLOW),
               box(12.4,10.9,1.2,0,0,13.25,(.65,.46,.14))]
    for x in (-6.65,6.65):
        result += [box(2.65,15.45,9.25,x,0,8.75,GREY),
                   box(2.69,15.5,.14,x,0,8.74,(.07,.07,.07))]
    for y in (-6.4,6.4):
        result.append(box(10.5,.13,8.4,0,y,8.5,(.76,.53,.17)))
        for z in (6.4,6.85,7.3):
            result.append(box(7.5,.10,.16,0,y*1.011,z,COPPER))
    result += [box(5.3,6,.09,0,0,15.47,(.49,.51,.45)),
               box(4.0,.3,.10,0,.9,15.52,(.15,.16,.14))]
    return result


def inductor():
    result = pins([(-2.5,0),(2.5,0)],2.1,.75)
    result += [cyl(8.35,1.1,0,0,1.15,GREY),cyl(8.35,1.1,0,0,9.45,GREY),
               cyl(5.8,7.35,0,0,5.3,(.35,.16,.08)),cyl(6.8,.24,0,0,10.12,(.18,.19,.20))]
    for i in range(20):
        result.append(cyl(7.35,.29,0,0,1.98+i*.35,COPPER))
    return result


def electrolytic():
    parts = [box(13.55,13.55,1.15,0,0,.62,BLACK),
             cyl(12.5,11.75,0,0,7.04,(.45,.46,.46)),
             cyl(12.38,.36,0,0,13.17,(.73,.74,.74)),
             box(2,2.2,.15,-4.15,0,.095,TIN),box(2,2.2,.15,4.15,0,.095,TIN)]
    parts += [box(8,.17,.022,0,0,13.36,GREY),
              box(.17,8,.022,0,0,13.36,GREY),
              box(2.2,3.4,.028,4.28,0,13.36,BLACK)]
    return parts


def fuse():
    return [box(14.65,5.4,4.65,0,0,2.57,(.83,.81,.74)),
            box(10,4.8,.4,0,0,5.0,(.86,.84,.76)),
            box(5.2,.55,.032,0,0,5.22,(.18,.19,.20))] + [
        box(1.55,5.58,4.94,x,0,2.62,METAL) for x in (-6.67,6.67)
    ]


def resistor():
    parts = [cyl(4.6,11.5,0,0,2.65,(.34,.53,.46),'x')]
    for x in (-7.1,7.1):
        parts += [box(2.75,2.05,.36,x,0,.18,TIN),
                  cyl(.82,2.35,x*.88,0,1.55,METAL,'x')]
    for x,color in [(-3.75,(.58,.13,.12)),(-2.54,(.58,.13,.12)),(-1.33,(.13,.10,.09)),
                    (3.4,(.63,.50,.21))]:
        parts.append(cyl(4.64,.42,x,0,2.65,color,'x'))
    return parts


def ic(width,length,h,coords,pin_width):
    parts = [box(width,length,h-.23,0,0,.12+(h-.23)/2,BLACK),
             box(width-.16,length-.16,.15,0,0,h-.07,GREY)]
    left = next((p for p in coords if p[0]<0),None)
    if left:
        parts += [cyl(.33,.026,-width/2+.42,left[1],h+.019,(.53,.55,.55))]
    for x,y in coords:
        if not x:
            continue
        side = 1 if x>0 else -1
        lead_len = abs(x)-width/2
        if lead_len <= 0:
            continue
        parts += [box(lead_len+.29,pin_width,.15,side*(abs(x)+width/2)/2,y,.10,METAL),
                  box(.18,pin_width,.31,side*(width/2+.19),y,.27,METAL)]
    return parts


def models(source, target):
    def lead_positions(model):
        data = (source / 'E27.pretty' / f'{model}.kicad_mod').read_text(encoding='utf8')
        coords = re.findall(r'\(pad "[^"]+" smd \w+ \(at (-?[\d.]+) (-?[\d.]+)\)', data)
        return [(float(x),-float(y)) for x,y in coords]

    packages = {'PWP0016A':(4.4,5.0,1.2,.24),'E27_Al5812_MSOP':(3.0,3.0,1.05,.23),
                'TPS7A16_DGN':(3.0,3.0,1.1,.23),'InSOP_24D':(7.5,9.4,1.7,.30),
                'AQY212GS_SOP4':(4.4,4.3,2.0,.43)}
    bodies = {'TMOV14':tmov(), 'CY1_10mm':safety_cap(), 'EE16_6pins_RFQ':transformer(),
              'Wurth_TI_HV_8':inductor(),'UCM_12p5':electrolytic(),
              'Schurter_UMT_H':fuse(), 'AC01_CS_WSZ':resistor()}
    for model, (w,d,h,pin) in packages.items():
        positions = lead_positions(model)
        assert positions, model
        bodies[model] = ic(w,d,h,positions,pin)
    bodies['MB10S_751EP'] = ic(3.9,4.725,1.65,[(-3.25,1.27),(-3.25,-1.27),(3.25,-1.27),(3.25,1.27)],.52)
    for model,parts in bodies.items():
        (target / f'{model}.wrl').write_text('#VRML V2.0 utf8\n'+'\n'.join(parts)+'\n',encoding='utf8')


if __name__ == '__main__':
    out = Path('outputs')
    target = out/'Studium_RevE'
    models(out/'Zasilacz_RevD_JLCPCB',target)
    for name in ('E_Jedna','E_Moc','E_Sterowanie'):
        pcb = target / f'{name}.kicad_pcb'
        if pcb.exists():
            text = pcb.read_text(encoding='utf8')
            new = re.sub(r'\$\{KICAD10_3DMODEL_DIR\}/Package_SO\.3dshapes/OnSemi_751EP_[^"]+\.step',
                         '${KIPRJMOD}/MB10S_751EP.wrl',text)
            if new != text:
                pcb.write_text(new,encoding='utf8')

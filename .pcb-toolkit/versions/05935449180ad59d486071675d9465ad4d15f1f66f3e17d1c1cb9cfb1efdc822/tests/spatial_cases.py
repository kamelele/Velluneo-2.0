"""Actual pcbnew + CLI spatial tests, using original non-confidential geometry."""
import copy
import json
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as pcb
import spatial_fixture as fixture
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import pcb_rules as rules
import spatial


def run(work,board_fn,schematic_fn,compose,record):
    cli=rules.cli_path(None)
    scenarios=[('no-outline',fixture.area(rectangle=[25,4,30,6]),False),
               ('outside',fixture.area(rectangle=[25,4,30,6]),False),
               ('track',fixture.area(),True),
               ('local-exception',fixture.area('A'),False),
               ('other-net-exception',fixture.area('B'),True),
               ('other-layer',fixture.area(layers=['B.Cu']),False),
               ('via',fixture.area(rectangle=[24,24,26,26],disallow=['via']),True),
               ('via-outside',fixture.area(rectangle=[28,24,30,26],disallow=['via']),False),
               ('pad',fixture.area(rectangle=[4,4,6,6],disallow=['pad']),True),
               ('pad-outside',fixture.area(rectangle=[28,24,30,26],disallow=['pad']),False),
               ('zone',fixture.area(rectangle=[18,18,22,22],disallow=['zone']),True),
               ('zone-outside',fixture.area(rectangle=[28,24,30,26],disallow=['zone']),False),
               ('class-width',fixture.area(rectangle=[25,4,30,6]),False),
               ('class-width-valid',fixture.area(rectangle=[25,4,30,6]),False),
               ('exception-other-area',fixture.area('A'),True)]
    for case,area,expected in scenarios:
        folder=work/('spatial-'+case);c=board_fn(folder,'valid');schematic_fn(folder)
        b=pcb.LoadBoard(str(folder/'board.kicad_pcb'))
        if case=='no-outline':
            drawings=b.Drawings()
            for i in range(len(drawings)):b.Remove(drawings[0])
        # Anchor both exact exception nets independently of KiCad's track reconciliation.
        nets={str(n.GetNetname()):n for n in b.GetNetsByNetcode().values()}
        if 'B' not in nets:
            n=pcb.NETINFO_ITEM(b,'B');b.Add(n);nets['B']=n
        if 'A' not in nets:
            n=pcb.NETINFO_ITEM(b,'A');b.Add(n);nets['A']=n
        for item in [b.Tracks()[i].Cast() for i in range(len(b.Tracks()))]:
            item.SetNet(nets['A'])
            if case=='class-width-valid':item.SetWidth(pcb.FromMM(.8))
        if case.startswith('class-width'):
            c['netclasses']=[{'name':'Power','nets':['A'],'clearance':.2,'track_width':.6}]
        for ref,net,x,y in [('J1','A',5,5),('J2','B',35,35)]:
            fp=pcb.FOOTPRINT(b);fp.SetReference(ref);fp.SetPosition(pcb.VECTOR2I(pcb.FromMM(x),pcb.FromMM(y)))
            pad=pcb.PAD(fp);pad.SetNumber('1');pad.SetShape(pcb.PAD_SHAPE_CIRCLE);pad.SetAttribute(pcb.PAD_ATTRIB_SMD)
            pad.SetPosition(fp.GetPosition());pad.SetSize(pcb.VECTOR2I(pcb.FromMM(1),pcb.FromMM(1)))
            layers=pcb.LSET();layers.AddLayer(pcb.F_Cu);pad.SetLayerSet(layers);pad.SetNet(nets[net]);fp.Add(pad);b.Add(fp)
        if case.startswith('via'):
            via=pcb.PCB_VIA(b);via.SetPosition(pcb.VECTOR2I(pcb.FromMM(25),pcb.FromMM(25)));via.SetLayerPair(pcb.F_Cu,pcb.B_Cu)
            via.SetWidth(pcb.FromMM(1.2));via.SetDrill(pcb.FromMM(.6));via.SetNet(nets['A']);b.Add(via)
        if case.startswith('zone'):
            zone=pcb.ZONE(b);zone.SetLayer(pcb.F_Cu);zone.SetNet(nets['B']);zone.SetLocalClearance(pcb.FromMM(.2));zone.SetMinThickness(pcb.FromMM(.2))
            poly=zone.Outline();poly.NewOutline()
            for x,y in [(16,16),(24,16),(24,24),(16,24)]:poly.Append(pcb.FromMM(x),pcb.FromMM(y))
            zone.SetIslandRemovalMode(pcb.ISLAND_REMOVAL_MODE_NEVER);b.Add(zone)
        pro=(folder/'board.kicad_pro').read_bytes();pcb.SaveBoard(str(folder/'board.kicad_pcb'),b);(folder/'board.kicad_pro').write_bytes(pro)
        areas=[area]
        if case=='exception-other-area':
            second=fixture.area();second['id']='SECOND';areas.append(second)
        fixture.install(folder,c,areas);rules.write(folder/'hardware.json',c)
        before=(folder/'board.kicad_pcb').read_bytes();plan=rules.configure(folder,c)
        record('spatial '+case+' preview read-only',not plan['conflicts'] and (folder/'board.kicad_pcb').read_bytes()==before,plan['conflicts'])
        transaction=rules.configure(folder,c,apply_plan=plan['id'])
        _,_,values=rules.resolve(c);settings=rules.project_settings('board',values,c.get('netclasses',[]))['net_settings']
        verified=spatial.verify(folder,c,values,settings)
        record('spatial '+case+' saved geometry and consumer inputs',verified['passed'],verified['errors'])
        result_path=folder/'spatial-drc.json'
        tool=rules.run_tool(cli,['pcb','drc','--format','json','--severity-all','--refill-zones','-o',str(result_path),str(folder/'board.kicad_pcb')],folder)
        findings=rules.violations(rules.read(result_path)) if result_path.is_file() else []
        kinds={f.get('type') for f in findings}
        record('spatial DRC '+case,tool['exit_code']==0 and ('items_not_allowed' in kinds)==expected,sorted(str(x) for x in kinds))
        if case.startswith('class-width'):
            record('spatial shared netclass width '+case,('track_width' in kinds)==(case=='class-width'),sorted(str(x) for x in kinds))
        if case=='outside':
            svg=ET.parse(folder/'.work/spatial-preview.svg').getroot()
            record('spatial preview includes footprint envelopes and pads',len(svg.findall('{http://www.w3.org/2000/svg}circle'))==2 and 'J1' in ''.join(svg.itertext()))
            consumer=folder/spatial.CONSUMERS['routing'];saved=consumer.read_bytes()
            divergent=json.loads(saved);divergent['constraints']['minimums_mm']['track_width']+=.1
            rules.write(consumer,divergent)
            failed=spatial.verify(folder,c,values,settings)
            record('spatial divergent routing versus DRC refused',not failed['passed'] and any('routing consumer' in e for e in failed['errors']))
            consumer.write_bytes(saved)
            preview=rules.configure(folder,c)
            document=rules.read(folder/'spatial-constraints.json');document['revision']='changed';rules.write(folder/'spatial-constraints.json',document)
            try:rules.configure(folder,c,apply_plan=preview['id']);refused=False
            except ValueError:refused=True
            record('spatial stale preview refused',refused)
            document['revision']='fixture-1';rules.write(folder/'spatial-constraints.json',document)
            restored=rules.configure(folder,c)
            record('spatial repeat configure preserves PCB bytes',not restored['conflicts'] and rules.configure(folder,c,apply_plan=restored['id']) is None)
            saved=(folder/'board.kicad_pcb').read_bytes();pro=(folder/'board.kicad_pro').read_bytes()
            altered=pcb.LoadBoard(str(folder/'board.kicad_pcb'))
            for i in range(len(altered.Zones())):
                if altered.Zones()[i].GetZoneName()=='HW-SPATIAL-QUIET':altered.Zones()[i].Move(pcb.VECTOR2I(pcb.FromMM(1),0))
            pcb.SaveBoard(str(folder/'board.kicad_pcb'),altered);(folder/'board.kicad_pro').write_bytes(pro)
            failed=spatial.verify(folder,c,values,settings)
            record('spatial moved protective area fails verification',not failed['passed'] and any('geometry' in x for x in failed['errors']))
            changed=(folder/'board.kicad_pcb').read_bytes();refused=rules.configure(folder,c)
            record('spatial mismatched area adoption preserves source',bool(refused['conflicts']) and (folder/'board.kicad_pcb').read_bytes()==changed)
            (folder/'board.kicad_pcb').write_bytes(saved)
        if case=='track':
            applied=(folder/'board.kicad_pcb').read_bytes()
            rules.configuration.rollback(folder,transaction)
            record('spatial transaction rollback restores original PCB',before==(folder/'board.kicad_pcb').read_bytes() and applied!=before)


if __name__=='__main__':
    import integration as base
    run(base.WORK,base.board,base.schematic,base.compose,base.record)
    rules.write(base.ROOT/'.work/spatial-smoke.json',base.RESULTS)
    raise SystemExit(0 if all(x['passed'] for x in base.RESULTS) else 1)

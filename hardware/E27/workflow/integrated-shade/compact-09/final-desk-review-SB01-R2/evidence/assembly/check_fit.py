from pathlib import Path
import json,math,hashlib,itertools
H=Path(__file__).resolve().parent; ROOT=H.parents[2]; P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
n=json.loads((H/'native-inventory.json').read_text(encoding='utf-8')); native={r['ref']:r for r in n['rows']}
assert sha(P/'SC09_compact.kicad_pcb')==n['source_board_sha256'],'PCB changed: rerun native inventory and review'
# Geometry uses exact manufacturer maxima where stated. Axial forming is a project process envelope.
# U1 basic dimensions are conservatively enlarged; R6 uses manufacturer family dimensional tolerance.
data=[
('BR1','MB10S-13',[-2.475,-2.05,2.475,2.05],2.9,None,'Diodes_MB10S','Bottom. Match positive pin1 BUS_RECT, negative pin3 DC_RETURN, AC pins2/4; never mirror polarity from a top-view image.'),
('C1','R76QI24705050J',[-9.25,-3.85,9.25,3.85],14.1,.85,'KEMET_R76','Nonpolar P15+/-0.4. Body max18.5x7.7x13.6; add0.5 engineering seating allowance. Form leads gently without force on epoxy; 24mm minimum lead length sufficient.'),
('C4','B32671P6154K000',[-6.5,-3,6.5,3],12.5,.65,'TDK_C4','Nonpolar P10+/-0.4, max13x6x12, project0.5 stand-off. Slight pitch correction may be needed.'),
('C5','CL21B475KAFNNNE',[-1.05,-.675,1.05,.675],1.35,None,'Samsung_C5','Bottom nonpolar0805. Pad1x1.5 at+/-1.0 is engineering selection; control solder volume and thermal shock.'),
('C6','EEUFS2A151',[4,-6.5,26,6.5],13.5,.65,'Panasonic_FS','Horizontal; plus pin1 LED_PLUS, stripe/minus pin2 DC_RETURN. D12.5+/-0.5,L20+/-2,P5+/-0.5,d0.6+/-0.05. Support can0.5 abovePCB; seal plane localX4, axis+X, ventX26. Preserve2.5 straight lead before1.5 centreline bend. Do not grip/force seal. Keep vent5mm free in3D and support without covering vent. Sleeve is not an electrical barrier.'),
('D1','US1M-13-F',[-2.3,-1.46,2.3,1.46],2.4,None,'Diodes_US1M','Bottom SMA. Cathode band to pin1 FB_INDUCTOR, anode pin2 DC_RETURN. Exact recommended2.5x1.7 lands pitch4.'),
('L1','PR02FS0201000KR500',[-4.4519,-1.95,2.9169,1.95],16,.83,'Vishay_PR02FS','Legacy refL1 is100ohm2W PR02-FS resistor, not choke. Upright body over pad1BUS_RECT. Pad pitch5.0038; bodyDmax3.9,Lbody10,totalterminal12. Preserve2mm stand-off and2mm topforming budget. Return lead to pin2BUS_FILTERED; sleeve return wire if needed to prevent accidental contact, without relying on sleeve for a new safety barrier. Inspect actual formed envelope.'),
('R4','ERJ-6ENF1242V',[-1.05,-.675,1.05,.675],.65,None,'Panasonic_R4','Bottom nonpolar0805; pads1.1x1.4 at+/-1.15 are project choice within generic manufacturer land range.'),
('R5','RL1206FR-7W0R68L',[-1.6,-.85,1.6,.85],.65,None,'Yageo_R5','Bottom nonpolar current-sense1206. Exact manufacturer body3.1+/-0.1x1.6+/-0.1x0.55+/-0.1. Retainedland pattern; inspect wetting.'),
('R6','1206S4F365KT5E',[-1.625,-.85,1.625,.85],.65,None,'Royalohm_1206','Bottom nonpolar1206. Family dimensional max3.25x1.70x0.65. Retained1206 manual-prototype lands, not claimed exact Royalohm recommended land. Inspect termination overlap and solder sample.'),
('R7','HVR2500003903FR500',[-1.25,-1.25,1.25,1.25],11.5,.63,'Vishay_HVR25','Upright P4.8. BodyD2.5,L2total7.5max. Seat0.5, keep2mm straight abovebody before projectR1 bend. Engineering11.5 topenvelope; no vendor-qualified bend-radius assertion.'),
('R8','RC1206FR-0768KL',[-1.6,-.85,1.6,.85],.65,None,'Yageo_R8','Bottom nonpolar1206, max3.2x1.7x0.65. Retainedmanufacturer1206 lands; manual process inspection.'),
('R9','RC1206FR-0768KL',[-1.6,-.85,1.6,.85],.65,None,'Yageo_R8','Same asR8; second68kohm bleeder, do not omit.'),
('RF1','FW20A47R0JA',[-3,-3,3,3],14.85,.70,'Bourns_FW','Upright P6.8, FW20A bodyD6,L12max, lead.65+/-0.05. Seat0.5; topstraight1,bendcentreR1,wireR.35 gives14.85 engineeringtopbudget. Nonpolar; do not replace by ordinary nonfusible resistor.'),
('RV1','B72207S0271K101',[-2.2,-4.5,2.2,4.5],11.5,.65,'TDK_RV1','Nonpolar straightP5+/-1 leads, discplanealongY, max4.4x9x11body. Project0.5 seating budget; gently form pitch with leads supported, do not force disc.'),
('T1','7687709152',[-6.25,-6.25,6.25,6.25],10.5,None,'Wurth_T1','WE-PD HV SIZE1210, NOT1280. Max12.5squarex10.5. Native5.4x2.9 lands pitch9.9 match manufacturer drawing. Marking/pin1 toLED_PLUS, pin2FB_INDUCTOR; no polarity-sensitive winding claim. No custom winding.'),
('U1','LYT1603D',[-2.05,-2.55,2.05,2.55],1.75,None,'PI_U1','Bottom SO8D08A. Body3.9x4.9 BASIC, enlarged to4.1x5.1 for contour screen, not claimed guaranteed package maximum. Maxheight1.75. Pin1BP,2M,3FB,4DRAIN,5-8SOURCE. Use pin1 marker and actual native netmap; packageviewmirrored onB.')]
rows=[]
for ref,mpn,box,height,lead,source,note in data:
 r=native[ref]; assert r['MPN']==mpn,(ref,r['MPN'],mpn)
 a=math.radians(r['orientation_deg']);c=math.cos(a);s=math.sin(a);x,y=r['xy_mm']
 pts=[(x+u*c+v*s,y-u*s+v*c) for u,v in itertools.product([box[0],box[2]],[box[1],box[3]])]
 glob=[round(min(p[0]for p in pts),5),round(min(p[1]for p in pts),5),round(max(p[0]for p in pts),5),round(max(p[1]for p in pts),5)]
 q=dict(ref=ref,MPN=mpn,side=r['side'],xy_mm=r['xy_mm'],orientation_deg=r['orientation_deg'],local_max_or_planning_bbox_mm=box,global_bbox_mm=glob,top_from_mounting_face_mm=height,source_id=source,assembly_note=note,pads=r['pads'])
 if lead:
  drill=min(p['drill_mm'][0]for p in r['pads']);q['hole_check']={'nominal_finished_hole_mm':drill,'JLC_negative_tolerance_mm':.08,'minimum_finished_hole_mm':round(drill-.08,4),'maximum_round_lead_mm':lead,'minimum_diametral_clearance_mm':round(drill-.08-lead,4),'minimum_radial_clearance_mm':round((drill-.08-lead)/2,4)}
 rows.append(q)
assert len(rows)==17 and len(native)==19
pairs=[]
for a,b in itertools.combinations(rows,2):
 if a['side']!=b['side']:continue
 aa=a['global_bbox_mm'];bb=b['global_bbox_mm'];dx=max(aa[0]-bb[2],bb[0]-aa[2],0);dy=max(aa[1]-bb[3],bb[1]-aa[3],0)
 if dx==dy==0: pairs.append({'a':a['ref'],'b':b['ref'],'bbox_overlap':True})
 else:pairs.append({'a':a['ref'],'b':b['ref'],'mechanical_bbox_gap_mm':round(math.hypot(dx,dy),5)})
collisions=[r for r in pairs if r.get('bbox_overlap')]
assert not collisions,collisions
contract={'revision':'SB01-R2 final assembly desk review','actor':'/root/r2_assembly_fit','source_board_sha256':n['source_board_sha256'],'method':'Read-only native inventory plus independently transformed source dimensional envelopes. Not a physical measurement or product release.','no_new_preorder_physical_incompatibility_identified':True,'electronic_parts':rows,'wire_ports':[native['J1'],native['J2']],'height':{'F_top_planning_mm':16,'PCB_nominal_mm':1.6,'B_package_max_mm':2.9,'nominal_PCB_stack_planning_mm':20.5,'PCB_max_at_10percent_mm':1.76,'stack_with_max_PCB_before_forming_process_variation_mm':20.66,'original_20mm_target_met':False,'through_hole_lead_and_solder_projection_limit_below_PCB_mm':1.5,'notes':'20.5 is a planning envelope with nominalPCB, not measured or unconditional maximum. Reserve21mm only as preliminary handling clearance; actual assembly gauge required. No enclosure is selected.'},'C6_exact_case':{'MPN':'EEUFS2A151','not_MPN':'EEUFS2A151L','nominal_D_L_mm':[12.5,20],'maximum_D_L_mm':[13,22],'ripple_mA_rms_100kHz_105C':1400,'frequency_factors_47_330uF':{'60Hz':.6,'120Hz':.7,'1kHz':.85,'10kHz':.95,'100kHz':1},'vent_free_mm':5,'vent_global_Y_mm':100,'free_corridor_to_global_Y_mm':95},'wire_port_process':'J1/J2 are solder lands, no connector body. Use separately insulated mains leads and LED pair; strain relief on insulated support outside PCB; route away from resistorbody and C6vent; no stripped wire whiskers. Verify polarity using actual pad nets. Do not count external wire loops in20.5mm boardstack.'}
(H/'assembly-contract.json').write_text(json.dumps(contract,indent=2)+'\n',encoding='utf-8')
(H/'fit-calculations.json').write_text(json.dumps({'same_face_bbox_collisions':collisions,'pairs':pairs,'hole_position_tolerance_note':'JLC hole position +/-0.075mm; pitch forming must use actual board, not forced nominal jig. Diametral clearance is not automatic raw-pitch fit.','nominal_mechanical_not_electrical_clearances':{'C6_T1':1.0,'R7_C1':1.1,'C1_C4':2.7,'L1_body_edge':.6481,'C1_right_edge':.75,'RF1_bottom_edge':1.0,'L1_body_to_virtual_courtyard':.1981}},indent=2)+'\n',encoding='utf-8')
files=['SC09_compact.kicad_pcb','SC09_compact.kicad_sch','bom-build.json','footprint-geometry.json','spatial-constraints.json','thermal-planning.json']
(H/'canonical-input-hashes.json').write_text(json.dumps({x:sha(P/x)for x in files},indent=2)+'\n',encoding='utf-8')
print(json.dumps({'electronic_parts':len(rows),'wireports':2,'same_face_bbox_collisions':len(collisions),'height_planning_mm':20.5,'stack_PCBmax_mm':20.66,'minimum_hole_diametral_clearances':{r['ref']:r['hole_check']['minimum_diametral_clearance_mm'] for r in rows if'hole_check'in r}},indent=2))

from pathlib import Path
import json,hashlib
H=Path(__file__).resolve().parent;ROOT=H.parents[2];P=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';c=json.loads((H/'assembly-contract.json').read_text(encoding='utf-8'))
sources={
'Diodes_MB10S':('https://www.diodes.com/datasheet/download/MB10S.pdf',None,'DS39045Rev3-2p4; manufacturer MB package and landdrawing'),
'Diodes_US1M':('https://www.diodes.com/datasheet/download/US1M.pdf',None,'DS16008Rev11-2p4; SMA package and recommendedlands'),
'KEMET_R76':('https://www.tme.eu/Document/54c856efb555c0dc609ed279e406baf5/R76QI24705050J.pdf',None,'KEMET manufacturer-authored exactMPN sheet mirrored by supplier'),
'TDK_C4':('https://product.tdk.com/en/search/capacitor/film/snubbering_pfc/info?part_no=B32671P6154K000',None,'Exactproduct plus B3267P family drawing P10+/-0.4,d0.6+/-0.05'),
'Samsung_C5':('https://product.samsungsem.com/mlcc/CL21B475KAFNNN.do',None,'Exactmanufacturer0805CL21B475KAFNNNE dimensionaldata'),
'Panasonic_FS':('https://industrial.panasonic.cn/cdbs/www-data/pdf/RDF0000/ABA0000C1257.pdf','work/sc09-spacing23/research/Panasonic-FS-primary.pdf','Actual capturedFS-A2025/9/1p5 exactEEUFS2A151 visually read; p1 dimensions/frequency also visually read. Official capturedURL; localcapturedPDFhash governs.'),
'Vishay_PR02FS':('https://www.vishay.com/docs/28915/pr02fs.pdf','work/sc09-sb01-startup-improvement/startup/PR02FS-primary.pdf','Rev22Oct2024 exactcoding and dimensions; axialforming is project choice'),
'Panasonic_R4':('https://industrial.panasonic.com/ww/products/pt/general-purpose-chip-resistors/models/ERJ6ENF1242V',None,'Exactmanufacturerpart; generic ERJ familylandrange'),
'Yageo_R5':('https://www.yageo.com/en/ProductSearch/PartNumberSearch', 'work/compact09/capture-passive/yageo-R5.pdf','Manufacturer-generated exactMPN sheet; original suppliersearchURL not directPDF'),
'Yageo_R8':('https://www.yageo.com/en/ProductSearch/PartNumberSearch','work/compact09/capture-passive/yageo-R8.pdf','Manufacturer-generated exactMPN sheet'),
'Royalohm_1206':('https://robu-prod-media.s3.ap-south-1.amazonaws.com/uploads/2024/12/royal-ohm-smd-res-datasheet-3.pdf','work/sc09-sb01-r2-final/assembly/Royalohm-manufacturer-1206.pdf','Royalohm-authored ThickFilmChipResistors catalogue pp3-4 hostedmirror. OrderingcodeS4/F/365K/T5E and1206 dimensions visually confirmed; officialdirectPDF unavailable, no vendorlandclaim.'),
'Vishay_HVR25':('https://www.vishay.com/docs/30260/hvr2537.pdf','work/sc09-spacing23/research/HVR25-primary.pdf','HVR25 dimensionaltable L1/L2/D/d'),
'Bourns_FW':('https://www.bourns.com/docs/product-datasheets/fw.pdf','work/compact09/footprint-basis/addendum-fw.pdf','FW20A specificrow; lead.65+/-0.05, notFW30A lead.75'),
'TDK_RV1':('https://product.tdk.com/en/search/protection/voltage/lead-disk-varistor/info?part_no=B72207S0271K101',None,'Exactmanufacturerpart dimensionsP5+/-1,d.6+/-0.05,max9x4.4x11'),
'Wurth_T1':('https://www.we-online.com/components/products/datasheet/7687709152.pdf','work/sc09-simple/t1/7687709152-mfr-mirror.pdf','Manufacturer Rev001.003 Size1210 andland12.8span/9.9pitch/5.4x2.9pads'),
'PI_U1':('https://www.power.com/sites/default/files/documents/lytswitch-1_family_datasheet.pdf','work/compact09/rdr-research/lytswitch-1_family_datasheet.pdf','RevB07/16p11 D08A BASICdimensions andmaxheight1.75; no literal3.9x4.9maximumclaim'),
'JLC_tolerance':('https://jlcpcb.com/capabilities/pcb-capabilities',None,'Read2026-11-24: finishedholes+0.13/-.08, position+/-0.075, PCB>=1mmthickness+/-10%')}
out={}
for k,(u,p,note)in sources.items():
 q={'url':u,'note':note,'primary_authorship':True}
 if p and (ROOT/p).exists():q.update(local_file=p,sha256=hashlib.sha256((ROOT/p).read_bytes()).hexdigest())
 out[k]=q
(H/'sources.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
patch={}
for r in c['electronic_parts']:
 q={'assembly_dimension_basis':r['source_id'],'assembly_note':r['assembly_note'],'planned_max_from_mounting_face_mm':r['top_from_mounting_face_mm']}
 if r['ref']=='U1':q['engineering_contour_screen_bbox_mm']=r['local_max_or_planning_bbox_mm'];q['body_basic_LW_mm']=[3.9,4.9]
 else:q['max_body_or_formed_envelope_bbox_xy_mm']=r['local_max_or_planning_bbox_mm']
 if'hole_check'in r:q['hole_fit_screen']=r['hole_check']
 patch[r['ref']]=q
patch['J1']={'description':'ActualnativeBpad1AC_L148.4,130;pad2AC_N148.4,124.5; pitch5.5; no connectorbody.'}
patch['J2']={'description':'ActualnativeBpad1LED_PLUS101.6,124.5;pad2DC_RETURN101.6,130; pitch5.5; no connectorbody.'}
(H/'proposed-geometry-row-addenda.json').write_text(json.dumps(patch,indent=2)+'\n',encoding='utf-8')


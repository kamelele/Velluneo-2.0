from pathlib import Path
import hashlib,json
ROOT=Path(__file__).resolve().parents[2];S=ROOT/'work/Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact';p=S/'SC09_compact.kicad_sch';old=p.read_bytes();s=old.decode()
edits=[('230 VAC / 50 Hz | 207-253 V screen | nominal 135 mA / 60 V / 8.1 W | 4000 K, CRI >=80','230 VAC / 50 Hz | 207-253 V screen | total ~135 mA, LED ~133 mA / 60 V / ~8 W LED | 4000 K, CRI >=80'),('R5 || R6 = 0.57321 ohm. Nominal LED current = (0.279 / 0.57321) / 3.6 = 135.2 mA; actual corners unmeasured.','R5 || R6 = 0.57321 ohm. Estimated total = 135.2 mA; LED ~133.4 mA at 60 V after bleeders; actual corners unmeasured.')]
for a,b in edits:assert s.count(a)==1;s=s.replace(a,b)
p.write_text(s,encoding='utf-8');(ROOT/'work/compact09/order-closure/schematic-note-correction.json').write_text(json.dumps({'before_sha256':hashlib.sha256(old).hexdigest(),'after_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'edits':'Two display notes only; symbols,pins,wires,netlabels,MPNsunchanged. FreshERC/connectivity/parityrequired.'},indent=2)+'\n')
print('Schematic notes corrected; no graph edit')

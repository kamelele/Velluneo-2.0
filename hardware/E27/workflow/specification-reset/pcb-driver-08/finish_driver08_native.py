from pathlib import Path
import pcbnew,json,hashlib,sys
W=next(p for p in Path(__file__).resolve().parents if (p/'Velluneo-readiness').is_dir());D=W/'Velluneo-readiness/hardware/E27/workflow/specification-reset/pcb-driver-08';E=D/'design';P=E/'Velluneo_driver.kicad_pcb'
raw=P.read_text();pro=P.with_suffix('.kicad_pro').read_bytes()
if '(stackup' not in raw:
 stack='''
        (stackup
            (layer "F.Cu" (type "copper") (thickness 0.035))
            (layer "dielectric 1" (type "prepreg") (thickness 0.2104) (material "7628"))
            (layer "In1.Cu" (type "copper") (thickness 0.0152))
            (layer "dielectric 2" (type "core") (thickness 1.065) (material "FR4"))
            (layer "In2.Cu" (type "copper") (thickness 0.0152))
            (layer "dielectric 3" (type "prepreg") (thickness 0.2104) (material "7628"))
            (layer "B.Cu" (type "copper") (thickness 0.035))
            (copper_finish "ENIG")
            (dielectric_constraints no)
        )
'''
 raw=raw.replace('\t(setup\n','\t(setup\n'+stack,1);P.write_text(raw)
b=pcbnew.LoadBoard(str(P));b.GetDesignSettings().SetAuxOrigin(pcbnew.VECTOR2I(pcbnew.FromMM(77.5),pcbnew.FromMM(130)))
for t in b.GetDrawings():
 if isinstance(t,pcbnew.PCB_TEXT) and t.GetText().startswith('RETURN06'):
  t.SetText('VELLUNEO DRIVER08 / 4 LAYERS / ROUTED CAD / PROTOTYPE')
for t in b.GetTracks():
 if isinstance(t,pcbnew.PCB_VIA):
  t.SetFillingMode(pcbnew.FILLING_MODE_FILLED);t.SetCappingMode(pcbnew.CAPPING_MODE_CAPPED)
pcbnew.SaveBoard(str(P),b);P.with_suffix('.kicad_pro').write_bytes(pro)
assert '(stackup' in P.read_text();print('Updated stackup, matched output origin, explicit per-via fill/cap and current board annotation')

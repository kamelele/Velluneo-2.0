from pathlib import Path
import shutil
HERE=Path(__file__).resolve().parent;S=HERE/'project';shutil.copy2(HERE/'routing/SC09_compact.kicad_pcb',S/'SC09_compact.kicad_pcb');(S/'.work').mkdir(exist_ok=True)
t=(HERE.parent/'thermal_guards.py').read_text();t=t.replace("S=root.parent/'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC09_compact'","S=root/'project'").replace("root/'spacing-thermal/spacing-contract.proposed.json'","root/'spacing-matrix.CAT01.json'").replace("root/'checker/root-lab-functional-assessment-v5.json'","root/'package-assessment.CAT01.json'").replace("root/'grid_expanded.py'","root/'grid_stock.py'")
(HERE/'thermal_stock.py').write_text(t)
print('Private thermal construction prepared; sameHV55matrix, freshguardsfromactualstockpads')

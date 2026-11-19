"""Reproduce SC07-C IDEAL-SOURCE trim experiment; NOT a model of new SC08 input RC.

Writes only alongside this script. Reads frozen SC07 model functions, never executes
their file-writing/report-generation tail. No hardware measurements or full-temp bounds.
"""
from pathlib import Path
import hashlib
import itertools
import json
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / 'Velluneo-2.0/hardware/E27/variants/integrated-shade/SC07_protection/studies/coupled_output.py'
EXPECTED_SHA = 'f364fabc8c75c5547e22d09057c856f5eed29e9dbd3b79fe6a0dd8767bb6345d'
raw = SOURCE.read_bytes()
actual_sha = hashlib.sha256(raw).hexdigest()
if actual_sha != EXPECTED_SHA:
    raise SystemExit('SC07 model changed; review new input before running: ' + actual_sha)
source_text = raw.decode('utf-8')
namespace = {'__file__': str(SOURCE)}
exec(compile(source_text[:source_text.index('\ncases=[]')], 'frozen_SC07_functions_only', 'exec'), namespace)
simulate = namespace['simulate']
results = []
for rled, high, inductance in itertools.product([470 * .95 * .97, 470 * 1.05 * 1.03], [False, True], [.0024, .0033]):
    conditions = dict(Rled=rled, L=inductance, vth=1.76 if high else 1.54,
                      ilim=.504 if high else .350, f=70000. if high else 62000.,
                      tmin=.675e-6, leak=.00145)
    low, upper = 23., 33.
    for _ in range(7):
        middle = (low + upper) / 2
        measured_by_model = simulate(Rs=middle, vac=230., duration=2., **conditions)['steady']['LEDavg']
        if measured_by_model > .055:
            low = middle
        else:
            upper = middle
    chosen = (low + upper) / 2
    checks = [simulate(Rs=chosen, vac=vac, duration=2., **conditions)['steady']['LEDavg'] * 1000
              for vac in [207., 230., 253.]]
    results.append(dict(Rled=rled, high=high, L=inductance, trim_R=chosen, LED_mA=checks))
report = dict(
    kind='Actually executed own SC07-C ideal-source numerical sensitivity; not SC08 input-RC simulation or measurement',
    source_path=str(SOURCE), source_sha256=actual_sha,
    method='Each fixed illustrative unit individually trimmed at230VAC,seven bisection iterations on23..33ohm;2s runs,final1s reporting;fixedR then checked207/230/253VAC',
    conditions='Existing SC07 model: ideal rectified source, fixed84.5VLED,120uF output,22uF feedback,5070ohm auxiliary,12.15V rail; no actual input pi/RC,OVP,relay,loss/nonlinear/hot model',
    limitation='Different controller values are illustrative fixed units, not a guaranteed hot envelope. Continuous trim is a study, not actual E96 population or calibration measurements. Numerical discontinuities do not justify precise physical trim resistance.',
    cases=results,
    summary=dict(trim_ohm_range=[min(c['trim_R'] for c in results), max(c['trim_R'] for c in results)],
                 post_trim_LED_mA_range=[min(v for c in results for v in c['LED_mA']), max(v for c in results for v in c['LED_mA'])]))
(HERE / 'trim-results.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report['summary']))

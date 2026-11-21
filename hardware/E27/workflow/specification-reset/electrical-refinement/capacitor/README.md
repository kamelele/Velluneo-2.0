# Bulk capacitor RMS refinement

The existing **Rubycon450BXW15MEFR10X20 (15µF/450V)** remains the prototype candidate. This conditional calculation provides no CAD/value change and does not close full ripple, temperature, lifetime or controller qualification.

## Evidence scope

This packet has **64 new switched-load endpoint cases**, with200ns/100ns numerical refinement and a worst-case current waveform/spectrum. The separate **1152 historical cases** in `../../electrical-integration/input-corners-results.json` are averaged bridge/bulk cases; they are inputs to the analytical comparison, not1152 switching-controller simulations. Neither set is a native UCC28711 model or a continuous-envelope proof.

New actual model maximum bulk RMS is0.1271347701A. The RSS bound of its separate nonnegative bridge/draw RMS maxima is0.1401453104A. The exact KCL cross term is retained in the direct waveform integration; RSS conservatism follows from signs, not independence. Positive clamp return introduces a positive bridge/return cross and requires additional bounds that also remain valid after it changes bridge conduction.

The model schedules11W remaining primary/bulk pulse energy **plus explicit bleeder/input losses**, not11W wall input. A finite nonsynchronous observation can show11.001878W primary mean. Its imposed peak and energy determine67.533–82.540kHz; independent unrelated peak/frequency/power maxima are not silently combined. Clamp return, real auxiliary/direct-HV dynamics, ESR/aging, input inductance, bridge HF and parasitic currents remain outside the model.

## Native rating comparison

Native BXW exact row:0.190Arms at120Hz/105°C and0.475A at100kHz. For10–82µF, native frequency coefficients are:

| Frequency | Coefficient |
|---|---:|
| 50/60Hz | .80 |
| 120Hz | 1.00 |
| 500Hz | 1.30 |
| 1kHz | 1.50 |
| 10kHz | 2.10 |
| ≥100kHz | 2.50 |

The severe all-band50Hz **comparison** is0.152A. The modeled waveform is below it. This does not invent a manufacturer-approved composite-spectrum formula, interpolation, operating temperature or lifetime acceptance. The old loose~0.2006A triangle alone does not demonstrate that15µF must be replaced by22µF.

## Files and reproduction

- `handoff.md`: detailed mathematics, waveform conditions, findings and remaining inputs.
- `model.cpp` / `calculate.py`: event-resolved numerical model and64-case sweep.
- `results.json`: full64-case output and full-window spectrum/RMS/Parseval. `waveform-record.json` preserves the exact full generatedwaveform SHA256/bytecount/samplecount. The34MB rawCSV is reproducible intermediate output, not versioned. `waveform-preview.csv` is only the first2000 originalsample rows; it is not used for whole-window numerical checks. `calculate.py --output-dir /external/output` regenerates the full uniform100ns rawwave.csv.
- `bounds.py` / `bounds-results.json`: sign-based KCL and explicitly conditional analytical budgets using the pinned historical averaged data.
- `sources.json`: exact native/historical source hashes and original URLs; native PDF is not redistributed.
- `original-handoff-hashes.json`: original temporary handoff artifact identities; `integration-verification.json` and `implementer-artifact-hashes.json`: original integrated reproduction evidence (including the reproduced fullCSV hash). `artifact-hashes.json`: coordinator-packaged currentfiles after replacing that reproducible fullCSV with a small exactprefix and rawidentity record.

Download the native BXW PDF externally from the URL in `sources.json`, and retain the exact recorded bytes/hash. From any working directory:

```sh
python /path/to/capacitor/calculate.py --bulk-pdf /external/source/BXW.pdf
python /path/to/capacitor/bounds.py
```

The model requires Python, NumPy andg++; it compiles into a temporary directory outside the repository and removes that executable when done. `--output-dir /external/output` sends numerical results/waveform elsewhere. The analytical script accepts `--historical-results`, `--switched-results` and `--output`; defaults resolve from the script/project directory, not the caller's working directory. Both native PDF and historical averaged-results hashes are checked; changed inputs require review rather than bypassing a mismatch.

No vendor PDF, compiled binary, PCB edit, measurement, reviewer approval or component substitution is included.

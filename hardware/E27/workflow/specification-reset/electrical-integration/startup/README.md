# Startup source witness and analytical checks

This packet integrates ELEC-CLOSE-01 without changing the schematic, physical pin graph or selected components. It adds a primary-source correction and preserves reproducible conditional calculations. It does **not** establish a successful controller transient, physical startup, independent review or finding closure.

TI SLUAAC5 p5 describes three initial sampling pulses at the controller's maximum switching frequency. This corrects the earlier statement that no source describes their frequency. The report covers UCC28711 among related controllers but uses UCC28704 examples and cautions that parameters differ. It does not provide a complete corner-certified startup latency/current envelope. TI SLUA783 p5 supplies a UCC2871x first-on-time fault screen of `1/fSW(max)`.

The integrated calculations reproduce the original results:

| Calculation | Conditional result |
|---|---|
| Current r12 ramp sensitivity | 128 cases; stress acquisition allowance 0.429348 ms |
| Three-period source-cadence witness | Worst VDD 11.55965 V under the existing assumptions |
| Optional 1 MΩ RVDD ECO, not folded into baseline | Worst VDD 11.49376 V under that same witness |
| Residual-current hybrid diagnostic | 768 cases; maximum primary peak 0.242097 A and flux proxy 0.079820 T |

The hybrid diagnostic includes residual current, leading-edge blanking and assumed delay. It demonstrates compatibility of a constructed sampling sequence, not three fully reset DCM cycles or the actual TI state machine. The inherited gate charge, bias current over declining VDD, output charging, auxiliary transfer and settling assumptions still need a matched physical or appropriately qualified model trajectory. See [HANDOFF.md](HANDOFF.md) for the charge-domain condition, source conditions, optional ECO separation and exact omissions.

## Reproduce

Use Python with NumPy and SciPy. The calculations resolve repository inputs relative to the script location and therefore do not depend on the shell's working directory.

Vendor PDFs and rendered pages are **not** redistributed here. Supply the three original, hash-matched documents externally, using filenames `ucc2871x.pdf`, `sluaac5.pdf` and `slua783.pdf`. [sources.json](sources.json) records their official URLs, complete SHA-256 hashes, relevant pages and conditions. Changed publisher downloads are rejected rather than silently accepted.

From the repository root:

```bash
python hardware/E27/workflow/specification-reset/electrical-integration/startup/calculate.py --source-dir /absolute/path/to/native-pdfs
python hardware/E27/workflow/specification-reset/electrical-integration/startup/hybrid3.py
```

If the UCC PDF is stored separately, add `--ucc-pdf /absolute/path/to/ucc2871x.pdf` to the first command. The other two PDFs still come from `--source-dir`. Outputs are written beside the scripts.

## Records

- `results.json` and `rows.json`: summary and all 128 analytical ramp cases.
- `hybrid3-results.json`: 768-case hybrid summary, worst case and explicit omissions.
- `calculate.log` and `hybrid3.log`: actual successful integration reruns.
- `integration-check.json`: exact calculated-value comparison against the original diagnostic. All calculated values matched; only source-provenance metadata changed in `results.json`. The other two result files are byte-identical.
- `sources.json`: external primary-source register.
- `manifest.json`: integrated artifact hashes and original script provenance.

The optional RVDD result remains separately identified. Its integration here is not authorization to apply that ECO. No physical measurement, vendor-model fit, complete startup pass or CAD/graph change is claimed.

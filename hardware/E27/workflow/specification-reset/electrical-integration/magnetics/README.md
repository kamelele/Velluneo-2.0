# Transformer winding and window candidate

Retained candidate: TDK EFD25/13/9, 120:30:22 turns, primary/auxiliary ELEKTRISOLA P180 Cu0.180mm IEC Grade2 and secondary Furukawa TEX-E0.30mm. This directory preserves source-linked numerical work; it is not a released winding drawing or a physical-test report.

- `winding-proposal.md`: exact wire definitions, layer sequence, preserved dot/pin map, packing, DC resistance/loss and owned remaining inputs.
- `window-fit.md`: actual native bobbin/core solid comparison and separate drawing-dimension tolerance screen.
- `winding-results.json` / `window-results.json`: preserved original numerical results.
- `calculate.py` / `check-window.py`: runnable calculations, independent of the caller's working directory.
- `sources.json`: original source URLs, hashes and retrieval basis. Manufacturer PDFs, STEP, HTML and images are not redistributed.
- `verification.json`: integration rerun results; `artifact-hashes.json`: hashes of integrated text/code/results.

Both winding alternatives avoid intersections with the nominal native bobbin/core solids. The0.30mm wire construction has +0.207mm remaining side-dimension budget; the0.40mm alternative has −0.003mm. The latter therefore does not obtain tolerance support from its nominal fit. Retain0.30 as candidate; local centering, winding build, exits, yokes, process and insulation acceptance remain open. No geometric margin here is a selected insulation distance.

## Reproduce

From this directory, the winding arithmetic uses only the source-transcribed constants in code:

```sh
python calculate.py
```

Download the original bobbin/core STEP files using the official links recorded in `sources.json` into an external working directory. Compare their exact SHA256 values with the record. The collision script requires explicit external paths and refuses mismatched source bytes:

```sh
python check-window.py --bobbin-step /external/source/bobbin.step --core-step /external/source/core.step
```

Both scripts accept `--output /external/temp/result.json` to avoid overwriting the preserved results. Window analysis requires CadQuery/OCP; the integration environment executed it successfully. A different vendor file or geometry engine revision requires fresh evidence; do not bypass the source hash check to force a pass.

The source PDF URLs in `sources.json` permit independent inspection of wire, tape and native dimensions without copying vendor publications into this directory. Initial original analysis paths mentioned in the reports identify the source history, not required repository dependencies. These calculations exclude qualified AC/core losses, leakage, insulation certification, physical thermal behavior and fault survival. Laboratory measurements remain unperformed.

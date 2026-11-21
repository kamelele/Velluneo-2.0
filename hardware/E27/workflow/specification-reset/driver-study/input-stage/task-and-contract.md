# Input/rectifier and circuit-intent task contract

DRV-INPUT-01 / VEL-INPUT-01. Date2026-11-17. Coordinator/sole shared-file writer/root. Specification research, baseline draft9f4a3f94eb5fb35b525413d6a4058e9b5769d8f7. Productr11 blob6493b29bd33fbde1f3c61c5e995b11447cb83e9b remains authoritative, to refresh before integration. Requirements R-SUPPLY/R-FAULT/R-EMPTY/R-OFFLINE/R-THERMAL/R-BUILD/R-SIZE/R-BASE-LIFE/R-COMPAT. Allowed repository writes driver-study/input-stage/* and driver-study/README.md only. No CAD/configuration/library ownership or physical-pin connectivity approval.

Bounded implementation: compare10/15uF exact native bulk candidates with fixed47ohm input resistance, exact bridge/fuse/bleed references, diode/NTC source-conditioned arithmetic and consolidated functional connection intent. Keep partial BOM and missing physical/model/safety/process data explicit. Do not fit failed MOSFET model, relabel encrypted UCC28710 as28711, force a successful start or introduce a broad topology survey. Existing findings and all stage gates retain scope.

Bounded implementer/root/model_compatibility read native startup sources and independently collected candidate diode/NTC sources in isolated tmp folders. It changed no shared files and is not a reviewer or human approver. Unverified initial diode/thermistor identifiers were excluded; final supported references are recorded without inventing JLC availability.

## Reproduce

Python3/NumPy2.3.5; canonical prior engine is driver-study/primary-buffer/calculate.py, exact hash asserted. No original engine mutation on disk. Cases/global input arrays are replaced together in the imported module; remaining output/control assumptions are recorded.

```sh
python calculate.py --parent ../primary-buffer/calculate.py --verify-halved-step > /path/isolated-results.json
python secondary.py > /path/isolated-secondary-results.json
```

Both exit0 indicate numerical/arithmetic completion only. Expected288cases,15uF minimum bus259.047V, conservative mixed-band screen0.7704, no transient-controller/physical pass. --include-cases optionally emits full288case table for further examination; the published summary is reproducible without that flag. Previous10uF-only diagnostic output is not the final packet. During reviews use isolated outputs, preserve frozen inputs and compare JSON numerics/bytes. Native PDFs and old vendor models/fixtures are reference-only and not redistributed.

Acceptance is preliminary numerical/source consistency and honest circuit-intent consolidation, not complete zasilacz/schematic/manufacturing acceptance. Startup bias charge, hot clamp/SOA, surge/fault, actual sensor/thermal/insulation and assembly evidence remain open; no unavailable evidence is invented. Owner alone approves product stages. Model-specific majors do not prohibit other independent analytical work, but cannot be silently downgraded or called closed.

Four separate read-only final reviewers: Reality/root/spec_reality, Overengineering/root/spec_simplicity, Completeness/root/spec_completeness, Change/root/spec_change. Same frozen inputs or explicitly retained unchanged scope; no majority approval or fabricated independent human. Snapshot manifest/review/index are lifecycle metadata excluded from source hashes. No order, supplier message, account/license action, merge, physical test or generated schematic occurs.

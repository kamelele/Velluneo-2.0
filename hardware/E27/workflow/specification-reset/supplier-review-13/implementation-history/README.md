# Actual implementation history, not an automatic replay command

These are the scripts actually used from the original workspace work/ directory.
Their paths resolve relative to that directory and depend on the recorded local
KiCad/toolkit/runtime installations and the C11 baseline. Moving this archive
does not make those local dependencies portable. Use the distributed editable
engineering ZIP for the self-contained KiCad project.

Do not blindly execute the mutation history against the final design: start,
refine, tune and shift were sequential experimental corrections, not idempotent
generators. The initial two DRC probes intentionally exposed unresolved issues;
the final current reports supersede them. Adoption ran once using the actual
pinned preview/apply transaction. No historical source or cache was patched.

The final-state native audit, exports, negative controls and toolkit checks were
actually executed; reports/commands are retained under checks/. The independent
CAM parser required normal access to its local installed library. KiCad renders
required normal filesystem access to the local model files: the restricted
render invocation omitted models and was discarded after visual inspection.
The published renders were regenerated with model access and visually checked.

Runtime for pure Python: CodexPrimaryRuntime.v26-1119-907-0 bundled Python.
Native CAD: KiCad10.0.6 bin/python.exe and kicad-cli.exe. Source runtime_clamp.ps1
from the original workspace for native environment/Git mapping; its obsolete
PcbPy alias must not be used. The exact toolkit manifest is in the project index.
No physical measurement, accepted supplier drawing or standards certificate was
created by these calculations. Those supplier/qualification holds remain open.

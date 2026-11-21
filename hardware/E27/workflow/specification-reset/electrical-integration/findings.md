# Finding ledger — ELEC-CLOSE-01

Owner for design fixes:/root. Physical validation owner:Kamil/university lab with actual qualified setup/personnel to be established before tests. Status is design-preparation only.

| ID | Severity/status | Evidence and exact remaining action |
|---|---|---|
| ELEC-BLEED-001 | Major; correction proposed, unapplied | Existing1206 pair one-open path loss/one-short voltage excess. ECO-01 addresses specified single resistor fault with two2512 branches. Need actual graph decision/CAD capture, physical layout/common-point/rating/thermal and whole-assembly discharge verification; no closure yet. |
| ELEC-VDD-001 | Major evidence gap; correction proposed | No dedicated passive bias discharge path in existing graph. Optional1Mohm R13 adds bounded35.75uA to the stated bias calculation; complete service/takeover trajectory still unverified. |
| ELEC-FLUX-001 | Major; unresolved | Conditional current envelope and native typical curve exceed allowed flux ratio. Proposed bin/calibration approach must demonstrate all-corner behavior and interchangeability or require a tighter-regulation ECO. No threshold relaxation or production guarantee. |
| ELEC-CAP-001 | Major; linked RC-INPUT-001, unresolved | Averaged LF current does not establish full capacitor ripple. Conservative conditional triangle bound.2006A>.152A screen; no actual-failure inference. Establish bounded waveform spectrum/temperature or independently review a suitable capacitor/value change including inrush/lifetime/fit. |
| ELEC-MAG-001 | Major; unresolved finished construction | Winding0.30 candidate has actual nominal fit and only.207mm dimension-only margin; leadouts/tolerances/tape/source procurement/insulation remain. Propagate125°C resistance and actual AC/core/aux losses through control/thermal.0.40 candidate not selected. |
| SCH-ANN-001 | Existing native warning; numeric ECO proposed | Names lack numeric suffix. Native graph still matches accepted intent; zero enabled ERC findings does not clear annotation. Aliases proposed only, to be captured/rechecked after real decision. |
| RC-BIAS-001 | Existing major; retained | NewTI source cadence and residual-current hybrid model improve feasibility evidence only. Actual charge/gate/VS/CS/aux/startup/fault trajectory still needed. |
| RC-COMP-002 | Existing major; retained | Clamp source proxy≤696.5V against engineering700V leaves little margin and does not bound hot dynamic clamp/SOA/surge/fault. Actual validated model/waveforms required. |
| RC-MODEL-001 / RC-CTRL-MODEL-001 | Existing majors; retained | MOS gate/Coss and exact28711 state model domain not validated. Do not treat encrypted28710 or hypothetical pulses as accepted full converter model. NoPSpice purchase assumed. |
| RC-PROT-001 | Existing major; retained | Changing controller does not prove old protection concerns closed; missing/open/short/partial/reversed/hot behavior must be defined and validated on this circuit. |
| RC-INPUT-001 | Existing major; retained | Fuse I²t is typical under stated sourceconditions; pulse/surge/coordination/ripple/thermal/fit not accepted. Ordinary averaged charge peak is not inrush or fault evidence. |
| U05–U09 / service / safety / thermal / lifetime / process | Existing gates; retained | Fresh requirements check still fails. Complete limits/interfaces/measurement plan/physical material and insulation/process evidence before applicable stage; no blank app record or example capabilities assumed. |

Newledger IDs do not delete or replace earlier finding histories. All older major scopes remain until explicit independent closure on actual relevant evidence. None is closed by this report's internal consistency or native ERC result.

# Explicit non-physical power-source declarations

The first actual product ERC reported three power_pin_not_driven errors at U1.1VDD, U1.4GND and U1.7HV. These are resolved using three original local POWER_SOURCE symbols with KiCad's standard `(power)` annotation semantics, not physical power-supply components. U1 pin types remain power_in; all passive rectifier/winding/resistor types are unchanged. No ERC severity, exclusion or waiver is added.

| Annotation | Electrical network | Actual intended source path | Verification boundary |
|---|---|---|---|
| #FLG01 | BULK_POS | External E27 AC through F1/RIN/BR1 and CBULK | Source declaration only; not line/startup/surge qualification |
| #FLG02 | PRIMARY_GND | BR1 negative/CBULK negative and primary supply return | Return declaration only; never joined to isolated output return |
| #FLG03 | VDD | U1 internal HV startup charging, then T1 auxiliary → DAUX → RAUX and CV1/CV2 | Source declaration only; actual startup charge/timing remains RC-BIAS-001 |

Separate implementer /root/model_compatibility tested the native flag mechanism on real synthetic KiCad10.0.6 exports with passive-source and physical-source controls. The copied experiment report/results identify native symbol provenance and unrelated fixture warnings. The product uses an original graphical symbol with the same power-annotation semantics, not a falsely claimed native-library release.

The final ACTUAL product export was compared by the installed locked toolkit:28 physical components/73 physical terminals/21 nets/4NC, exact approved intent unchanged. Non-physical #FLG symbols are omitted from native physical XML component/pin sets. Their absence was verified by the genuine product comparison, not by removing extra components from the expected graph. Native ERC now exits0 with zero findings. Neither result establishes analog operation or source adequacy.

SCH-ANN-001 remains separate: native export reports annotation warning for the approved nonnumeric role references such as RIN/DOUT. A controlled synthetic reference-only change independently reproduces that warning. The product references were not silently renamed, so the human-approved graph is preserved. Numeric-reference ECO remains an owned library/capture acceptance task; export success does not erase the warning.

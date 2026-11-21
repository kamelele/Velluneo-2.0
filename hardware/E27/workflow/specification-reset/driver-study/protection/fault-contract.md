# Proposed base fault/recovery contract

VEL-FAULT-INTENT-01 r1, 2026-11-16. Proposed implementation intent for packet r11 requirements R-FAULT/R-EMPTY/R-OFFLINE/R-THERMAL/R-COMPAT. Functional requirements are preserved; these rows are not verification results or a new owner approval. Architecture A: covered isolated driver/regulation/protection in the base, common simple replaceable panels.

| Condition | Intended response | Evidence still required |
|---|---|---|
| Healthy supported panel | Common fixed factory current; steady useful light without user settings. | Actual current/light ripple, accuracy, CCT/flux/thermal behavior; adopted optical criteria and all claimed variants. |
| No panel at power-on | Limit output voltage/energy; remain indefinitely without destructive heating. | Real OVP/retry waveform, VCC/auxiliary/clamp stress, output ratings, fault/access limits and long-duration worst-ambient empty-base heat. |
| Panel opens/fails during use | Stop normal power transfer through OVP; any retry must be non-destructive and energy/temperature bounded. | Detection/filter/stop latency, residual pulses, output energy, VCC guard and component temperatures. No assumed four-pulse limit accepted as proof. |
| Panel shorts during use/start | Limit primary pulse stress and enter benign low-frequency/UVLO recovery as implemented; no base fuse change or destructive failure from the panel fault. | Actual incomplete reset/CCM, blanking/turn-off, burst duration/average power, transformer/rectifier/gate/clamp stress, capacitor discharge and fuse coordination. |
| Healthy panel installed after offline replacement | Restore normal operation after ordinary power cycling, without hidden reset/calibration or fuse replacement. | Matched normal/fault/power-off/recovery sequence with actual stored-energy and reset conditions. No live panel insertion is authorized by this requirement. |
| Abnormal overheating | Automatic recoverable protection preferred; normal rated operation must not depend on repetitive thermal cycling. | Proposed self-resetting base thermal protector or a justified simpler equivalent, exact thermal trip/reset and rated switching/placement/life; whole-lamp thermal map. IC shutdown is not whole-lamp evidence. |
| Lamp unscrewed for replacement | Primary stays behind a separate cover; panel and its mount are the only normal service area; replacement after justified cooling/discharge delay. | Accessible voltages/energy and re-energization after removal; contact/insulation geometry, discharge-path faults, actual measured delay and temperature. No numeric wait time selected. |

A trip/cool/retry response is not failure immunity. The final design must prevent damage during fault persistence and subsequent recovery; fault tests must use the exact reviewed configuration and appropriate laboratory setup. The owner has described university/experienced-person support; actual readiness/method/equipment must be established before testing. These requirements do not impose an outside reviewer before calculations and do not authorize physical tests now.

## Interpretation boundaries

Panel replacement does not expose the mains primary. Recessed/keyed contacts, insulation barriers and the method of retaining the base cover still require explicit interface/mechanical design. Nominal output voltage alone is not an insulation or touch-safety classification. A 50 V capacitor class, an illustrative 40 V ceiling and a passive discharge calculation establish no safe user access limit.

The protection proposal uses the lower current-limit reference configuration in a physically isolated transformer circuit. No independent active short detector is selected merely because the controller's mode label says non-isolated. Actual filtering/negative-clamp/sense/gate behavior and fault-energy coordination remain mandatory engineering work.

Internal controller failure, a failed clamp/discharge path, insulation/component single faults and relevant abnormal conditions need the eventual applicable safety assessment; the panel-fault contract is not a complete product safety analysis. No protection, isolation, thermal, lifetime or regulatory pass is claimed.

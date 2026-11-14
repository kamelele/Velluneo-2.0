# LYTSwitch-5: independent DCM, magnetics and output-storage screen

VEL-FLYBACK-DCM-01 r2, 2026-11-14. Specification investigation supporting owner-selected architecture A and product packet r11. Candidate ordering option: LYT5225D-TL. No controller, transformer, protection ceiling, capacitor or service delay is selected. Previous CrM calculations are not a design for this controller.

## Result and practical decision

A fresh ideal DCM model identifies an exploratory 0.50 mH, 4:1 transformer operating region compatible with selected catalogue timing/current comparisons. This is a mathematical feasibility witness, not a LYTSwitch-5 controller simulation, manufacturer spreadsheet result or regulation design. Its least minimum-on-time margin is only about 2.1% against a 25 C table limit; that is not sufficient evidence to freeze the design over temperature and production.

The main new trade-off is output storage. The modeled single-stage sinusoidal-power approach removes the earlier assumed smoothed high-voltage bus, but the 100 Hz energy pulsation must be buffered somewhere. An output capacitor alone cannot guarantee low light ripple without the actual LED current/voltage and control-loop behavior. Larger output storage also takes space and can increase discharge time. Therefore a smaller transformer and integrated switch do not yet establish the smaller or better complete lamp supply.

## Sources and actual access

The author re-opened the LYTSwitch-5 rev C electrical tables and DER-528 transformer/worksheet pages visually. AN-65, previously returning HTTP 406, was now available through the web service's indexed PDF text; its DCM guidance, primary-sensing distinctions and tuning workflow were read. Some extracted equations are malformed, so the script uses independently derived circuit/energy equations rather than copying OCR expressions. No native AN-65 file checksum, manufacturer calculation workbook, PI Expert result or hardware measurement has been obtained.

Manufacturer basis used in the comparison: DCM operation; LYT5225's current-limit table at 25 C is 1.232–1.418 A; minimum-on-time upper table value is 1.15 us and maximum-on-time lower value 5.75 us at 25 C; fMIN is 40 kHz typical and fMAX minimum is 115.3 kHz at 25 C. The script samples +/-4% as an interpretation of the stated 8% peak-to-peak frequency jitter. These limited conditions do not establish full-temperature timing/current bounds or reproduce the jitter/control algorithm.

## New operating model

Inputs retained as investigation assumptions: 207/230/253 V RMS, 50 Hz; 18/21/24/27 V load; 228/250/286.227 mA secondary load. The largest current includes the former illustrative bleeder at its high-voltage/-1% corner. The mains screening range and load window are not newly approved requirements.

Separate new assumptions: no smoothing bulk capacitor that holds the rectified mains flat; sinusoidal unity-power-factor input power; ideal triangular DCM currents; 0.8 V secondary drop; primary inductance 0.50 mH +/-10%; Np=96, Ns=24. Extra power sensitivities of 0 and 0.30 W are assigned entirely to an equivalent additional secondary load. That reserve is not an actual loss calculation, panel-power requirement or predicted secondary current. Actual bias energy splits differently.

For phase angle theta, Vpk=sqrt(2)*VAC and average transferred magnetic power Pm, the mathematical witness uses:

- Ipk(theta)=sqrt(4*Pm/(Lp*f))*sin(theta).
- ton=Lp*Ipk_crest/Vpk; demagnetization time(theta)=Lp*Ipk(theta)/(n*(Vo+Vd)).
- KDP=(1/f-ton)/demagnetization time_crest; KDP>1 implies an idle interval at the crest.
- A deliberately constructed operating-point law f_nom=max(42 kHz, 9500 Hz/W*Pm), sampled with jitter factors 0.96/1.04.

That law only demonstrates possible operating points; it is not programmable into this IC as written, not its actual control law and not a proposed resistor setting. Its purpose is to test whether the candidate magnetic/load region has any timing room before controller-specific programming. Actual controller frequency, current accuracy and line/zero-crossing behavior remain unknown.

`dcm.py` evaluates 288 electrical combinations and 2304 additional phase samples. Each case checks average magnetic-energy and secondary-current identities. Primary and secondary line-cycle RMS use analytical sine-wave integrals, not crest-cycle RMS mislabeled as full-line RMS. All sampled non-crest phases have at least the crest idle interval under the assumed model. Rectifier drops, conduction dead zones and real zero-crossing operation are excluded. Sampled extrema are not continuous certified bounds.

| Quantity | Calculated range / maximum |
|---|---:|
| Sampled switching frequency | 40.32–81.58 kHz |
| On-time | 1.175–1.678 us |
| Crest idle interval | 6.40–17.76 us |
| KDP at crest | 2.51–4.09 |
| Primary crest peak current | 0.987 A maximum |
| Secondary crest peak current | 3.949 A maximum |
| Primary full-line RMS current | 0.136 A maximum |
| Secondary full-line RMS current | 0.822 A maximum |
| Calculated normal flux swing | 0.165 T maximum |
| Magnetic transfer average power | 4.286–8.257 W including equivalent-load sensitivity |

These results justify further controller-specific analysis only. They do not qualify 9 W output inside an E27 base or the earlier provisional 20% capacity reserve. The previous CrM model used smoothed DC rather than this input waveform; its RMS, frequency and efficiency proxies are not directly comparable as an equal-input benchmark. A final architecture comparison must use equal line/storage/optical requirements.

## Transformer and device implications

The exploratory 96/24-turn transformer needs AL approximately 54.25 nH/turn2 for 0.50 mH. The 31 mm2 area comes from the same previously inspected EFD20/10/7 core family. This AL is not the previously identified catalogue AL100 option and is unconfirmed custom magnetics. An exploratory 12-turn auxiliary winding would give approximately 8.7–13.2 V after assumed drops across the normal load window. These are model counts and voltages, not winding/manufacturing instructions, a proven bias supply or a selected core/bobbin/gap.

Winding fill, hot material properties, core/copper losses, leakage/clamp, wire insulation, interwinding barriers, termination and assembly are unverified. At Lp+10% and the 25 C table upper current limit, linear flux would be about 0.262 T. This does not validate fault saturation. Propagation delay is not blindly added to an already measured ramp-current limit; actual slope/temperature/leading-edge behavior must be checked against the controller and magnetic data.

Maximum drain plateau is 469 V, or 569 V with the same hypothetical 100 V overshoot used previously. Actual surge and ringing are not bounded. The integrated 725 V switch still requires a properly designed clamp and surge strategy. Rectifier reverse voltage is 116.45 V before ringing. The earlier 200 V diode class therefore remains an investigation direction, but approximately 4 A pulses and higher RMS require a new device/thermal check rather than reusing the earlier 1 A-peak calculation.

Using the listed 6.55 ohm maximum at 100 C as a limited conduction proxy gives switch conduction up to 0.122 W. The fixed-drop rectifier proxy reaches 0.242 W. No total efficiency or heat budget is established: gate/controller/drain supply, bias, clamp, magnetic, bridge, sensing and switching losses remain open.

## Output energy storage and service implications

For ideal sinusoidal input power and hypothetical constant output load power P, buffer-energy variation peak-to-peak is P/(2*pi*f_line). The capacitor-only energy model uses Vcenter=sqrt(mean(Vcap squared)); it is not an asserted mean LED voltage. It does not solve the real LED nonlinear load or feedback loop. At Vcenter=21 V and 250 mA, capacitor -20%:

| Nominal output capacitance | Ideal buffer-voltage ripple peak-to-peak | Illustrative 30-to-5 V discharge with C+20%, 10 kohm+1% |
|---|---:|---:|
| 220 uF | 4.55 V | 4.78 s |
| 470 uF | 2.12 V | 10.21 s |
| 1000 uF | 0.995 V | 21.72 s |

The approximate low-frequency capacitor-ripple-current scale is 0.177 A RMS at that current, excluding switching ripple and ESR heating. These figures are buffer screens, not a capacitor specification, LED ripple, flicker performance, acceptable 5 V limit or safe wait time. Across the separate storage examples, instantaneous voltage extends approximately from 15.22 to 29.45 V. Thus the 18–27 V centers do not bound instantaneous voltage. The DCM stress/bias calculations above do not include these storage excursions: a coupled LED/control/storage model must update normal voltage/current, bias, OVP, rectifier/clamp ratings and transient margins before any selection. Do not treat the earlier 469/569 V drain figures as bounds for a completed buffered circuit. The discharge example excludes continued conversion, failure of the discharge path, primary stored energy and cooling. Increased capacitance may reduce voltage ripple while delaying discharge; selecting it requires real LED dynamic resistance, flicker requirements, tolerance/ESR/ripple lifetime, size, fault voltage and safe-access analysis together. No assumption that a larger capacitor alone cures flicker is accepted.

## Procurement evidence and next choice

Exact suffix matters. LCSC lists LYT5225D as C567758 and LYT5225D-TL as C567759. The former page reports out of stock; the latter listing does not establish available assembly inventory. DigiKey's directly opened page labels the -TL version Active, while its tube version is discontinued at that distributor. Neither statement proves manufacturer-wide discontinuation or long-term supply. The manufacturer still lists the family and links -TL distributors. Direct JLCPCB lookup for C567759 was inaccessible, so no JLCPCB stock or assembly capability is confirmed. LCSC's SOIC-14 category is not a footprint specification; use the manufacturer's SO-16B drawing and omitted lead positions for any later library review.

Prioritize actual feedback/bias/OVP programming and output-storage/fit analysis for LYT5225D-TL before considering the larger LYT5226D justified. Manufacturer worksheet calibration fields require actual measured bias/output/current: those must stay blank until measurements exist. Open/no-load/short, thermal recovery, safe accessible interface, actual LED bounds and source/process feasibility still prevent final selection. No orders, supplier messages or manufacturing files were submitted.

## Reproduction and sources

Run `python dcm.py > dcm-results.json` beside the upstream `results.json`; its SHA-256 dependency is checked. Only algebra and sample consistency checks were executed. No SPICE, controller simulation, CAD/ERC/DRC, installed-toolkit environment check or physical test. Four independent agent review scopes and frozen hashes are in `dcm-review.md`.

Sources inspected 2026-11-14:
- PI LYTSwitch-5 rev C: https://www.power.com/sites/default/files/documents/lytswitch-5_family_datasheet.pdf (electrical tables visually inspected).
- PI AN-65: https://www.power.com/sites/default/files/documents/an65.pdf (indexed text accessed this turn; extraction limitations noted).
- PI DER-528: https://www.power.com/sites/default/files/documents/der528.pdf (reference transformer, circuit and worksheet visually inspected; no values copied as this design).
- TDK EFD20/10/7: https://www.tdk-electronics.tdk.com/inf/80/db/fer/efd_20_10_7.pdf (area previously checked in VEL-FLYBACK-01; not a newly sourced transformer).
- Exact distributor listings: https://www.lcsc.com/product-detail/C567758.html and https://www.lcsc.com/product-detail/C567759.html ; https://www.digikey.si/en/products/detail/power-integrations/LYT5225D-TL/5819975 and https://www.digikey.si/en/products/detail/power-integrations/LYT5225D/5870086
- Manufacturer catalogue: https://www.power.com/products/lytswitch/lytswitch-5/lyt5225d

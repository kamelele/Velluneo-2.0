# E27 single-string specification

Revision 8S-spec-2. The project owner selected one series string of eight LEDs on 2026-11-11. This decision selects the architecture for investigation. The detailed specification and stage evidence are for review.

## Product and electrical intent

- The replaceable insert uses eight 3 V LED packages in one current path. The power board is the candidate location for constant-current regulation, independent output overvoltage protection and the existing removal and thermal shutdown functions. The insert interface needs a positive feed and return. Physical contact numbering and the separate interlock and thermostat wiring will be agreed before schematic work.
- Retain the product targets of 750–850 lm after the diffuser at steady state and CRI ≥80 in 2700 K, 4000 K and 6500 K versions. The first bench sample is 2700 K. Evaluate the other two CCTs before release. Retain the engineering junction-temperature target of ≤95°C under rated conditions from the baseline. Final ambient and measurement setup are open.
- The baseline target for accessible contacts is ≤30 V DC including ripple and peaks under a single fault and <5 V within 100 ms after normal opening. Evaluate reinforced mains-to-accessible isolation, removal and reinsertion, open LED string, shorted output, sense and feedback faults, independent shutdown and residual energy. Establish the applicable product classification and test conditions before release. Use the baseline 207–253 VAC, 50 Hz range for design screening. Verify startup, continuous regulated output and fault handling across that range. [E27 baseline](../../outputs/Raport_E27_RevA.md)
- Use the [power Rev K](../../outputs/Zasilacz_RevK_Moc/README.md) and [control Rev H](../../outputs/Zasilacz_RevH_Sterowanie/README.md) as archived engineering references. Treat their native checks and JLCPCB exports as evidence for those revisions.

## Driver-to-insert interface change

- The 2×8 baseline uses a common anode and two regulated cathode returns. The 8S proposal uses one positive feed and one regulated return. Disposition of the former second cathode contact, including its physical removal or safe unused status, remains a connector decision.
- Retain S1 and TH1 as a shutdown path and retain S2 as an independent physical interruption of the positive feed as the baseline behavior. Review that opening inhibits drive, opens the positive path and discharges the exposed contact side before access. On closing, contacts must mate before re-enabling drive. Verify stuck-switch and wiring faults. Physical pin numbers, tolerance limits and actual contact timing are open.

## LED feasibility

Candidate MPNs are Cree JB2835BWT-G-H27GA0000-N0000001, JB2835BWT-G-H40GA0000-N0000001 and JB2835BWT-G-H65GA0000-N0000001. The warm device has 29.1 lm typical and 27.0 lm minimum at 55 mA and 25°C. The datasheet lists 27.2 lm typical, calculated at 85°C. Approximate multipliers digitized from page 6 are 4.23 at 250 mA, 4.38 at 260 mA and 4.69 at 280 mA. For the 2700 K variant:

- At 250 mA, about 800 lm in the typical scenario and 680 lm in the adverse scenario.
- At 260 mA, about 830 lm typical and 710 lm adverse.
- At 280 mA, about 890 lm typical and 760 lm adverse.

The typical calculation uses 27.2 lm, 85°C and diffuser transmission 0.87. The adverse calculation uses the 27.0 lm bin floor, approximate flux factor 0.90 at 105°C and transmission 0.83. Both multiply the baseline flux by the relative-current curve and by eight. The 105°C case is a sensitivity case above the project junction-temperature target. Current and temperature corrections are treated as separable. This model leaves bin spread, diffuser variation and optical measurement tolerance for bench verification. Use one driver PCB across CCTs as the starting point. Evaluate bin selection and a fixed current-setting component per CCT. The modeled 260 mA adverse case falls below 750 lm, and the 280 mA typical case exceeds 850 lm. Release acceptance requires a measured current, flux and temperature matrix for each CCT and a bin and current selection rule. [Cree datasheet, pp. 4–8](https://downloads.cree-led.com/files/ds/j/JSeries-2835-3V-Consolidated.pdf#page=4)

## Power-stage calculations

- For an illustrative hot forward voltage of 3.0 V per LED, the series load is 24.0 V and 6.24 W at 260 mA or 6.72 W at 280 mA. A 3.2 V per LED cold screening assumption gives 25.6 V. It is a design input to verify on parts and must cover selected bins, current and temperature. At 280 mA this is 7.17 W at the LED contacts. Recalculate low-line transformer margin, rectifier loading, output ripple and startup for the measured load envelope.
- Rev K uses LYT6073C-TL and R9 = 0.11 Ω as an aggregate current limit. With the datasheet 35.17–36.62 mV ISENSE threshold at 25°C, a 1% 0.137 Ω candidate gives about 254–270 mA and 0.130 Ω gives about 268–285 mA. These are comparison values for a future constant-current circuit. The loop, output-voltage limit, dynamic behavior and temperature tolerance still need verification. [Rev K BOM](../../outputs/Zasilacz_RevK_Moc/BOM_RevK.csv) · [LYTSwitch-6 datasheet](https://www.power.com/sites/default/files/documents/lytswitch-6_family_datasheet.pdf)
- Rev K uses 470 µF at its output. If that full capacitance were connected to the exposed contacts after opening, it would store about 0.21 J at 30 V. At 564 µF, corresponding to a +20% screening assumption, a continuous passive path would need about 99 Ω or less to fall from 30 V to 5 V in 100 ms. At 30 V, 99 Ω would dissipate about 9 W continuously. In schematic review, identify which capacitance stays connected to the contacts and evaluate isolation of the reservoir and discharge of the contact-side capacitance.
- Define the minimum cold-start ambient, cold-soak and acquisition timing and measurement uncertainty. Determine minimum driver compliance from the resulting worst-case cold string voltage plus path drops and ripple. Budget the maximum protection threshold, tolerances and turn-off overshoot against 30 V separately. The exact normal voltage limit, fault threshold, component choices and startup timing are open.

## Retained verification requirements

- Before layout, establish mains-to-accessible insulation design inputs and the accessible contact sequence with the enclosure. Keep the 8 mm PCB separation target from the baseline as an engineering input. Derive the actual clearance and creepage requirements from the verified materials, insulation system and product classification.
- Keep conducted and radiated EMC, immunity, individual mains harmonics, PF and DF, and PstLM/SVM checks for the complete lamp. Confirm classification and applicable limits for this design before layout and collect measured evidence before release. Legacy design targets are documented in the baseline report.
- Start thermal tests at 25°C and 40°C, in both vertical directions and horizontal, and include the worst intended fixture. Retain the ≤85°C electrolytic case target at 40°C ambient. Confirm the rated ambient and temperature measurement setup before qualification. [E27 baseline](../../outputs/Raport_E27_RevA.md)

## Profiles and evidence

- Common profile uses the pinned toolkit recorded in the project index. The historical native CAD baseline is KiCad 10.0.8. Toolkit CAD validation uses 10.0.6 and its matching pcbnew.
- Product profile is an E27 mains-powered lamp with an isolated user-replaceable 8S insert and a single power PCB as the packaging goal. External geometry, creepage, insulation and the contact sequence need inputs from the complete assembly.
- JLCPCB FR-4 routed, two layers and 1 oz copper is the fabrication proposal. The [process proposal](profile-proposal.md) specifies a nominal 1.6 mm board and lead-free HASL for review. Obtain the exact order stackup and laminate information before using them in the isolation and placement reviews.
- JLCPCB supplier assembly is the working proposal. Confirm the intended Standard PCBA service and applicable constraints at specification. Review exact T1 and through-hole scope, BOM and approved panel before release. The LED insert MCPCB fabrication and assembly are separate from the FR-4 driver proposal. [Fabrication capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/) · [Assembly capabilities](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)

## Low-voltage bring-up plan

Use an isolated, current-limited bench supply on the 8S insert. Start at a lower current and step to 240, 250, 260, 270 and 280 mA as thermal data permits. Record LED part numbers and bins, sample IDs, ambient, diffuser configuration, cold string voltage at each tested current and the stabilized voltage, flux, CCT, CRI and solder-point temperature. Estimate junction temperature from the measured solder-point temperature and the applicable datasheet thermal model. Use a calibrated integrating sphere for the flux decision. The baseline proposes at least three inserts per CCT for development and samples from several lots before series production. Record the supply current ceiling and stop before exceeding the approved thermal limit. Close the cold-voltage window and current setting using actual data. Capture these tests as measurement evidence separately from the calculations.

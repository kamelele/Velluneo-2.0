# SC08 bounded driver-current research

Author: /root/driver_research. Existing design read only; no CAD changes or stage approval. Supplied remote source revision a6c7ed424a6aa882ef7e5b46899955d3d928f09d. Analysis uses the actual SC07-C coupled_output.py bytes (SHA256 f364fabc8c75c5547e22d09057c856f5eed29e9dbd3b79fe6a0dd8767bb6345d), not a checked-out claim about the local Git HEAD.

## Recommendation and handoff scope

Retain the LYT0 control architecture for a bounded engineering prototype. Do not substitute a nominal resistor adjustment for qualification; instead select the populated R2 after measuring average LED current, then verify line and temperature behavior. Current accuracy and fault-energy/temperature safety are different requirements. No complete commercial-lamp acceptance is established here.

Root's subsequent SC08-A proposal is a different input network (input L removed, RF2/D4 and different TVS added) and2x22uF X7R feedback. The trim experiment below uses the ORIGINAL SC07 ideal-source model. It is not a simulation of that new RC input, nor a review/approval of new SC08 CAD. The earlier input-L-energy warning below applies only if such an inductor is present. A new RC input needs a fresh coupled model and measured correlation.

## Primary-source findings

LYT0006D datasheet Rev B 06/15 current-limit tables explicitly use TJ=25C and selected current slopes; temperature/current-slope curves are typical. No located primary document supplies the complete hot/all-slope envelope previously imposed as Ipk<=0.7A. The official design guide/reference-design method supports calculations followed by maximum drain current, startup/fault and thermal verification; this is a normal prototype qualification task, not justification for renaming typical curves guaranteed.

Sources: https://www.power.com/sites/default/files/documents/lytswitch-0_family_datasheet.pdf and https://www.power.com/sites/default/files/documents/an60.pdf .

LYTSwitch-5 LYT5225D/LYT5226D integrates a 725V switch and output-OVP processing, potentially removing external OVP parts. However, Rev C explicitly labels feedback accuracy, important OVP thresholds and current-limit/delay rows TJ=25C. Its 9W/16W table is conditional on open-frame heatsinking at50C. This is a new low-side topology with different sensing/magnetics, not a drop-in or a route to automatic full-temperature assurance. It still needs PIXls/DCM design and physical correlation. No reason found to discard SC07 merely to obtain an equally conditional device table. Sources: https://www.power.com/sites/default/files/documents/lytswitch-5_family_datasheet.pdf and https://www.power.com/products/lytswitch/lytswitch-5 .

BP2863X plain version is not a protected replacement: the manufacturer catalog differentiates X from XJ for open-load protection, and lists500V switching. Do not infer XJ documentation/thresholds from X. Full X source: https://www.bpsemi.com/upload/en/file/2024-01/col547/1705890914604.pdf . Catalog: https://www.bpsemi.com/col302/index . AL5890 is NRND and AL5809 is only60V operating; neither is a simple unrestricted substitute for the whole off-line stage. https://www.diodes.com/part/view/AL5890 ; https://www.diodes.com/assets/Datasheets/AL5809.pdf .

## Current-trim experiment (own model, actually executed)

Eight combinations: R7=433.105/508.305ohm, L=2.4/3.3mH, and bundled controller sensitivity inputs low(1.54V,350mA,62kHz)/high(1.76V,504mA,70kHz). Each combination individually tuned R2 at230VAC to55mA using seven bisection steps; every run2s, report final1s. Then fixed that R2 and reran207/230/253VAC,2s each. Cfb22uF, Cout120uF, fixed LED Vf84.5V, gate minimum675ns, capacitor leakage1.45mA. These are the existing model's illustrative assumptions, not device guarantees or actual LED IV.

Computed R2 range25.46094..31.39844ohm. Across24 post-trim line checks LED average54.4284..55.3341mA. Discrete controller decisions prevent interpreting extra decimal places as physical precision. E96 population approximately25.5..31.6ohm is a useful prototype trim menu; verify actual discrete selections before use. Exact MPN examples in the same HP1206 family: CRCW120625R5FKEAHP, CRCW120626R1FKEAHP, CRCW120628R7FKEAHP, CRCW120631R6FKEAHP (manufacturer coding evidence, not distributor-stock verification). Keep one selected sense resistor; no powered adjustment implied.

This demonstrates why per-board current trim can absorb fixed unit variations; it does not absorb temperature-induced or mechanism/model errors automatically. Record calibration current, mains, load, device temperatures and trim value; recheck cold/hot207/230/253VAC. Flux800lm needs the optical module/temperature measurement, not just55mA.

Reproducible source: trim_sensitivity.py. Actual numerical report: trim-results.json. It verifies the input function hash before executing only in-memory functions and writes only to this research folder.

C4 changes with trim: AN60 tau>20T gives Ceff>20/(62000*25.5)=12.650uF, or12.778uF with Rsense-1%. Nominal22uF*(-20%)*(-15%)=14.96uF before DC bias/aging; only14.6% further reduction remains. At minimum candidate25.5ohm do not inherit the28.7ohm capacitance allowance. Worst25C threshold-power screen1.76^2/(25.5*.99)=0.1227W versus conditional HP1206 allowance0.75*(155-125)/(155-70)=0.2647W. Ceff and substrate temperature still require verification.

## Passive LED and output-energy envelopes

At COUT<=135V and R7>=433.105ohm, zero-load-voltage current<=311.7mA, healthy60V floor173.17mA, one-LED-short58V floor177.79mA. At proposed145V these become334.79mA/196.26mA/200.88mA. The60/58V floors are design assumptions requiring LED IV/load-case support, not minimum values guaranteed by the55mA Vf table.

Cree JB2835B G datasheet lists480mA absolute DC maximum, but its operating curve explicitly depends on Rja40K/W and derates to180mA at105C. Therefore196mA at145V is not supported by the105C example. A bounded open prototype with LED ambient85C and demonstrated effective thermal path has a more plausible envelope, but module self/mutual heating and junction temperature must be checked. Source https://downloads.cree-led.com/files/ds/j/JSeries-2835-3V-Consolidated.pdf . No pulse overrating was assumed.

For root's proposed two220ohm input resistors: using total Rmin396.264ohm and |Vs|<=357.796V, instantaneous power transferred beyond the resistors is Vs*i-R*i^2<=Vs^2/(4R)=80.77W. This is independent of the controller's current-average claim. Add every pre-existing stored-energy reservoir separately, including input L1, not only film capacitance and output inductors. This is a normal-line shutdown-energy bound, not a surge-proof equation.

Illustration: starting131V on Cmin120uF,2ms at80.77W plus film energy30.3mJ, output L energy3.23mJ and an illustrative input L energy10.78mJ yields about143.5V. The1.4A/11mH input-L example is not a proven current envelope. Under these assumptions145V permits about2.32ms, not2.45ms. Never omit L1 energy or claim a guessed initial current has been guaranteed.

## Thermal/fault distinctions

R7 normal55mA nominal dissipation1.422W. At90mA and R7max508.305ohm it is4.117W, before hot derating. At145V/healthy60V, its instantaneous dissipation is16.68W. Retry duty can make average fault dissipation exceed5W even if every capacitor charge remains below145V. Thus an output-energy proof does not prove R7 continuous/repetitive thermal safety. Driver loss of current regulation plus a short LED load can also evade voltage-only protection; classify the actual single/compound fault mechanisms explicitly.

Two220ohm input resistors roughly double loss at unchanged actual input RMS current:60mA gives1.584W total (0.792W each),80mA gives2.816W total (1.408W each). Actual input RMS must come from the input-network model/measurement; DRAIN RMS is not RF RMS. New input resistance changes available current/headroom, so these examples are not predictions or proof of unchanged LED regulation.

Correctable now: include all stored energy; select resistor/thermal/temperature budgets; provide R2 trim menu and updated C4 requirement; preserve exact actuator-open scope; use an actual two-resistor input-network calculation. Later prototype evidence: hot/cold current, real delay/OVP peak, nonlinear inrush, repeated removal/reconnect, resistor/relay/shunt temperatures, surge clamp/ringing. Commercial optical, EMC and accessibility/insulation/fire evidence remains later release work. No claim of physical tests or manufacturable PCB qualification.

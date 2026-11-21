# ECO22 startup-feed resistor comparison

Bounded implementer: /root/eco22_resistors. Root owns CAD/power-model integration.
Baseline: C16 at commit63c7a3fed59d7807bd1b71cf9058175b04a22f4b. No CAD is written
by this script. Run `python calculate.py` using the standard library only; it writes
results.json here. This is a conditional analytical comparison, not a controller
transient simulation, measured startup, optical response or protection qualification.

## Selected bounded change

- R16/R17:402k each -> **422k each, Vishay CRCW2512422KFKEG**,2512,1%,100ppm/K.
  Retain the existing **500V /1W at70C** family. Total resistance allowance remains
  the inherited engineering +/-2.1%, not a demonstrated lifetime-drift bound.
- R13:80.6k CRCW -> **84.5k, Vishay TNPW060384K5BEEA**,0603,0.1%,25ppm/K,100V.
  Use a deliberately widened **+/-0.65% engineering allowance**. Initial tolerance
  plus25ppm/K over150K is0.475%; the additional allowance is a declared budget,
  not measured ageing or a guaranteed five-year total-error limit. Current maker
  P70 is0.21W; retain a conservative100mW integration rating unless the actual
  PCB thermal conditions justify more. At35V the selected resistor dissipates
  about14.6mW, below that conservative screen.

R1, all four bulk-discharge resistors, output preload/bleeders and current/voltage/
line programming resistors remain unchanged. The existing bulk passive-only
discharge analysis and protection values are not relaxed to obtain efficiency.
Normal voltage-feed limits below apply only to the startup-resistor source;
they do not bound auxiliary, commutation or surge injection into VDD.

## Results and accounting scope

The64DCcases/design reuse the inherited analytic charge law:

`Rpar=Rstart||R13; Vinf=Rpar*(Vbulk/Rstart-Istart-ID2);`
`t23=-Rpar*Cdd*ln(1-23/Vinf)` whenVinf>23.

Cases:207/253Vac,0/5V bulk-drop allowance, independent resistor extrema,
Cdd=.94uF+/-5%, D2 leakage3/20uA and TI startup1.5uA. C2/C3 are the actual
470nF C0G/J-tolerance parts; the two capacitors are both directly on VDD.

The baseline worst charge time is0.251660s; selectedECO22 is0.247664s. Minimum
net charge current at23V improves9.52777->11.75374uA. Normal-line zero-controller-
draw feed-only ceiling decreases33.86666->33.39124V, below35V in this screen.
All64cases for each selected design reach23V. Charging to23V is not the complete
start<=1s/90%-stabilized-flux requirement: sampling pulses, gate load, auxiliary
handoff, LED charging and controller state transitions require further verification.

The rejected2xfeed804k->1.612M/R13=162k proposal fails4of64hot-leak cases;
minimum equilibrium22.18029V cannot reach23V. It is not adopted. Simply scaling
the resistors without accounting for the unchanged diode/controller leakage would
incorrectly imply an easy50% reduction of startup-feed loss.

There are72additional rectified-input witnesses for EACH selected design. They
integrate ideal-sine bridge, bulk capacitor and VDD capacitor until the FIRST23V
crossing:207Vac49/50/51Hz;4rectified phases;0/50/100ms linear amplitude ramps;
Cbulk12/18uF;Cdd=.987uF;worst charging resistor corners;R1=49.35ohm plus selected
6ohm fuse resistance;2V bridge pair;bulk bleed488.521k;selected246.5uA bulk
leakage;constant21.5uA D2/controller draw. No switching occurs in this witness.
The bulk-leakage value is motivated by the Rubycon rated-voltage five-minute
20C formula, not a guaranteed hot/actual-voltage leakage bound. Series/fuse/drop
values are sensitivities, not a complete source-impedance or inrush qualification.
Midpoint10us is refined to5/2.5us on nominal-resistor witnesses. Times are quantized
at the timestep; the source and full rows are retained for replay.

Conservative VDD hold-up lower screens use Cmin=.893uF and NO CREDIT for positive
startup feed in either design; full-time IRUN2.65mA, Qg20nC*140kHz, full-time10V/
47k gate pulldown and R13draw bounded at23V are additive engineering sensitivities.
R13draw falls, so this conservative hold-up lower bound improves. The actual
nominal net startup contribution falls slightly: not every real trajectory margin
improves, and no complete bias takeover is qualified.

Net continuous startup feed at8.45V/highline falls from341.148uA to the recorded
ECO22value. This reduces the OTHER sink required to force VDD lower but cannot
establish fault-retry timing: TI provides no guaranteed minimum fault sink in the
used table. The displayed passive35->8.45/5V times assume bulk FORCED TO ZERO,
no other draw and C/R maxima; they become slightly longer. They are not powered
fault, lamp-service or discharge waiting times. Existing whole-assembly limits
and physical qualifications remain open.

Single-short screens address only the remaining startup resistor's voltage/power:
full357.8V bus atVDD0,500V rating retained, dissipated power below the same125C
CRCW2512derating screen. They do not prove every circuit single fault, including
VDD behavior after a resistor short or auxiliary fault.

At the inherited nominal310.363Vbus/11.131VDD, the three-resistor heat saving is
approximately **5.35mW**. Full input-power change depends on the integrated bias/
magnetic accounting; it must not be counted twice as both startup and transformer
efficiency gain. This modest change does not solve the driver's thermal reserve.

## Exact source and purchase routes

Manufacturer sources read21November2026:

- TI UCC2870x SLUSB41A: startup1.5uA/table18V; UVLO maxima and VDD operating range;
  RUN current2.65mA maximum has zero gate-load test conditions. The continuous
  RUN/large-gate additive hold budget is explicitly hypothetical.
  https://www.ti.com/lit/ds/symlink/ucc28700.pdf
- STTH1R02A DS4743Rev4: IR3uA at25C,20uA max at125C, at rated reverse voltage.
  These are source conditions, not a measured actual-bias startup current curve.
  https://www.st.com/resource/en/datasheet/stth1r02.pdf
- Vishay CRCW Rev14-Apr-2026, document20035:2512P70=1W,Umax500V;
  initial1%/TCR100ppm packing code applies to the selected exact part.
  https://www.vishay.com/docs/20035/dcrcwe3.pdf
- Vishay TNPW Rev10-Apr-2026, document28758:0603100V,P70.21W,175C film limit;
  B=.1%,E=25ppm/K,EA=5000-piece reel. Body1.55+/-.05x.85+/-.10x.45+/-.10mm.
  https://www.vishay.com/docs/28758/tnpw_e3.pdf
- Maker-referenced pads, document28950Rev12-Jul-2022:0603IPC reflow gap.70,
  pad.90x1.00,overall2.50mm,centers+/-.80mm. This is not exactly the existing
  CRCW module's.75x1.00 pads at+/-.75mm. The integration writer must review the
  new footprint/courtyard and run fresh native checks; no mere name-only match.
  https://www.vishay.com/docs/28950/recsoldpaddims-drabeyresfus.pdf
- Rubycon BXW leakage source used only to motivate a witness sensitivity:
  https://www.rubycon.co.jp/wp-content/uploads/catalog-aluminum/BXW.pdf

Purchase-page checks21November2026: exact MPNs have cut-tape MOQ1routes atDigiKey.
Retrieved pages are crawled snapshots, not live or reserved stock. Reported1590
CRCW and4793TNPW units were visible in snapshots crawled last month; recheck at
procurement. No order, cart, supplier communication or sourcing reservation occurred.

- https://www.digikey.com/en/products/detail/vishay-dale/CRCW2512422KFKEG/1173742
- https://www.digikey.com/en/products/detail/vishay-dale/TNPW060384K5BEEA/14544059
- CRCW LCSC listing C4347041 exists but snapshot displayed0stock; no equivalent
  JLCPCB inventory or PCBA acceptance is established for either selected part:
  https://www.lcsc.com/product-image/C4347041.html

TNPW2512precision feed alternatives are not adopted: current TNPWsheet has no2512;
legacy2512family is200V and would reduce the existing500V resistor capability.
The chosen approach retains the CRCW2512family and tightens only the low-voltage
R13part. All existing C16/C17 physical, thermal, fault, service, assembly and human
review conditions remain separate from these analytical bounds.

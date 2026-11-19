# Development history — not the active capture contract

This research records earlier alternatives and seeds. The authoritativeSC06-Bpartsetandpinsetsarebom-design.jsonandintended-connectivity.json. InparticularSCR/D2/R6-to-groundandactivecapacitorcrowbarareNOTselected.

# SC06 OVP engineering proposal — researcher handoff

Read-only with respect to shared CAD/repository. This note proposes a replacement network; coordinator integration and independent review are required. Calculated, not simulated or measured. No stage approval.

## Main decision

Use TLV6700DDCR as the actual overvoltage comparator and reuse ATL431BQDBZR as an always-biased nominal12.075V shunt regulator. This removes the former detector's sub-mA ATL431 accuracy assumption. The dedicated comparator threshold has a full-temperature specified interval. Normal maximum reservoir should remain below123V; rising OVP calculation is126.605–130.207V, nominal128.4V. Dynamic135V ceiling remains a physical qualification requirement.

## Exact candidate network and pin intent

All GND below means bridgeDC-, mains-referenced.

- Three series HV feed resistors: CRCW25126K98FKEG, each6.98k1%1W/P70, from COUT+ through two midpoint nets to VCC_OV. These replace the old two18k2010 feed parts. Manufacturer ordering code is valid; procurement/stock not established.
- UREG ATL431BQDBZR: pin1 cathode=VCC_OV; pin2 REF=RAIL_REF; pin3 anode=GND. RRTOP TNPW120638K3BEEA38.3k.1%25ppm from VCC_OV toRAIL_REF; RRBOT TNPW120610K0BEEA10k.1%25ppm fromRAIL_REF toGND. No direct cathode capacitor.
- Comparator supply isolation: RC0805FR-07100RL100ohm fromVCC_OV toVDD_COMP; GRM21BR71H104KA01L100nF50VX7R fromVDD_COMP toGND, close toUOV.
- UOV TLV6700DDCR, TSOT23-6: pin1OUTA explicitly unused/NC; pin2GND=GND; pin3INA+=GND; pin4INB-=OV_SENSE; pin5VDD=VDD_COMP; pin6OUTB=OV_LOW. INA+ tied low defines unused channel; OUTA left unconnected, not relabeled as a different pin type.
- OVP divider: two TNPW1206160KBYEA160k.1%10ppm in series fromCOUT+ throughOV_MID toOV_SENSE; TNPW12061K00BYEA1k.1%10ppm fromOV_SENSE toGND. CodeY is10ppm; X is15ppm; E is25ppm. Do not accidentally useBY parts as25ppm orBE as10ppm. Current at128.4V=.4mA. Each top resistor dissipates~25.6mW nominal and~28.4mW at135V.
- QOV BC857B,215: pin1B=PNP_BASE; pin2E=VCC_OV; pin3C=GATE_SOURCE. RC0805FR-0722KL22k fromPNP_BASE toOV_LOW; RC0805FR-0710KL10k fromVCC_OV toPNP_BASE.
- Startup-blocking candidate DZSTART BZX58550-B3V3,115: pin1K=GATE_SOURCE; pin2A=GATE_ZOUT. RC0805FR-073K3L3.3k fromGATE_ZOUT toSCR_GATE. This is reversed into Zener operation during an asserted trip. Retain RC0805FR-071KL1k fromSCR_GATE toGND andGRM21BR71H104KA01L100nF in parallel.
- Retain R6 AC05000004700JAC00 and the existing AN60Fig8 discharge/latch path. Exact SCR X0202NN5BA4 pad mapping must be verified by the schematic/library owner against ST pin graphic; this research does not manufacture a verified library symbol.

## Calculations

OVP: useVIT+=396–404mV,2x160k/1k, independent resistor error .1%+10ppm*100K=.2%, and input-current screen±15nA. Vtrip=VIT*(1+Rtop/Rbottom)+Iin*Rtop. Result126.605322–130.206966V; nominal128.4V. This is a component-tolerance/static calculation using TI's input-current table value (specified test input0.1V); include any required bias-condition extrapolation and long-term resistor drift in independent review. Even a .1% additional per-arm aging reserve leaves a useful static margin, but recalculate rather than silently accepting it.

Rail regulator: initialVref2.487–2.512V; temperature reserve±34mV; cathode-voltage reserve27mV on the low side; rail-divider individual .1%+25ppm*100K=.35%; Iref up to200nA. Initial conservative result11.6528–12.3734V before small dynamic-load error; carry11–13V for preliminary current screens. ATL431 minimum35uA is an operating threshold, not the same as its1mA precision test condition. The feed below deliberately budgets≥1mA at the OVP operating point.

With a deliberately broad ±3% additional feed/gate/base resistance reserve, atVcap123V,VCC13V,Rfeedhigh3*6980*1.01*1.03, feed current≥5.049605mA. Upper loads with3.3k gate resistor and a modeledDZSTART minimum2.8V must be recalculated against the narrower actual rail bound; do NOT reuse the old4.3k/no-Zener load result. For reference, the old4.3k/no-Zener network upper load was4.046675mA, leaving1.00293mA. A conservative upper bound atVCC12.38V withDZSTART2.8V: gate-path current≤(12.38-2.8)/(3300*.99*.97)=3.02297mA; base-path current≤12.38/(22000*.99*.97)=.58601mA; rail-divider≤.2573mA; comparator≤.013mA. Total≤3.880mA. At123V and12.38V feed≥5.078mA, leaving≥1.198mA forUREG. Rail bypass current13uA gives100ohm drop~1.3mV nominal.

Each6.98k feed part at135V,VCC11V and low-resistance budget dissipates approximately .254882W. CRCW2512P70=1W; linear125C allowance is.352941W (before mounting verification), preferable to2010's .264706W. Normal120V input and12.075V rail: feed5.154mA, totalfeed-resistor heat.556W, supply input power.6185W. Actual low-voltage-rail load is part of that supply input; do not add it again. OVP HVdivider adds~.374mA at120V;44kbleeder adds2.727mA. LED55mA therefore requires approximately63.255mA driver output at120V. If LED60mA, approximately68.255mA. Recenter the CC design rather than retaining the old55/61mA driver setting.

Gate withstartupZener: usingVCC11.65V,VCEsat.3V,VZSTART3.8V,VGT.8V, RGhigh3300*1.01*1.03 andRGKlow1000*.99*.97 givesIG≈1.132mA after the1k bleed. These are engineering envelopes forZener/BJT, not guaranteed full-temperature limits from their25C tables. WithoutstartupZener and with4.3k, the previous broad11Vrail screen gave1.380mA. Do not combine these two configurations' numbers.

## Startup, stability, and limits

The series3.3VZener is a reasonable draft barrier to gate drive while the supply is very low. It is not a mathematical full-temperature false-trigger proof: its leakage specification is at25C and TLV6700OUTB is indeterminate belowPOR. Above1.8V supply, allow450us maximum startup settling perTI before treating comparator output as valid. Test slow/fast ramps, interrupted mains, bounce and brownout; verify no spurious SCR latch, no gate overstress and correct rearm. Until these tests, do not claim automatic startup/restart guaranteed. No broad claim of a guaranteed9–14VZenerrail is retained.

The100ohm isolated local100nF branch follows TI's series-resistance remedy for capacitive shunt-regulator loading. Avoid putting this capacitor directly onUREG's cathode; verify phase/transient behavior on the actual circuit. The bypass is on the comparator only, so it does not need to supply the several-mA SCRgate drive. The comparator's specified18us propagation figure requires its stated overdrive/load conditions; it is not a guaranteed135V overshoot bound under this circuit's different conditions.

STX02 tableIGT200uA,IL6mA,IH5mA applies25C unless stated. Temperature curves can inform the cold-current engineering reserve but cannot be relabeled as a tabulated full-temperature guarantee. The proposed~1.1mA gate is a substantial design reserve, not proof. R6 holding/BP shutdown and continued primary-feed power require the full LYT waveform analysis/test. No driver-off-before-release, nohot-pulse and no135Vdynamic claim is invented by the comparator change.

## Primary references

- TI TLV6700 RevB: https://www.ti.com/lit/ds/symlink/tlv6700.pdf — thresholds, comparatorpolarity,pins,operatinglimits,startup.
- TI ATL431 RevE: https://www.ti.com/lit/ds/symlink/atl431.pdf — exactBQ,pins,shuntaccuracy,current,stability.
- TI SLVA685: https://www.ti.com/lit/an/slva685/slva685.pdf — stability and series resistance to capacitive loads.
- Vishay TNPW28758 Apr2026: https://www.vishay.com/docs/28758/tnpw_e3.pdf — .1%,Y10ppm ordering and resistance ranges. New codes are manufacturer-ordering candidates, not asserted stock.
- Vishay CRCW20035 Apr2026: https://www.vishay.com/doc?20035 —2512rating/derating and ordering.
- Nexperia BC857: https://assets.nexperia.com/documents/data-sheet/BC856_BC857_BC858.pdf
- Nexperia lowcurrentZener: https://assets.nexperia.com/documents/data-sheet/BZX58550_SER.pdf
- STX02 Rev7: https://www.st.com/resource/en/datasheet/x02.pdf
- ExactJLC comparatorC2868382: https://jlcpcb.com/partdetail/TexasInstruments-TLV6700DDCR/C2868382 —Extended,Economic/Standard SMT permitted; stock/price not exposed/verified.

No orders, supplier contact, CAD edits or physical tests. Exactparts remain procurement-unverified; network remains an engineering candidate for integration and independent review.

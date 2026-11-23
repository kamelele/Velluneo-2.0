# Płytka TME — SC10-TME-A

Separate native KiCad10.0.6 design candidate with a complete routed board. **NOT FOR ORDER OR POWERED TEST.** The accepted SC09_compact and main remain unchanged; its manufacturing acceptance is not transferred.

PCB: **51.2 × 37 × 1.6mm, 2 copper layers, 1oz**, manual assembly. Proposed total component/board envelope approximately **27mm**, with all tall THT parts on the front. This exceeds the former33mmwidth/20mmheight targets; finished bulb fit is not established. J1ACinput is at the right edge, J2LEDoutput at the left.

Input target207–253VAC/50Hz. Nominal calculated output60V/135.2mAtotal, approximately133.4mAexternalLEDafterbleeders. External20SLEDmodule,4000KCRI>=80,~800lm remains an unmeasured optical target. Output is mains referenced, notSELV. No dimming. Lab ambient0–40°C; component temperatures, losses and efficiency are not measured.

23fitted electronic positions use16unique catalogue MPNs; J1/J2 are direct insulated-wire solder pads. No custom-wound part: MYRRA74089 is used on its primary only as an energy choke, with unused windings open. Every selected MPN has a TME offer below. Some stock figures are cached: **current positive stock for all16MPNs has not been established**. Seeengineering/procurement.TME-A.json for exact quantities, MOQ and dated freshness.

## TME parts

- F1: **1 × 37301000410** — [TME](https://www.tme.eu/en/details/37301000410/fuses-tr5-fast/littelfuse/).
- R1: **1 × PMR03SJ0151A19** — [TME](https://www.tme.eu/pl/details/pmr3s-150r/rezystory-tht/royalohm/pmr03sj0151a19/).
- RV1: **1 × B72207S0271K101** — [TME](https://www.tme.eu/en/details/siov-s07k275/tht-varistors/tdk/b72207s0271k101/).
- BR1: **1 × MB10S-13** — [TME](https://www.tme.eu/en/details/mb10s-13/smd-tht-sing-phase-diode-bridge-rectif/diodes-incorporated/).
- C1, C4: **2 × R71PF315050H6K** — [TME](https://www.tme.eu/en/details/r71pf315050h6k/tht-film-capacitors/kemet/).
- U1: **1 × LYT1603D** — [TME](https://www.tme.eu/en/details/lyt1603d/led-drivers/power-integrations/).
- C5: **1 × CL21B475KAFNNNE** — [TME](https://www.tme.eu/en/details/cl21b475kafnnne/mlcc-smd-capacitors/samsung/).
- R4: **1 × ERJ6ENF1242V** — [TME](https://www.tme.eu/en/details/erj6enf1242v/smd-resistors/panasonic/).
- R5: **1 × CS06FTFUR680** — [TME](https://www.tme.eu/en/details/cs1206-0r68-1%25-hp/smd-resistors/viking/cs06ftfur680/).
- R6: **1 × 1206S4F365KT5E** — [TME](https://www.tme.eu/pl/details/smd1206-3.65r-1%25/rezystory-smd/royalohm/1206s4f365kt5e/).
- D1: **1 × US1M-13-F** — [TME](https://www.tme.eu/en/details/us1m-13-f/smd-universal-diodes/diodes-incorporated/).
- C6, C7, C8: **3 × UHE2A470MPD** — [TME](https://www.tme.eu/en/details/uhe2a470mpd/tht-electrolytic-capacitors/nichicon/).
- R7, R10, R11, R12: **4 × RC1206FR-0797K6L** — [TME](https://www.tme.eu/en/details/rc1206fr-0797k6l/smd-resistors/yageo/).
- R8, R9: **2 × RC1206FR-0768KL** — [TME](https://www.tme.eu/en/details/rc1206fr-0768kl/smd-resistors/yageo/).
- L1: **1 × COIL1010-3.3** — [TME](https://www.tme.eu/en/details/coil1010-3.3/inductors/ferrocore/).
- T1: **1 × 74089** — [TME](https://www.tme.eu/en/details/74089/pcb-transformers/myrra/).

## Verification and release limits

Native ERC/DRC, exact graph and routing checks are recorded in the adjacent workflow packet. A clean manufacturing DRC is not functional insulation or product safety qualification. Seeengineering-status.json for unclosedT1faultcurrent,L1plug-intransients,fuse/resistor/MOVcoordination,fullfunctionalclearance and hotcurrent/OVP/ripple/thermal measurements. The conservative231-pair spacing assessment has no inheritedpackage exceptions or approval. Local3Dmodels are illustrative engineering envelopes, not certified supplierSTEP geometry.

Native project: Plytka_TME.kicad_pro. Workflow and views: ../../../workflow/integrated-shade/tme-board (repository-relative path; use the workflow link from the task handoff). No supplier upload, order or powered test performed.

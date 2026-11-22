# SC09-ROUTE05 parts and purchasing review

Actor: `/root/r05_parts`. Input: commit `d011ef6a865f6dd7f06825f233b2465238ecba27`, active CAT01 BOM, PCB SHA256 `9b73c61c34dc28fceff2e9d2265fcfb1280053245c9840f4e7c0bb39d782fa87`. Scope: engineering desk review for a bare PCB prototype assembled manually. No CAD, BOM, supplier cart or order was changed.

The existing 16 catalogue MPNs cover 17 electronic positions. No component substitution is needed for this review. Native inspection confirmed all 19 references, 46 physical pads, exact MPNs and BOM pin assignments. The four critical U1/BR1/D1/T1 land size sets match the primary manufacturer land basis. A matching BOM comparison is separate from independent circuit-intent verification.

## Purchasing routes

Each item below is a specific catalogue component, not a custom-made winding. Exact current stock is not reserved. Fresh public HTTP offers, cached product pages and manufacturer stock feeds have different freshness; the JSON records preserve that distinction.

- RF1 — `FW20A10R0JA`, one per board: [DigiKey](https://www.digikey.com/en/products/detail/bourns-inc/FW20A10R0JA/3777398). Retrieved product index reports 81,699; fresh LCSC offer is zero. Use the 2 W fusible 10 Ω, 5% part, not a generic resistor.
- RV1 — `V275LA4P`, one: [LCSC C129558](https://www.lcsc.com/product-detail/C129558.html). Fresh response reports 3,970; minimum five pieces. Keep the actual staggered lead form.
- BR1 — `MB10S-13`, one: [LCSC C460887](https://www.lcsc.com/product-detail/C460887.html). Fresh response reports 5,285. Other manufacturers' MB10S numeric pin identities are not automatically interchangeable.
- C1 — `B32529E6473K189`, one: [DigiKey](https://www.digikey.com/en/products/detail/tdk/B32529E6473K189/18718969). Retrieved product index reports 5,750. This is a post-bridge 47 nF/400 V film capacitor, not an across-line X capacitor.
- L1 — `768772332`, one: [DigiKey](https://www.digikey.no/en/products/detail/w%C3%BCrth-elektronik/768772332/16910471). Retrieved product index reports 142. Würth's primary datasheet specifies 3.3 mH, 400 V and a 1.2 mm hole/P5 pattern.
- C4 — `B32671P6154K000`, one: [DigiKey](https://www.digikey.si/en/products/detail/tdk/B32671P6154K000/3878304). Retrieved exact product index reports 13,460, EUR 0.92 for one or EUR 0.586 each at ten. TDK's separate manufacturer feed lists DigiKey stock 13,275, updated 2026-10-23; fresh LCSC stock is zero. These snapshots are not a reserved checkout.
- U1 — `LYT1603D-TL`, one: [LCSC C567687](https://www.lcsc.com/product-detail/C567687.html). Fresh response reports ten exact parts. [TME LYT1603D](https://www.tme.eu/en/details/lyt1603d/led-drivers/power-integrations/) reports 80 in a fresh response; the manufacturer datasheet identifies the blank suffix as standard packaging and `-TL` as tape/reel, with the same 1603 die and SO8 package. This packaging alternate was identified, not applied to the BOM. Do not blindly substitute LYT1604.
- C5 — `CL21B475KAFNNNE`, one: [DigiKey](https://www.digikey.com/en/products/detail/samsung-electro-mechanics/CL21B475KAFNNNE/3888627). Retrieved product index reports 232,263; fresh LCSC stock is now zero.
- R4 — `ERJ-6ENF1242V`, one: [DigiKey](https://www.digikey.com/en/products/detail/panasonic-industry/ERJ-6ENF1242V/119288). Retrieved product index reports 20,881.
- R5 — `RL1206FR-7W0R68L`, one: [LCSC C859937](https://www.lcsc.com/product-detail/C859937.html). Fresh response reports 3,830. `0R68` is 0.68 Ω; `0R068` is the wrong value.
- R6 — `CRCW12063R65FKEA`, one: [Mouser](https://www.mouser.co.uk/en/ProductDetail/Vishay/CRCW12063R65FKEA?qs=a87eylGnD3%252BEdqERjdagRQ%3D%3D). Retrieved product index reports 14,174. Direct HTTP returns an access-denied page, so that response is not live stock evidence. `3R65` is 3.65 Ω; `3K65` is wrong.
- D1 — `US1J-13-F`, one: [LCSC C85095](https://www.lcsc.com/product-detail/C85095.html). Fresh response reports 27,435. Preserve Diodes Incorporated's exact lead-free SMA part and cathode identity.
- T1 — `MSS1210H-125KED`, one: [Coilcraft](https://www.coilcraft.com/en-us/products/power/high-voltage-inductors/mss-mos-%281%29/mss1210h/mss1210h-125/). Manufacturer buy route lists quantity one at USD 3.68. Its numeric stock is not exposed reliably by the static page. A six-day-old Coilcraft Direct feed on [Findchips](https://www.findchips.com/search/10h12) reports 1,077. This is lower freshness than a live checkout, and is not a reservation. Do not omit the `H` from the MPN.
- C6 — `EEUFS2A151`/distributor formatting `EEU-FS2A151`, one: [DigiKey](https://www.digikey.com/en/products/detail/panasonic-industry/EEU-FS2A151/9597035). Retrieved product index reports 566. Do not substitute the longer `L` variant or a changed lead-form suffix without review.
- R7 — `HVR2500003903FR500`, one: [DigiKey](https://www.digikey.com/en/products/detail/vishay-beyschlag-draloric-bc-components/HVR2500003903FR500/719816). Retrieved product index reports 17,138. The selected family is HVR25, not the old VR25.
- R8 and R9 — `RC1206FR-0768KL`, two: [LCSC C137239](https://www.lcsc.com/product-detail/C137239.html). Fresh response reports 93,700. Keep both parallel bleeders.

Fresh exact public HTTP responses were captured on 2026-11-22 around 18:00–18:01 UTC, with matching response dates. Six unique selected MPNs have fresh positive stock: RV1, BR1, U1, R5, D1 and R8/R9. Other sources are explicitly indexed or manufacturer-feed evidence. U1 stock ten can cover five boards plus limited spares, but ten boards leave no spare margin. Reconfirm stock, minimum quantities and shipping at checkout; no purchase was performed.

## Electrical and assembly desk checks

At 253 V RMS, the sinusoidal line peak is 357.796 V. This is below the normal DC ratings of the 400 V input components, 600 V diode and 725 V MOSFET. It does not prove ripple, abnormal surge or fault coordination. The MOV's specified 710 V clamp at 10 A leaves little margin to 725 V; its clamping value is not a guarantee for arbitrary surge current or layout overshoot.

C1's full 400 V category rating applies through 85°C. The manufacturer's derating gives only 325 V at 100°C, so no 100°C/full-400-V claim is acceptable. An 80°C prototype stop ceiling is proposed for the coordinator's test plan, pending actual temperature and waveform measurements. Other conservative power screens and manufacturer limits are in the JSON. They are calculations, not measured temperatures or waveform simulations.

Würth gives L1 lead diameter 0.7 mm as a reference, not a guaranteed maximum. The board follows its recommended 1.2 mm hole/P5 pattern. Actual sample gauging and gentle free-lead adjustment remain normal preassembly checks. HVR25's lead maximum is 0.63 mm; a 0.9 mm nominal hole with JLC's stated −0.08 mm tolerance leaves 0.19 mm diametral margin. C6 needs the documented horizontal forming/support and clear vent reserve; its sleeve provides no insulation credit.

U1, BR1 and D1 primary pin identities are retained. U1's bypass capacitor remains on the same face with the current layout requirements. LYT1604 has a higher auto-restart current range (1.61–1.88 A versus 1.06–1.24 A), so availability alone does not justify that substitution.

## Documentation finding and remaining test scope

`PART05-05` is independently verified closed for the T1 procurement/specification scope. The current specification now identifies catalogue `MSS1210H-125KED`, current PCB dimensions are 51.2 × 33 × 1.6 mm, the earlier pre-CAT01 specification is preserved as historical evidence, and the old custom-winding contract is explicitly superseded and forbidden for current procurement/assembly. Exact inspected file hashes are recorded in JSON. This role did not edit those source files.

The native parts check was rerun after adoption of the ROUTE05 board, SHA256 `3b9188b60e65c67e45f43cd6b55243fc1fee33aa202559efe423ba11768e97f3`. It still passes for all 19 references, 46 pins, exact MPNs and the four critical land size sets. The larger outline and the R4 track escape correction do not require electronic component substitutions.

Physical current, ripple, OVP, discharge, temperature, fault, surge, EMC and insulation tests belong to controlled post-fabrication laboratory work. This report neither fabricates those results nor treats an unmeasured prototype as a qualified lamp. The coordinator and independent reviewers must bind the final integrated geometry and manufacturing files. This report gives no human stage approval and performs no supplier upload or order.

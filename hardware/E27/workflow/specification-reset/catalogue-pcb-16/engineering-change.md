# C16 — integrated factory-part PCB correction

The owner requested correcting the transformer fault-current incompatibility and
transistor clearances, updating the actual PCB for purchasable parts, GitHub and a
preview. Base a9a8fc94701ad6b221f2737654bf0822c8d04da3. Historical RFQ13/JLC14
manufacturing packages are NOT valid for this changed circuit.

MYRRA74032 replaces74215: factory-wound E25,72/10/18 turns,1.1mH+/-10%,1.1Apk,
26.5x22.5x26.5mm maximum. No winding work is requested. Primary3(DRAIN,dot)-5(BULK),
aux2(AUX_RAW,dot)-1(PGND), secondary6(SECONDARY_RAW,dot)-10(OUTPUT_NEG).
Pin4 physically absent;7/8/9 physically present and externally unused, no winding
shown. The component-side footprint orientation is established by the primary front elevation
(1left/5right); the unlabeled pin plan must be interpreted as BOTTOM view. The
first interpretation was mirrored, caught by independent final review and corrected
before publication. checks/T1-top-view-verification.json verifies every saved pin. Oval lands
1.95x2.30/hole1.40 retain3.05mm primary pad gap and12.94mm opposing-row gap.

STFW2N105K5 TO-3PF replaces the incompatible DPAK:1050V,8ohm maximum at10V,
Qg10nC TYPICAL. Straight G1/D2/S3 leads at5.45mm,round2.35mm lands/hole1.70 give
3.10mm nominal copper gap. Neither customer bending nor a package-local waiver.
The minimum pitch5.35 minus maximum shoulder width2.20 gives conditional3.15mm
metal separation. Independently inspect actual drawing/first-fit centering before
production acceptance. Lowest wide shoulder must be>=3mm abovePCB; the plastic
body bottom is then about6.5mm, assembled maximum reservation29.7mm. This is NOT
an accepted fit inside the complete60x120mm lamp.

R4=53.6k,R5=20.0k,R6=2.00k,R9=1.80ohm; exact100ppm/1% Vishay MPNs are in BOM.
The independent map precedes capture.33positions/80physicalpads, including2wire
pad pairs;28SMT electronic positions and3THT electronic parts(T1,Q1,C1).

The old static fault screen0.627A exceeded the old transformer0.50Apk rating.
The new screen is0.908A static and1.05252A with an allocated400ns extra current
ramp at253Vac,LPmin0.99mH,RCSmin1.7622ohm. Calculated delay frontier531.37ns.
TI's unblanked additional OCP stops switching and enters UVLO/restart. Its1.6V
maximum is not marked as the jitter-average normal-CS parameter. However TI does
NOT publish a guaranteed maximum total OCP propagation/turn-off time.400ns is a
prototype acceptance allocation, not a claimed manufacturer guarantee. The static
rating incompatibility has a design correction; fault qualification remains open.
This calculation does not bound internal shorts/failed sensing/all component faults.

Nominal analytical interface19..22V/about319mA, conditional303.6..336.1mA at
assumed transformer efficiency0.9. This revises an analytical candidate, not the
owner750..850lm lamp requirement. No selected qualified optical panel is claimed.
Worst independent frequency sensitivity113.25kHz is below120kHz minimum maximum
frequency. CV nominal26.03V; low/high first-order corners24.48..27.61V. VDD low
screen at19V is9.833V; target healthy minimum9.45V. C2+C3=.94uF C0G stays within
TI's1uF recommendation. Prior conservative budget gives approximately2.15ms hold
at10nC/1.59ms at20nC, versus about0.77ms unloaded output charging to auxiliary
takeover; this is conditional on the actual LED load/startup trajectory.

R10 is the4.7ohm AUXILIARY series resistor, NOT a clamp/snubber resistor (CAT15
label corrected). Clamp is D1+SMBJ160A returning locally to BULK, adjacent toT1.
MYRRA leakage/DCR/saturation curves are unpublished; actual clamp peak, TVS pulse
energy, damping and hot-fault behavior require characterization. The MOSFET voltage
rating alone is not a clamp qualification. Current-dependent C4/D3 first-order RMS
screens remain within selected ratings; actual ringing and thermal rise remain due.
Cold ideal inrush8.01A/.0258A2s/1.152J is below bridge nonrepeat surge screen,
but F1 typical meltingI2t is not guaranteed clearing coordination. R1 is not claimed
fusible. No physical test or TINA-TI run is fabricated.

The saved board is45x60mm,4layers. Keep3mm HV/quiet,10.7mm P/S copper floor and
the all-layer isolation band. Actual native effective-shape audit measures11.146726mm
projectedP/S and3mm common-layerHV/quiet; HV/quiet crossings on different layers
exist and are not claimed absent. Dedicated positive sense travels onIn2; separate
power/charge/quiet/aux return branches converge in a finite2mm region atC1minus.
This is not a perfect mathematical two-wire Kelvin pair or a measured EMI result.
C1 is now front-mounted; its10.5mm body circle has no unrelated F.Cu. All54 routing jobs are
captured; actual native ERC/DRC/parity and graph comparison are authoritative.

The toolkit initially refused the obsolete non-existent T1Pad3 NC net pattern.
Bounded manual cleanup deletes only that literal;784 real directed net cases
including empty/unknown retain identical effective clearance. Native floors,
severities, area scope and waivers are unchanged. Reviewed configure preview then
explicit apply f7e48a9e / transaction6dc59bc8 generates current ownership and
adapter contracts. The route engine used explicit numeric constraints before
managed contracts were refreshed; no false claim of consuming their later digest.

Release remains blocked by unperformed physical/insulation/process/lamp tests and
missing revised human stage approvals. Toolkit reports these as failures. The
owner authorized drafting this PCB, not manufacturing approval. No order, supplier
message, cart, payment, upload BOM/CPL or replacement Gerber package is created.


Final layout correction: the controller and positive-sense routing are moved beside
Q1/shunt; C1 is front-mounted, BR1 rotated180degrees and the input connection is at
the lower edge. The R1 courtyard follows the union of its actual body and factory
SMD wings, retaining0.25mm body and0.5mm land margins; its copper is unchanged.
C1 uses a circular5.75mm-radius courtyard around the10.5mm body reservation,
replacing an oversized rectangular corner envelope. No electrical clearance floor
or check severity was relaxed. A source-bound local Kelvin via offset clears C2;
native full-board DRC verifies the final result. The final copper object count is333.

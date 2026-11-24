# SB01 R2 — same-board RC startup correction candidate

The physical legacy **L1** position is now populated with **PR02FS0201000KR500,
100 ohm, 10%, 2 W**. It is called R10 in the engineering calculations only.
Its L1 reference, local-library identifier and original two pads are deliberately
retained to match the existing PCB/silkscreen and manual assembly location.
The custom two-terminal zigzag symbol now shows the resistor value and datasheet.
Do not fit the old 768772332 choke at this position in the R2 assembly.

RF1 remains the selected 47 ohm protective fusible resistor. No net, pin, copper,
via, outline, mask or legend change is intended. The new resistor body/model is
an engineering assembly representation, not a manufacturer-qualified fit model.
The <=16mm formed-resistor height stays within the retained19.5mm module envelope;
actual lead forming/support and hot clearance still require a sample inspection.

The passive RC model removes the original deliberate LC energy exchange.
It does not model silicon switching, parasitic inductance, EMC or finished faults.
New source and assembly evidence invalidate prior exact-source release acceptance.
Native checks and artifact comparisons must be rerun; existing Gerbers may be
retained only if full copper/mask/outline/drill identity is proved.

Cold normal startup pulse support is based on the exact PR02-FS primary curve.
Full hot pulse capability, operating RMS/temperature, surge, output OVP dynamics,
LED current, MOSFET-short consequences and EMC remain measurement gates.
This candidate does not authorize a supplier order, powered testing or product use.

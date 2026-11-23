# SC09 before the actual 2 mm controller redesign

The exact pre-change design is preserved at commit
[d910b241f21cc5faefd6ba4ea5ab30dcd878262d](https://github.com/kamelele/Velluneo-2.0/tree/d910b241f21cc5faefd6ba4ea5ab30dcd878262d/hardware/E27/variants/integrated-shade/SC09_compact).
Its PCB SHA-256 is `a66e97b16b16b1dc667aeb59bcfa512543c749aff0824d9455ca29513e223f19`.
The accompanying manifest identifies the 149 retained source/artifact files. The local
archive is `outputs/SC09_przed_poprawa_odstepow/SC09_przed_poprawa_odstepow.zip`.

The original source is not overwritten by the ongoing engineering work. This
checkpoint does not approve its old Gerbers: the original conservative spacing
screen still has 23 findings, including intrinsic package land gaps.

The owner explicitly chose: **“Zmienić sterownik — rzeczywiste odstępy 2 mm”.**
The new SC09-SB02 engineering candidate uses a DIP controller, a different bridge
and a manufacturer-verified high-voltage diode land pattern. It is a circuit
redesign, not a rule waiver or shrinking of manufacturer pads. The complete new
independent graph and its 190-pair screen are being checked before routing.

The target remains a compact bare laboratory PCB with manual assembly, 230 V / 50 Hz
input, 207–253 V calculation range, and 0–40°C ambient. The new design is not
approved for manufacturing or energization at this checkpoint. No order or powered
tests were performed. Main remains outside the write scope.

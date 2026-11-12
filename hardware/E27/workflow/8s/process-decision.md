# Owner decision on E27-8S-SPEC revision 2

On 2026-11-12 the Velluneo project owner replied “okej kontynuuj” to the request to approve the 8S specification and the proposed JLCPCB process before schematic work. The reviewed intent digest was `42fba813be0bb01826ab7b7f688270b926d10379f9c60d61f1549ab2539b692c`. [Reviewed packet](https://github.com/kamelele/Velluneo-2.0/blob/3013cb6665b9d6642fdcd3becdd5d3956cd832c8/hardware/E27/workflow/8s/stage-packet.md)

Accepted for design planning are a single 8S current-regulated output, a single power PCB as the packaging objective, and the proposed JLCPCB routed FR-4 process with two layers, 1.6 mm thickness, 1 oz outer copper, lead-free HASL and Standard PCBA. Published JLCPCB capabilities support the selected process. The exact laminate and stackup, order-specific assembly scope and panel remain subject to the requirements at placement and release. [Process proposal](profile-proposal.md) · [JLCPCB fabrication](https://jlcpcb.com/capabilities/pcb-capabilities/) · [JLCPCB assembly](https://jlcpcb.com/capabilities/pcb-assembly-capabilities)

The next bounded task is schematic preparation. Confirm the driver-to-insert interface, cold operating envelope and independent pin intent before generating a new KiCad schematic. Physical measurements and supplier order authorization require separate evidence.

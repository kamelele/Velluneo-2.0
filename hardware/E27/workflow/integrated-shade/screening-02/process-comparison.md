# IS-PROCESS-02 — Economic versus Standard PCBA

Owner requested comparison before process selection,2026-11-19. Neither process is approved. Study quantities10 and100 finished drivers are comparison scenarios, not orders. No Gerber/BOM/CPL quotation was submitted.

## Recommendation

Economic PCBA is the first candidate for a single-sided compact driver, subject to every exact part and tooling/process check. Standard remains the alternative for two-sided placement, Standard-only components, V-cut or a better complete quote. Through-hole parts by themselves do not force Standard. Both services support mixed assembly; actual handling of each selected THT line must be confirmed.

The official capability page lists Economic single-board minimum10x10mm versus Standard70x70mm handling size; thus a potential40x25mm finished outline is not automatically disqualified. Source: https://jlcpcb.com/capabilities/pcb-assembly-capabilities . This does not establish fit or actual part eligibility.

JLC explains that removable rails can bring a smaller Standard assembly up to its handling size while preserving the original finished circuit-board outline. Ordinary5mm rails on two sides alone do not make40x25mm meet70x70mm; panel/tooling geometry must be checked. Economic tooling holes need deliberate safe placement, especially in a mains product. Source: https://jlcpcb.com/help/article/common-pcba-after-sales-issues-and-faq . Supplier-added holes/rails must be reviewed before manufacturing.

Economic accepts mouse-bite panels; V-cut requires Standard. A100-finished-unit study can consider50 two-up panels rather than dismiss Economic solely because its nominal order quantity is2–50. The quote must confirm panel count, actual panel dimensions and replicated assembly quantities. Sources: https://jlcpcb.com/help/article/pcb-panelization ; https://jlcpcb.com/help/article/pcb-assembly-faqs ; https://jlcpcb.com/blog/reduce-pcb-assembly-cost-prototype . No panel has been designed or accepted.

## Price illustration, not a quotation

Official price guide checked2026-11-19: setup8.18USD+stencil1.53USD Economic versus25.56USD+8.21USD Standard single-sided. The two-line subtotal is9.71USD versus33.77USD per accepted order. Dividing only that subtotal by10 finished boards gives0.971USD versus3.377USD, and by100 gives0.0971USD versus0.3377USD. These are NOT complete assembly prices and not savings guaranteed for this design.

The same guide lists Economic Extended loading3.07USD per line versus Standard1.53USD per Basic/Extended line. Apply actual BOM classification/counts. Other charges include PCB/panel, parts and attrition, SMT/manual joints, hand-solder labor, fixtures, handling, inspection and shipping/taxes. Some are conditional; the quote must resolve them rather than summing every line blindly. Source: https://jlcpcb.com/help/article/pcb-assembly-price . No exchange-rate conversion or unit production cost is claimed.

## Selection checks

Every orderable MPN/C-code must be matched directly to actual service eligibility, availability, package and placement side. Standard-only stock can defeat an otherwise Economic-compatible outline. Preorder/private inventory/global sourcing is possible but does not prove a particular part can be assembled under Economic or at a distributor's displayed price. Sources: https://jlcpcb.com/help/article/common-bom-and-cpl-matching-issues-and-explanations ; https://jlcpcb.com/help/article/how-to-use-my-own-parts-for-pcb-assembly-order ; https://jlcpcb.com/help/article/how-to-use-jlcpcb-global-sourcing-parts-service . No inventory was purchased or supplier contacted.

The process decision should cover the actual candidate BOM, sides, laminate/stackup/copper/finish, THT operations, panel/rails/tooling and inspection. Keep all mains spacing, thermal and accessibility requirements independent of service eligibility. No safety/EMC conclusion follows from manufacturability.

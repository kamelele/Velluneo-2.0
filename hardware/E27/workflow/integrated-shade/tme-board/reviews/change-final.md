# Change review — Płytka TME SC10-TME-A

Actor: /root/tme_change. Frozen source digest `86c78b4be01ec98c0227b2ce02a5600e4c6f7527d1007f378b6b368268d3d2a2`. Recommendation: **blocked for release or powered testing**. It is reasonable to save this exact candidate separately with its current draft status. This recommendation is not stage or manufacturing approval.

Independently verified all91source hashes,22artifact hashes and140preservedSC09source hashes. Fresh native netlist export agrees with independent physical-pin intent; the only Toolkit graph finding is missing actual approval. Native MPN fields and connected pad membership agree with the25-position BOM. All7NCwinding terminals remain unrouted. Fresh independent DRC reports0violations,0unconnected and0schematic-parity issues. Actualroutinginput digest/hash agrees with the implementer record; placement/routingconsumer documents are equal.

The original19references/46pins/126tracks/10vias become25references/65pins/190tracks/17vias. The new board is51.2×37×1.6mm,2layers. Read-only native inspection and semantic pin checks found no unexpected merge, missing physical pin, reversed output-capacitor polarity, custom-winding requirement or original-source mutation.

## CHG-HV-ROUTING — blocker

checks/functional-spacing.json: B.Cu /DC_RETURN pad D1.2 versus /BUS_FILTERED track64adb25b... has0.350001mm conservative drawn gap against2mm target.401object-pair hits over231enumeratednetpairs; affected41netpairs.

A native manufacturing-floor DRC pass does not establish functional high-voltage spacing. These are not solely unavoidable package-pin findings, and SC09exceptions/approval do not transfer.

Closure: Correct intercomponent/route spacing and independently rerun native matrix. Any remaining package/short-escape exception requires exact object/region electrical basis and actual authorized acceptance, not inherited SC09waivers.

## CHG-CHANGED-ELECTRICAL-ENVELOPE — blocker

New T1MYRRA74089 primary0.85A peak versus characterized ICfault1.06–1.24A. NewL1typ0.3A10%Ldrop versus ideal linear plug-in1.398A flag. New50A-breaking F100mA plus150ohm3W has no total-clearing/pulse coordination proof. Three47uF141uF aggregate and changed R6TCR invalidate earlier hot/ripple bounds.

Actual circuit/parts differ from approvedSC09:19refs46pins11nets becomes25refs65pins15functionalnets+7NC. Normal-model graph equivalence and fresh DRC do not qualify new faults, surge or thermal limits.

Closure: Close exact source/fault/current/voltage/hot/ripple acceptance conditions or redesign. Physical data and approved contained test conditions must precede energized validation; do not mark these PASS from images or normal-current margins.

## CHG-PROCUREMENT-FRESHNESS — major

All16selecteduniqueMPNs have exactTMEoffers,23electronicpositions; only a subset has direct23Novemberpositiveinventory. Other counts are cached and last batch stopped atR5HTTP429. No custom-woundpart remains.

A categorical all-components-currently-orderable claim is not established. Catalogue membership is established, current full-set stock/MOQ availability is not.

Closure: Confirm positive current prototype-quantity availability and purchase multiples for every exact selectedMPN; record timestamp and actual supplier part. No substitution without affected electrical/land checks.

## CHG-MECHANICAL-ENVELOPE — major

Saved four-edge rectangle51.2x37mm,2L1.6mm; oldSC09acceptedboard51.2x33mm. New total assembly reservation27mm exceeds20mmtarget. MYRRA22mm body plus0.5mmseating, board1.6mm and bottomBR12.9mm. R1uprightformedP7.5 remains sample/jig dependent.

New candidate is not a demonstrated drop-in mechanical replacement or proven ordinary-bulb fit; width grows4mm.

Closure: Retain actual target misses in user handoff. Before enclosure integration/assembly release, inspect exact samples, formedlead/vent clearances and agreed fixture/bulb envelope.

## CHG-NEW-ACCEPTANCE — major

Fresh independently exported physical-pin graph has only missing_stale_intent_approval finding; currentmap/spatialapprovalsnull; Toolkitwork/releaseFAIL. No originalSC09stageapproval transferred.

New candidate may be retained for review but cannot inherit old bare-board manufacturing authorization. Four agent recommendations are not human approval.

Closure: Present exact updated candidate and remaining limits for actual authorized stage/release review after technical blockers are resolved; never fabricate acceptance.

## Retained and invalidated evidence

SC09manufacturing acceptance is historical and does not cover these changed parts, map, placement or routing. Model-only root repair is explicit and the final manifest supersedes the implementer handoff model hashes; unchanged CAD hashes retain their narrower scope. Old55-pair and new231-pair clearance matrices differ, so raw finding counts should not be treated as a normalized ratio. The0.350001mm BUS_FILTERED-to-return route gap above is a concrete new-candidate blocker independently of those counts.

No remote main state was independently read in this review; root must finish branch/tree/main preservation checks at publication. No physical measurement, approval, supplier upload, order or energized test occurred.

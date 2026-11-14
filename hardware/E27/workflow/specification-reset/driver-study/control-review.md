# Current/startup/alternative review record

VEL-FLYBACK-CTRL-01 r1, 2026-11-14. Limited mathematical/specification investigation. No formal specification gate, human engineering approval, schematic approval or physical qualification.

## Frozen evidence

| File | SHA-256 |
|---|---|
| control-and-alternative.md | 50f0f119d63f0d17cb169a3723e56e77cbf6425d3db2065e82694df04915f9f9 |
| control.py | c4cc7e96c896f346f2fbba90479dd8824a018c48a23e054bba5446c4d1e1cf07 |
| control-results.json | 06dc2240c6291ea86699e5f57608cb150cb1b8b3016db8f54e59a70b003880f9 |
| upstream results.json from VEL-FLYBACK-01 r2 | 6435677103247ad888ab1bdf2078409f8a5ecadcf165749fc70191534f4addb3 |

The author executed the script successfully. Four separate read-only agent contexts verified the hashes, executed the script and reproduced the result file exactly, including the upstream dependency check. Their reviews cover the same frozen r1; no post-review changes to these three files were made.

## Actual independent agent reviews

| Role / context | Recommendation and checked evidence | Open findings / limits |
|---|---|---|
| Reality Checker /root/spec_reality | Ready for preliminary human discussion; equations/current, threshold, RC, delay and flux arithmetic consistent. | RC-CTRL-001 verify lower-threshold configuration, regulation/timing and external SCP together; minimum comparator trip about 0.264 A versus prior sampled normal peak about 0.249 A leaves unqualified margin. RC-CTRL-002 complete actual startup/auxiliary takeover/recovery model. RC-CTRL-003 fresh controller-specific DCM/magnetics/protection and sourcing analysis. |
| Overengineering Reviewer /root/spec_simplicity | Ready for preliminary publication; no unnecessary-circuit or premature-part blocker. | OE-LED-01 full BOM, transformer, startup, protection, sourcing, assembly and thermal comparison remains open before final selection. |
| Completeness Reviewer /root/spec_completeness | No completeness finding for this limited early study; quantitative summaries consistent and unmodeled behavior explicit. | Fault dynamics, current accuracy, startup transition and manufacturing remain deferred; no complete design inference. |
| Change Reviewer /root/spec_change | No requirement drift or false design approval against product packet r11; clear distinction between total secondary/LED current and screened/conditional power ratings. | No new Change finding. Formal stage and safety gates remain open. |

The original source PDFs were inspected by the author; none of these file-based independent reviewers independently revalidated manufacturer specifications. Mathematical reproduction does not validate a control loop, source accuracy, startup, protective action or physical safety. No human approval is simulated.

## Corrections and current engineering decision

An initial conversational interpretation of a small LYTSwitch-5 isolated-topology figure incorrectly mentioned a transoptor. The author reopened the full DER-528 circuit and description and explicitly corrected the statement before freezing this study. The reviewed document describes primary-side sensing without transoptor. No transoptor or secondary feedback network was added to the project.

Retain TPS92310 as a comparison, not a selection. Next calculate a fresh LYTSwitch-5 DCM candidate, checking whether LYT5225D suffices before treating LYT5226D as necessary. The previous CrM transformer is not transferred as an approved design. Actual current/optical bounds, fault interface limits, thermal/manufacturing feasibility, exact lifecycle/sourcing and toolkit/CAD prerequisites remain unresolved where previously recorded. The inaccessible AN-65 guide (HTTP 406) is disclosed; no completed manufacturer-tool workflow is claimed.

No CAD, supplier contact, purchase, BOM upload, SPICE, ERC/DRC, installed-toolkit environment pass or physical test occurred in this study.

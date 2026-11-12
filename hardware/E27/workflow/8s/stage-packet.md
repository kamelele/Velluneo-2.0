# Stage packet — E27-8S-SPEC revision 2

## Candidate and decision

- Scope is the specification for one series string of eight LEDs and one candidate power PCB. The project owner's 2026-11-11 chat message selects the architecture. Formal acceptance of this packet remains open.
- Velluneo base commit is `a8b2ee8fc110c338037cb6391b1e41e378b3445e`. The requirements revision is `8S-spec-2` and its intent digest is `42fba813be0bb01826ab7b7f688270b926d10379f9c60d61f1549ab2539b692c`. No new CAD source snapshot exists at specification.
- Toolkit ruleset 0.7.1, commit `86614c3b9b43713031e0ea481edbe26b71cd1b8f`, verified candidate package 0.7.1-preview.3. The CLI requirements check is independent of KiCad. Historical KiCad 10.0.8 checks are for the archived boards. Toolkit CAD checks require the matching 10.0.6 environment.

## Review and findings

Independent agents reviewed revision 1 against digest `403d227708ae8f510cae370ab69aedf635efeb28528a391a895122864efabc44`. Codex incorporated corrections and requested targeted read-only re-reviews against revision 2. The dispositions below distinguish documentation changes from outstanding evidence.

- Reality Checker `/root/reality` independently recalculated the optical scenarios, current-sense limits and discharge resistance. RC-1 now defines a measured flux/current matrix and bin selection. RC-2 now identifies cold-start acquisition and voltage-budget inputs. Both documentation findings are closed. The actual cold envelope and physical optical measurements remain open. RC-3 remains open pending process confirmation.
- Completeness Reviewer `/root/completeness` confirmed the revised mains, EMC and flicker traceability, insulation design inputs, electrolytic temperature and sample plan. COMP-03 and COMP-04 closed. COMP-02 remains open for the machine-readable interface before schematic work. COMP-01 remains open for fabrication and assembly confirmation.
- Overengineering Reviewer `/root/scope` confirmed the shared driver PCB, fixed current-setting and bin selection approach, and the separation of contact-side discharge from the upstream reservoir. OE-01 through OE-03 closed for documentation. Schematic and bench verification remain open.
- Change Reviewer `/root/change` matched the revision 2 requirements hash against the saved report. CHG-01 documentation is closed with the logical interface delta and the removal sequence. Physical pin mapping and the electrical envelope remain open before schematic work. CHG-02 is closed for the distinction between current process selection and later board-specific evidence. CHG-03 is closed with the indexed owner decision and historical Rev K/H scope. The reviewer delivered these findings in a review message before the session reached its usage limit.

The [requirements check](requirements-check.json) ran with `requirements workflow/8s --stage specification` using the verified toolkit source tree and returned exit 1. The current findings are `OPEN-PROFILE` and missing review evidence for `REQ-JLC`. The project owner can confirm the proposed process from the [profile proposal](profile-proposal.md). Board-specific evidence remains at the later gates recorded in the [requirements](requirements.json).

## Handoff and evidence

The [specification](specification.md) includes the calculation and bench plan. The candidate changes only workflow documents and contracts. Rev K/H remain the historical 2×8 reference and their CAD and manufacturing reports apply to that design. Before schematic work, review the cold electrical envelope, actual contact assignments and the separate shutdown and disconnect paths. Bench data is required to qualify the 8S optical and thermal performance.

Attachment SHA-256 values for revision 2 after LF line-ending normalization and rerunning the requirements check. The reviewed wording and intent digest are unchanged.

- `specification.md` — `aaa6cfadcc5bf7dd76286891a27d5f438ac71f174256cf9948cbcaf177b07662`
- `requirements.json` — `82ccaee2a16e659424f5c15c18f97675657f77408b7d674c65a156016f3a519c`
- `hardware.json` — `4fa7446dc1ea39af8cbd0f758455b23eb1768ef48d5b80b1e051369f442bc205`
- `requirements-check.json` — `553200561a84ff05015edb3b3ff071cdf731e8a03a3c7135c09eacf758ed2ae4`
- `profile-proposal.md` — `5c5b2e5da676edcc049ed10e85fd2a4dd523ed240b46cdf3bbaef212bb846d45`
- `task-contract.md` — `328102ca59ce372a409733e5ad85f3f3d37790828e20c7a753f144de2749ddb4`

## Human decision

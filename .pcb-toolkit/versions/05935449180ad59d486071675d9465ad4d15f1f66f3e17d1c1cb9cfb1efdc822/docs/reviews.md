# Evidence for stage reviews

For placement/routing, attach the approved spatial intent, resolved constraints digest,
configure preview SVG/diff, actual saved geometry report, exact consumer input digests
supplied to adapters and fresh DRC. Review footprint sides/heights separately from the
2D envelopes. Block cards must cover sensitive signals, switching nodes, return paths,
loops and Kelvin topology with the linked requirement evidence. Spatial agreement does
not certify SI/PI/EMC or actual external router behavior. See
[shared spatial constraints](spatial-constraints.md).

At schematic review and every affected later review, attach the independent intent
revision/digest, real approval evidence and fresh connectivity report/export hash.
Review its basis separately from CAD. Resolve pin/unit, NC, merge/split and separation
findings even when ERC and schematic/PCB parity pass. Graph agreement is not proof of
function, correct MPNs or insulation. See [connectivity](intended-connectivity.md).

At every stage attach the requirements --stage STAGE traceability matrix and open
questions. Require current evidence of the specified kind and agreement of electrical,
firmware and mechanical endpoints. Reported consistency is not proof of physical
operation, actual CAD implementation or human authorization.

The coordinator assigns all four roles from docs/roles on a frozen candidate. Use the
task/finding/review/stage templates under templates/project/workflow. Role reports are
read-only recommendations; only an authorized human approves the stage. Keep finding
history, independent closure evidence and integration/invalidation decisions. See
[the complete workflow](agent-workflow.md).

| Stage | Minimum evidence | Exit criterion |
|---|---|---|
| Specification | Functions, domains/currents, faults, mechanics, environment, standards assessment, vendor/service/assembly, test plan | User-approved requirements and process; unknowns have owners and a blocked stage |
| Schematic/libraries | PDF, ERC, BOM/MPNs, dated datasheets, pin/pad map, power/startup/protection calculations, programming and test points | All pins represented, truthful ERC types, findings and exceptions resolved |
| Placement | Both sides/3D, heights, mechanics, decoupling/loops, thermal design, antennas/barriers, assembly/inspection | Feasible process and test access; human approval |
| Routing | Layers, return paths, zones, impedance/topology/lengths, thermal design, clearance/creepage, ERC/DRC/parity | Correct rule scopes; each exception has rationale and approval |
| Release | Inspected manufacturing package, BOM/DNP, rotations/sides, process/stencil/panel, reports/hashes, bring-up plan | Consistent revisions, current approvals, release check passes |

Do not automatically reuse a footprint or reference layout for another MPN or stackup.
Evaluate MOSFETs at actual Vgs/load, I2C against rise times, and relays against their
specific datasheets. Mounting holes, PE and via fences depend on enclosure and isolation.
EMC and safety tests have separate acceptance criteria.

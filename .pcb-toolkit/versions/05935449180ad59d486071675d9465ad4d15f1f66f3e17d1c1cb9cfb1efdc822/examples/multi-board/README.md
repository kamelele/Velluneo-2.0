# Original two-board contract example

POWER and LED are fictional boards; CASE is their enclosure. No customer source,
schematic or manufacturing data is included. Numeric values are local fictional
requirements, not approved organization or supplier limits.

requirements.json has four requirements and electrical, firmware and mechanical
contracts. design-review.md is explicitly synthetic review evidence. A valid result
only confirms consistency of this declaration; it is not an actual human approval,
functional circuit, simulation, measurement or manufacturing-ready product.

From the ruleset repository root run:

    python examples/multi-board/run_demo.py

The runner writes original/broken variants and detailed matrices under
.work/multi-board-demo/ and a summary to reports/product-contract-example.json.

| Case | Expected result |
|---|---|
| valid | Declared contracts pass the placement gate |
| missing-requirement | IF-POWER refers to absent REQ-POWER; document rejected |
| interface-conflict | A declared 12 V upper bound exceeds the sink's acceptance |
| stale-evidence | Changed requirement acceptance invalidates the previous review |
| unknown-before-placement | Missing tolerance has an owner and blocks placement onward |

Broken conflict cases use freshly bound synthetic review metadata to show that a
matching digest cannot suppress a contract inconsistency. The stale-evidence case
deliberately does not rebind. The runner never creates real approvals.

To use the standalone command, prepare hardware.json with
product.requirements_file="requirements.json" and run:

    python scripts/pcb_rules.py requirements PROJECT --stage placement

No CAD installation is needed for declared-contract checks. The independent #9/#11
checks will later verify actual connectivity and spatial implementation.

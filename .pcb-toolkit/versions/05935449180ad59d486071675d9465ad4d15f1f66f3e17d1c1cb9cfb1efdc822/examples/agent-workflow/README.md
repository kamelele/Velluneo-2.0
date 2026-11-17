# Synthetic coordinator/reviewer walkthrough

This is an original tabletop exercise, not an actual multi-agent CAD run, independent
agent review, physical test or human approval. Named role reports and decisions below
are fictional fixtures. Never copy them into real approval records.

## Scenario

The POWER/LED/CASE example starts with a declared 500 mA source and 300 mA LED load.
A task requests a fictional 650 mA startup load. The first candidate updates the sink
without changing the source or reviewing the evidence. The declared contract is now
incompatible, and its prior review is stale.

The coordinator freezes the candidate and assigns the four read-only reviews:

| Role | Recorded synthetic finding | Closure evidence required |
|---|---|---|
| Reality Checker | F-01 major: 650 mA exceeds the declared 500 mA source | Agreed source/load budget and current contract check; later physical validation remains separate |
| Overengineering | F-02 proposal: reuse an existing power block, possibly simplify protection | Show application limits and preserved fault response; no unverified component removal |
| Completeness | F-03 major: startup requirement is missing from the catalog | Add owned REQ-STARTUP with acceptance, implementation and review evidence |
| Change Reviewer | F-04 major: the current candidate no longer matches prior review evidence | New verification on the corrected intent revision and integrated inputs |

Overengineering's optional simplification conflicts with Reality Checker's demand
for preserved fault behavior. The coordinator does not vote or remove protection.
It records both positions, retains protection in the fixture and refers reuse to a
bounded follow-up with its own evidence. F-02 remains a proposal, not an automatic fix.

The synthetic correction explicitly allocates an 800 mA source for the fictional
650 mA load, adds REQ-STARTUP and updates the synthetic design review. These are local
example decisions, not real engineering approval or shared rules. The review evidence
is then rebound to the corrected intent. The declared-consistency check passes.

All four fixture reviews can now recommend human review. The final state is
**awaiting_human_review**: no real human approval exists, so the next stage and merge
are not authorized by the exercise. Manufacturing and physical behavior remain unverified.

## Reproduce the executed contract portion

From the repository root:

    python examples/agent-workflow/run_walkthrough.py

The runner calls the existing product-contract checker for the incompatible candidate,
corrected candidate with old evidence, and corrected candidate with fresh synthetic
evidence. It writes detailed reports in .work/agent-workflow-walkthrough/ and a summary
to reports/agent-workflow-walkthrough.json. It launches no agents, edits no CAD and
creates no human approvals. Process refusals in the decision table are tabletop
expectations, not claims of a runtime enforcing transitions.

## Tabletop acceptance and refusal decisions

| Case | Required coordinator action | Evidence inspected in the exercise |
|---|---|---|
| Scoped task with pinned inputs | Delegate after ownership/dependencies are recorded | Task contract and project-index templates |
| Two writers request the same board | Block the second write assignment; allow read-only analysis | One logical-file lease, regardless of branch |
| Four reports disagree on a major finding | Keep the finding open and resolve with evidence/human owner | F-01/F-02 positions and resolution above |
| Implementer claims its own correction verified | Request independent closure review | Finding/review templates separate author and verifier |
| Candidate input changes during review | Invalidate affected reports and refresh the frozen candidate | Old intent digest fails the executed checker |
| Integration differs from reviewed branch | Run whole-project checks and repeat affected reviews | Integration-record template and explicit source comparison |
| All agents recommend readiness but no human decision exists | Wait; no next-stage transition or merge | Final fixture state is awaiting_human_review |
| Authorized human reviews the exact unchanged packet in a real project | Record actual decision, perform authorized merge and compare hashes | Procedural positive case only; not exercised as real approval |
| Rework/firmware change after bring-up | Open linked defect/ECO and repeat affected verification | Bring-up template and workflow invalidation rules |

The separate second-person pilot (#20) must test actual delegation, review independence,
tool integration and usability. Intended-netlist comparison (#9) and spatial CAD
enforcement (#11) remain separate work. This walkthrough does not replace them.

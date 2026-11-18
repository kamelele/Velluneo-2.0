# Reality re-review — ASSEMBLY-FIT-01

**Current frozen body:** `2f4d3e2eb2e0c63df7cf94675e409501a94b1dd60f37863f157c41f89770e652`  
**Verified members:** 68  
**Recommendation:** **ready_for_human_review** for the conditional mechanical study. **Actual PCB entry and assembly qualification remain blocked.**

## Scope and actual checks

Targeted independent re-review of the RF-01 correction and associated geometry/rendering changes. Read `RF01-resolution.md`, revised construction contract, `check_assembly_path.py`, path results, rendering changes and current check records. Ran frozen-member verification and the read-only assembly-path screen. Verified actual ZIP/member hashes, inspected revised OBJ piece groups and visually inspected the current preview.

Earlier static-envelope/source observations remain applicable; this re-review does not claim fresh electrical, thermal, manufacturing or physical testing.

## RF-01 — Major, corrected within the declared envelope scope

**Original defect:** the former fixed Z34–40 lap obstructed straight insertion of the populated board. The historical finding remains valid against the original 62-member body.

**Correction inspected:** the upper cup now opens at **Z40**, with no fixed tongue below it. The separate joining sleeve, lower nose and removable lid/cradles are installed after PCB loading. This changes the obstructing geometry rather than waiving the finding.

Independent numerical reconstruction confirms:

- Upper-mouth minimum radius: **27.9 mm**.
- Sleeve maximum outer radius, including declared radial tolerance/eccentricity: **27.75 mm**, leaving **0.15 mm**.
- Sleeve minimum inner radius: **20.39 mm**; lower PCB obstacle radius **16.46824596 mm**, leaving **3.92175404 mm**.
- C1 lowest allocated position: **Z42.95**, above the sleeve’s **Z42.1** upper bound. T1’s lower bound is **Z52.4**.
- Nose/sleeve allocated radial clearance: **0.15 mm**.
- Upper-loading limiting PCB side clearance: `17 − 16.375 − 0.2 =` **0.425 mm**.

The path screen includes declared body, PCB and trimmed-tail envelopes, with SMT metal additionally checked against the removable cradles. Its monotone axial-path reasoning is consistent with the proposed cavity and assembly order. The fresh run reports zero modeled cradle obstacles.

**Owner:** mechanical design/root implementer.  
**Closure status:** RF-01 closed for the explicitly conditional rigid-envelope study. Full manufactured assembly remains unqualified.

## Regression and evidence limits

No new bounded major identified. Archived OBJ now distinguishes upper cup, joining sleeve, nose, lid and end cradles; it remains envelope geometry rather than manufacturing CAD.

Overall allocated metrics remain **118.5 mm nominal height**, **119.8 mm tolerance stack**, **59.7 mm maximum diameter**, **0.55 mm component/cavity clearance**, and **0.48057 mm additional C1 vent-reservation clearance**.

The extra sleeve and **2 mm upper/6 mm lower overlaps** do not establish electrical seam adequacy. Selected wires, bends, contacts, retention force, tooling, materials, dimensional capability and actual assembly require further evidence. Installed heights remain unqualified production bounds. Custom cooling has no demonstrated thermal performance.

Current records retain requirements exit **1** and work-check exit **2**. Prior electrical, fault, magnetic, thermal, insulation and process gates remain open. This recommendation grants no stage approval or manufacturing release.

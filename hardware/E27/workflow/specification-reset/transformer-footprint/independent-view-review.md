# T1-STEP-VIEW independent Reality diagnostic review

Reviewer /root/spec_reality; 2026-11-17. Read-only shared source; only this report written. Scope: native-source geometric inference for candidate coilformer pin view, not assignment/CAD, owner approval, a physical sample, manufacturer certification or a finished-transformer acceptance.

Recommendation: **ready_for_human_review for the corrected Proposal A source/view inference**. No blocking geometric/handedness error found in the corrected inference. A subsequent actual footprint/assignment still requires review against its own exact frozen packet. The earlier FOOTPRINT-02 report remains historical for its unassigned T1 packet.

## Independent checks

Independently imported the authentic hashed TDK STEP using the installed CadQuery/OCP geometry kernel, without executing implementer scripts or writing their outputs. Reproduced one solid and430 faces; ten square tip faces area0.36mm² at Y10.25, X−10/−5/0/5/10 and Z±11.25, normal+Y. Thus pins project toward+Y and a component-side view looks inward from−Y.

Reproduced external mark face335: centre approximately(−8,−5.15,−8.65), outward normal(−0.7071068,−0.7071068,0), area0.26627417mm². Its bounding Z extent−8.70..−8.60 places this small external chamfer at one flange/end. Four other45°XY planes are much larger symmetric inner-aperture surfaces (area21.9741), not four equivalent exterior pin1 marks. Do not describe face335 as the sole45°plane in the whole model.

Visually compared the native TDK PDFp3 Pin1-marking arrow/corner and front outline with the actual diagnostic front rendering. In the native-front orientation (pins downward), the external mark is upper-left, matching the model seen from−Z with screen-right+X and screen-up−Y. The corresponding outer pin is STEP(X−10,Z−11.25). The native2D numbering places1..5 along that flange, left to right; the opposite flange carries10..6 left to right. STEP has no textual numbered pin map; this numbering is inferred by correlating the source's unique exterior mark, front outline and pin plans with actual model geometry.

Independently checked handedness algebra: inward viewing vector(+Y) cross screen-up(+Z) yields screen-right(+X). Therefore front/component-side footprint coordinates are **x_fp=X_STEP, y_fp=−Z_STEP**, with the observer on−Y and pins extending away toward+Y. The corrected mapping is:

| Footprint row | x=−10 | x=−5 | x=0 | x=+5 | x=+10 |
|---|---|---|---|---|---|
| y=−11.25 (STEP Z+11.25) | 10 | 9 | 8 | 7 | 6 |
| y=+11.25 (STEP Z−11.25) | 1 | 2 | 3 | 4 | 5 |

This supports Proposal A, including pin1 at(−10,+11.25). The earlier Proposal B top-view claim used the wrong screen-down sign and is superseded for this diagnostic. Merely reproducing a raster rotation is not the basis: the camera cross-product and inspected solid coordinates establish the sign.

## Retained constraints

No shared footprint was assigned or accepted by this review. This source-correlated inference addresses the prior 2D-view ambiguity at the candidate level; it does not prove an actual supplied bobbin's geometry/marking, finished winding pinout, start/dot connections, solder holes/annuli, process, thermal fit or insulation construction. Complete native T1 footprint generation/assignment and fresh pin/graph checks remain a separate integration. SCH-LIB-001 and all electrical/startup/clamp/model/thermal/safety majors remain open. No manufacturer contact, physical inspection or measurement occurred.

## Exact inspected inputs

| Path | SHA256 |
|---|---|
| tmp/fp02-a/tdk-efd25.step | f6acdbbccb291fd39ac8028c163d7bdb47fa6849c8c7d94dce01076f05dfb2f0 |
| component-study/source/efd25.pdf | f4b6084fa9171a0157c3744663e146da6b3a738171dab4dfd3e137c125f6f06e |
| tmp/fp02-step-audit/findings.json | a169c159ee7c9185201e590d104430db13f1179642cad6bc5b203d2a2e176eb7 |
| tmp/fp02-step-audit/faces.json | fb4872226bbccab48e8622123bcab8856e4d342a4b3c8fec575714f74500fef4 |
| tmp/fp02-step-audit/explicit-views.py | 6308394d82ca226ffe6844fab53a248e935704eb7d8f6dabbda302dbeddc87b0 |
| tmp/fp02-step-audit/front-native-orientation.png | 79a039a98c0c69233ad2f2369f45e00da031b63e3db6495a418b7b83719eb347 |
| tmp/fp02-step-audit/component-top-Xright-minusZdown.png | c7da841734f5b3cd99aa59ca74d9841c5969065264ca79036c12e9e27ee97150 |
| tmp/fp02-step-audit/native-pin1-front-crop.png | b7b9f8596b75b810728bd36d7ab7985058f22cb6a3a818c63b4fece56d8be63a |

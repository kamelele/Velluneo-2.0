# Primary-buffer and optical-acceptance proposal review record

VEL-PRIMARY-BUFFER-01 / VEL-LIGHT-ACCEPT-01 r1, 2026-11-16. Preliminary screen and proposed acceptance content only. No formal specification approval, controller/capacitor release, human engineering sign-off or physical qualification.

## Frozen files

| File | SHA-256 |
|---|---|
| calculate.py | 432a8a480078e093359206ea02cce14c5861ab6c60d7f580ed7b8c6516fc25ea |
| results.json | a2273e730c841e7caa1df843e4799fac01c77b6352fff7f531e5a5745afacf2a |
| findings.md | 31de6d27403d8b64268ba47127f29d5da85f105f6a2c81427a6cca79436c3d80 |
| acceptance-proposal.md | 8c771e680c67a37092d76feb6170844bba2527f1dad938f932f7855c99b841c9 |
| sources.json | b5615626e7f976f836e3fd4d5ea13b87a7329c448645bcaa933878924d220586 |

All four independent read-only review contexts inspected the same frozen files. Source downloads remain reference-only outside repository deliverables; their sizes and hashes are in sources.json. No result file changed after review.

## Actual review scopes and findings

| Role / actual context | Evidence checked / recommendation | Open engineering work |
|---|---|---|
| Reality Checker /root/spec_reality | Full half-step reproduction across 216 cases exactly matched results.json; checked bridge/CPL energy equation, feed/loss accounting, Fourier PF/DF/THD normalization, partial thermal/inrush/discharge arithmetic. Native PDF sizes/hashes match; local source text supports the cited capacitor rows and EU benchmark values. Ready for preliminary human discussion. | RC-PBUF-001 actual controller regulation/startup/UVLO/fault/LED/light behavior. RC-PBUF-002 capacitor ESR/leakage/switching ripple/temperature/ageing/tolerance. RC-PBUF-003 actual harmonic limits/methods and genuine adoption of proposed optical criteria. |
| Overengineering Reviewer /root/spec_simplicity | Code/results/note/proposal/source-register inspection; no duplicate full solver run. No new unnecessary-complexity blocker. Recognizes that 10 uF is not an optimum or final choice merely because smaller values meet the provisional floor. | OE-LED-01 complete common-requirements implementation/process comparison stays open. No unnecessary PFC stage is added or excluded. |
| Completeness Reviewer /root/spec_completeness | Five hashes, native source integrity, stored-result tables/ranges/partial proxies and proposal scope reconciled. No duplicate full solver run or independent source-PDF content validation. | No completeness finding after the bounded milestone-input clarification below. Controller, optical test capability, thermal, faults, sourcing and manufacturing remain deferred. |
| Change Reviewer /root/spec_change | Five hashes and native reference integrity; packet r11 scope, proposals versus accepted values, authority, one-colour milestone, PF/DF/THD distinctions and absent qualification claims. No duplicate full solver run. | No new Change finding. No hardware, numeric optical criterion, service delay or stage approval inferred. |

Author and Reality reviewer separately ran `python calculate.py --verify-halved-step`. Numerical differences for 2 us versus 1 us were at most 0.754 mV minimum bus voltage, 1.204e-6 total PF and 0.208 uA capacitor RMS current. Energy identities and periodic balance were checked. These verify declared equations only, not real hardware or standards compliance.

Current legal applicability/classification, full licensed IEC methods, live component/process sourcing and physical behavior were not independently established. Catalogue scope summaries are not represented as a completed test procedure.

## Input-scope clarification

The Completeness Reviewer initially could not establish whether one colour suffices for the September deadline from earlier initial-sampling context alone. The authoritative local product packet r11 was supplied by path; the reviewer directly verified R-DEMO and section 17. They explicitly require one complete tested prototype with at least one colour by 30 September 2027; all three by then are a stretch goal while future three-colour compatibility remains required. The reviewer independently closed that input-scope issue. No new milestone or product-scope decision was made here.

The proposal's first-colour testing does not qualify unbuilt variants or replace later three-colour evidence. PstLM <=1.0 and SVM <=0.4 remain proposed content for genuine owner review, not accepted requirements. The earlier illustrative 5% electrical value remains illustrative.

## Separate index delta

The Change Reviewer separately inspected the updated driver-study/README.md content, SHA-256 `393dc25f415372343795faef863c44c7788bbb58917f52aec2b4f01242b444a5`. It adds the actual new evidence, updates task status to completed screening, keeps 10 uF/450 V provisional, and names controller/protection as the next bounded priority. Relative links and unchanged human authority were checked. Earlier technical reviews retain their unaffected scope; no additional full simulation was needed for this index.

## Outcome and limits

Proceed with the bounded buffered-controller/protection proposal, using 10 uF/450 V as a candidate and checking actual capacitor/ripple/thermal/harmonic feasibility. The 200 V comparison floor, 450 V rating reference, example discharge thresholds and proposed optical values do not certify safety, lifetime, flicker or manufacturability. Earlier applicable protection/interface findings remain open.

No CAD, SPICE, installed-toolkit environment pass, ERC/DRC, measurement, laboratory booking, supplier communication, order, reservation or BOM submission occurred. Agent recommendations are not human approval.

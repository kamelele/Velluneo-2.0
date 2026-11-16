# Proposed temporal-light acceptance and laboratory evidence

VEL-LIGHT-ACCEPT-01 r1, 2026-11-16. Proposal for the next complete specification review, not an owner decision or a compliance declaration. Product packet r11 remains authoritative. No requirements.json accepted value is changed by this document.

## Proposed measurable full-output goal

For the assembled lamp with its diffuser, propose:

| Metric | Proposed acceptance | What it addresses |
|---|---:|---|
| PstLM | <=1.0 | Objective light flicker metric |
| SVM | <=0.4 | Stroboscopic visibility metric |

These values are drawn from the EU 2019/2020 lighting benchmark as consolidated in the inspected source, including the SVM level effective from September 2024. This is a practical proposed baseline for the domestic lamp, not a claim that this prototype has passed or a complete determination of the replaceable panel/base product's legal classification. Recheck applicable law/standards and product classification before release; no special-use exemption is assumed.

Electrical current modulation, current ripple, total PF and visual inspection are not substitutes for those light measurements. The earlier 5% electrical-current example remains a development illustration, not a new acceptance limit. No stricter premium requirement is introduced here.

## Proposed evidence conditions and scope

The formal reference test proposal is full-output operation at nominal 230 V/50 Hz using a stable source, after thermal stabilization, with the intended panel, base, diffuser and open/ventilated fixture arrangement. Stabilization criterion, instrument method, optical geometry, ambient reference, measurement duration, sampling/filtering, uncertainty and pass margins must be taken from the actual adopted method and recorded before tests; no invented timings or acquisition settings are supplied here.

Risk-based development screens should cover the proposed 207/253 V ends, hot ambient/critical orientation and any variants that differ materially. These screens are proposed robustness work, not a claim that the reference legal test requires every combination. The already accepted 10–40 C/all-orientation product intent remains unchanged. Use a justified matrix rather than duplicating every electrical/thermal combination indiscriminately.

For the 30 September 2027 demonstration target, measure the actually built colour; one completed colour remains the minimum. Family claims for all three colours require representative evidence for all three, without making all three obligatory for the one-colour milestone. The ordinary milk-diffuser 800 lm reference remains useful for comparison; subjective similarity alone is not the metric acceptance test.

The user/university has stated access to flux, colour, safety and EMC measurement resources. Specific PstLM/SVM measurement capability, calibration, validated computation/instrument versions and method access have not been established. A generic photodiode/oscilloscope capture does not by itself prove a valid PstLM/SVM result. Coordinator prepares the test specification; the owner/laboratory establishes actual equipment, personnel, method and safe setup before physical work. No external reviewer is imposed before analytical design.

## Method references and actual access

The IEC public catalogue describes IEC TR 61547-1:2020 as an objective light flickermeter method, including intrinsic performance on stable mains and disturbance-immunity testing. IEC TR 63158:2018 describes an SVM meter; its July 2018 corrigendum is listed by IEC. Only public scope/catalogue information was inspected here, not complete licensed procedures. Do not claim implementation/measurement conformity from those summaries. Applicable current/harmonised editions and exact procedures remain to be established for the final test plan.

## Mains-current distinction that affects the buffer choice

The inspected EU source distinguishes fundamental displacement factor from total power factor. For LED/OLED mains light-source input power, its stated DF bands include 0.5 for >5 to 10 W and 0.7 for >10 to 25 W. Use actual measured whole-lamp input power, not a rounded internal power budget, when assessing applicability. The prototype model can exceed 10 W after feed/bridge/series losses; a high DF does not waive harmonic-current assessment or establish compliant total PF.

No standalone project PF/THD limit, regulatory exemption or complete mains-harmonic pass is adopted here. The applicable product/EMC/harmonics classification and exact limits remain open, and final performance must be measured.

## Review and decision status

Owner approval is to be sought with the complete specification proposal after the controller, interface and feasibility evidence is assembled. This note is concrete proposed content for that packet; an ordinary continue instruction is not recorded as approval of these new numeric criteria. No PstLM/SVM result, laboratory booking, order, supplier communication or physical test is claimed.

Sources inspected 2026-11-16:
- EUR-Lex: https://eur-lex.europa.eu/eli/reg/2019/2020/2021-09-01/eng — Annex II functional requirements and displacement-factor definition.
- IEC: https://webstore.iec.ch/en/publication/64795 — IEC TR 61547-1:2020 catalogue scope.
- IEC: https://webstore.iec.ch/en/publication/61455 — IEC TR 63158:2018 catalogue scope.
- IEC corrigendum listing: https://webstore.iec.ch/en/publication/63464

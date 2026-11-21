# Implementer handoff — LED and heat

Base:9f6f999aba18ca06b4bdc5ff4d0bf6148bb3fe94. Result:uncommitted exclusive `compact-60/led-heat/**` candidate for root integration. No shared graph/CAD/library/requirements edits. Toolkit86614c3b9b43713031e0ea481edbe26b71cd1b8f; manifest05935449180ad59d486071675d9465ad4d15f1f66f3e17d1c1cb9cfb1efdc822. Current owner direction60×120mm; no human stage approval fabricated.

Changed deliverables:calculate.py,native-spectra.json,results.json,sources.json,README.md,run.log,HANDOFF.md. SHA256 of script, source PDFs/CIE and previous optical input are recorded in results.json; actual final file manifest is written separately. Source snapshot is exact manufacturer Rev10B PDF, Rev36 lifetime summary and CIE DOI dataset; full input hashes are asserted by replay.

Requirement/object mapping:

- R-LIGHT/R-CCT/R-DIFFUSER:current actual8/7/7 Gfamily model, prior nominal optical acceptance and factory matching budgets retained; separate source-derived radiant calculation counts diffuser absorption as heat. Typical model is not production acceptance.
- R-THERMAL/R-ENV/R-SIZE/U07/U15:replace old8Wnormal/68C assumptions with source-conditioned electrical and optical estimates, no-credit rectangle, concrete48mm panel/75C internal rim and95C solder target; root integrates the actual60×120body, driver losses, orientations and external dissipation.
- R-PANEL-LIFE/U07:new exact Gorderfamily manufacturer applicability at105C359mA,10000h and reported L70>60000h;15khL70 design rationale constrained by actual source/current/temperature domain. Not measured life or warranty.
- R-COMPAT/R-REPLACE/R-BUILD/R-COST:common outside48mm panel size and annular thermal interface proposal, insulated LEDpads, bounded bin/current/FCT needs; no supplier assembly/stack/price confirmation, no approved contact CAD or new driver topology.
- R-FAULT/R-SUPPLY:retain no-optical-credit corner screen; forward-voltage cold/hot table is typical sensitivity, not guaranteedproductionlimits. Root power/fault analysis owns actual enforced current/voltage and faultclosure.

Executed:Python3.12 with PyMuPDF/numpy2.2.6, `python hardware/E27/workflow/specification-reset/compact-60/led-heat/calculate.py --sources ../compact-sources`, exit0.1nm/0.25nm native spectralintegration delta<0.00074%;positiveheat and48mm coarsefit checks pass. Actual LM80 p10 and spectral p41 were rendered from primary PDF and visually read. Source downloaded by coordinator; direct child DNS was unavailable, no fabricated download. No actual PCB, physical measurement, energized test or supplier quotation.

Open ownership:root combines electricalmodel with actual driverheat and compactbody, enforces thermal/faultlimits and exactmaterial/insulation construction. Prototype qualification later measures hottestLED/solder/rim, current/voltage/complete-lamp photometry and replacement-pressure repeatability over line/10–40C/orientations. Independent reviewers determine whether the stated prototype entry evidence is adequate; implementer does not declare own findings closed. Generic supplierAl data does not establish10K/W local thermal performance, reinforced insulation or actual sourcing.

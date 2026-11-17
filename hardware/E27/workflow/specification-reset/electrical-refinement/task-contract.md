# ELEC-REFINE-02 task contract

Parent/useroutcome: refine the current supply'sstartup,protection,capacitorloading andfluxbudget; actualinstruction “No to dopracuj to”. Basecommit36ad2f243d36d592228304b26c27188da0d46c4d, existingactualECO-01 decision remainsvalid. Stage: electrical/schematicpreparation, not manufacturing. Requirements R-SUPPLY,R-OFFLINE,R-FAULT,R-EMPTY,R-THERMAL,R-LIGHT,R-CCT,R-COMPAT; U05–U09 and existingmajors retained.

| Actualactor | Exclusivewrites | Deliverable |
|---|---|---|
| /root | electrical-refinement root, optics/,clamp/, lifecycle/workflowindex; coordinatorcompactpackaging of receivedcapdata | Scope/decisions,100budgetcases,clampconstraints,realchecks,finalreviewintegration |
| /root/support_design | electrical-refinement/capacitor/ duringimplementation,nowreleased |64switchedendpointcases,200ns/100nsconvergence,signKCLbounds,actualrerun/source/waveformrecords |
| /root/model_compatibility | electrical-refinement/startup-protection/ duringimplementation,nowreleased |48charge/pathscenarios,finitewindingauxiliarymodel,exactsourceconditions/OVP/samplecurrentlimits,actualrerun |
| /root/spec_reality | Readonlyfinalfrozeninputs,outputonlytmp/refine-review-reality.md | IndependentRealityreview |
| /root/spec_simplicity | Readonlyfinalfrozeninputs,outputonlytmp/refine-review-simplicity.md | IndependentOverengineeringreview |
| /root/spec_completeness | Readonlyfinalfrozeninputs,outputonlytmp/refine-review-completeness.md | IndependentCompletenessreview |
| /root/spec_change | Readonlyfinalfrozeninputs,outputonlytmp/refine-review-change.md | IndependentChangereview |

Root retains soleCAD/librarywritelease, inactive here. No nativeCAD/partvalue/interface/approvedrequirement/configuration/graphsource file maychange. No physicalmeasurement, newdevicearchitecture, purchase or energization is performed. Numerical source/results and explicitconditions are reviewable; no data from differentloads silentlypromoted to same-waveform proofs. CADanalysisevidence and actualsimulation/measurement levels remainseparate. Native originals remainexternal, exacthashes supplied.

Acceptanceofthis boundedanalysis: actualreproduciblecalculation/modelwithconvergence and equationchecks; knownconstraints/sourceconditions/no inventedminima; preservedrawgenerateddataidentity/reproduction; acknowledgedmissingactualcontroller/parasitic/fault/thermal evidence;100opticsbudgetswithmeasurementuncertainty included inbothfluxandmatchingchecks; unchangedCADbaseline verified; freshschematicrequirements result; four distinctreadonlyfinalreviews and appropriatecorrections. Completiondoesnotcloseparentmajor or schematichumangate byvote. Technicalfindings requiringactualvalues/sourcebound/physicalevidence remain assignedto/root and the futureuniversitylab owner asappropriate; no reviewerperson or actualinstrumentavailability invented.

Stopaffectedacceptance on mismatch, unsupportedsource/parameter, changedfrozeninput, sharedwrite, contradictoryreview or claimofmeasurementwithoutrecords. Neededspecificpart/topologycorrections wouldbecome a source-boundECO; no repeatapproval of unchangedECO-01 or productchoices requested. No manufacturedPCB or release is authorizedbythis task.

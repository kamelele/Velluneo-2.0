# LED19 bounded compatibility task

Owner requests checking selected LEDs against current C16 supply, specifically
voltage, light and thermal loading at319mA and whether seven series LEDs fit.
Root solewriter: led-compatibility-19/**, additiveproject-index entry and the owner-authorized revision13 append-only requirements addendum. BaseGit
7f4b7781f2178af5a57d42212a02ac1996ffcd2a. C16/C17/VIS18CAD, BOMs, rules,
manufacturing files and stage approvals are read-only. Owner explicitly relaxes only the850lm upper criterion; retain other requirements.
Check actual pinned/fresh makerPDF and exactordercode; reproduce existingtypical
curve and sourcecurrent, cover conditionalcurrent/temperature/count andthermal
derating; identify incompletebounds. Compare onecompatible4000Kcandidate if the
oldpartmissestarget; do not silentlychangeCAD orapproveparts. Fouractualindependent
reviewroles inspect samefrozenpacket. Publish checkedresults in VelluneoGitHub.
No stockreservation,suppliermessage,order,physicalmeasurement orstageadvance.

# LED19 verification plan - no measurements performed

First panel candidate: seven series JB2835BWT-G-H40GA0000-N0000001,4000K/80CRIclass.
Begin panel-only characterization with an isolated/current-limited laboratory DC
source and a controlled thermal fixture. This is not permission to energize the
unfinished mains driver. Use exact reel/bin identity, calibrated current/voltage,
photometry and a properly attached solder-point temperature sensor; do not infer
junction temperature directly from an uncorrected infrared surface reading.

Record DC voltage/current and LED solder-point temperature at303.624/319/336.057mA,
cold start and stabilized heating, with the actual selected substrate/TIM/heat path.
The currentpoints are C16 calculations at assumed transformer delivery0.90, not
complete guaranteed operating bounds. Characterize actual driver current separately.
Use95C solder-point and115C estimatedjunction as conservative engineering stop
targets from the preceding thermal study, not manufacturer life guarantees or
approved final product limits. The maker125C junction absolute limit remains binding.
Actual Rjs uncertainty, sensor error and spatial gradients must be accounted for.

For the complete lamp, retain the accepted230Vac/50Hz,25+/-1Cambient,base-up,complete
milky diffuser and stabilization protocol. Require at least750lm with the laboratory
uncertainty allowance; no850lm rejection ceiling after the owner's21Novembermessage.
Record actualflux rather than asserting959lm. Check4000+/-200K/Ra>=80 under the
actual drive and thermal conditions. Eventual three-colour matching remains due.

When the driver is qualified for controlled bring-up, capture actual LED ripple and
startup/transient current, VDD margin and switchingfrequency over line/load/temperature.
Check first/repeatedfaults, clamp, PstLM/SVM, transformer surroundingambient<=50C,
driver componenttemperatures and final housing/service conditions using the existing
C16bring-upplan. No finished safety, lifetime, EMC or manufacturing acceptance follows
from the present typical-curves calculation.

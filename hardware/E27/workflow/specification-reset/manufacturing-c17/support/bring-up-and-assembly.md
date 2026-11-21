# C16 prototype acceptance / assembly conditions

Qualified mains-power laboratory operator; isolated setup and properly rated
differential/current probes. An isolation transformer does not make the primary
touch-safe. Begin with unpowered continuity, polarity, actual part/lot identity,
hole insertion and full metal/shoulder spacing inspection. Reject mis-mapped T1.

T1 finishedhole1.40+/-0.05mm is a requested tight tolerance, not a standard JLC
capability confirmation. With landXmin1.925,holemax1.45,registration0.025mm,
annulus minimum0.2125mm. Standard+0.13mm hole tolerance does not establish0.20mm.
Q1 hole1.70,land2.35 gives0.2225mm annulus under declared1.83/2.325/0.025 corners.
Lowest wide Q1 shoulder>=3mm abovePCB; use a controlled assembly fixture/spacer
and trim straight tails after soldering. No forming. Mechanical support, material,
hot creepage and actual supplier insertion tolerances need confirmation.

Start with an isolated adjustable supply/current-limited power setup and electronic
load under a controlled test plan. At207/230/253Vac, cold/hot and repeated starts:
recordVDD,VS,CS,VGS,VDS,primary current and secondary voltage. Healthy VDD trough
>=9.45V. Check minimum on-time~>=300ns and demagnetization~>=1.1us perTI guidance,
especially no-load/CV/light-load. Tune R6 to measured delay, rerun current limits.

Open output, short output and restart tests: capture the FIRST and repeated fault
pulses; require primary current<=1.1Apk and total extra current-rise interval<=400ns.
Stop immediately on exceeding either, saturation knee, unsafe VDS/ringing or VDD
overrating; do not treat averaged current as a per-cycle peak. Record probe bandwidth,
calibration/loading, line phase, initial capacitor charge and transformer/IC/FET lots.
No arbitrary internal component-failure coverage is implied by the working-OCP test.

Measure primary inductance/leakage/DCR and hot behavior of actual74032; measure
TVS/clamp pulse energy/temperature and MOSFET VDS including ringing/line transients.
Establish a declared voltage margin below device ratings before acceptance. Confirm
fuse clearing/resistor pulse/sustained faults against actual prospective source.

Thermal soak in final orientation/enclosure: transformer surrounding ambient<=50C
perMYRRA; establish winding/core,IC,FET,caps,NTC and resistor temperatures against
each exact datasheet and life target. Verify NTC shutdown/restart, sensor location
and coupling. No forced airflow or housing radiator is assumed by this board update.

Finish product insulation review and dielectric/creepage/clearance tests with the
applicable full lighting standards and qualified lab; component4kV declaration is
not a product test. Owner lacks full standards; no invented normative table is used.
Complete60x120mm enclosure/750..850lm LED integration and harness cut lengths,
sleeving,strain relief and assembly provider capability before release.

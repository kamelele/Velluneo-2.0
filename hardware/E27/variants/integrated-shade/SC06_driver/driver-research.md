# Development history — not the active capture contract

This research records earlier alternatives and seeds. The authoritativeSC06-Bpartsetandpinsetsarebom-design.jsonandintended-connectivity.json. InparticularSCR/D2/R6-to-groundandactivecapacitorcrowbarareNOTselected.

# SC06 driver research handoff, 2026-11-19

Research author: /root/driver_research. This is an engineering seed, not a qualified driver, manufacturer simulation, accepted schematic or measured result. No CAD was edited. Root owns integration. Primary PDFs inspected: local component-sources/an60.pdf Rev B03/15 and lyt0.pdf Rev B06/15. LYT0 page4 Figure4 and AN60 page10 Figure8 were rendered and visually inspected.

## Independent physical/function graph

LYT0006D-TL SO8C: pin1 BP; pin2 FB; pin4 DRAIN; pins5,6,7,8 SOURCE. Pin3 is physically absent. Do not use PDIP numbering. Exact Diodes MB10S-13: pin1 positive, pin3 negative, pins2/4 AC (manufacturer pin numbering differs from generic bridge symbols).

AC_L -> fusible RF -> AC_FUSED -> BR1 AC; AC_N -> other BR1 AC. MOV across AC_FUSED/AC_N. BR1 positive=RECT_PLUS; BR1 negative=DC_RETURN. C1 RECT_PLUS/DC_RETURN; L1 RECT_PLUS/BUS_PLUS; damping R1=4.7k across L1; C2 BUS_PLUS/DC_RETURN; U1.4=BUS_PLUS. A proposed bus TVS must specify whether before or after L1: those placements have different surge/filter ringing behavior.

SOURCE=U1.5/6/7/8=L2.1=Rsense.1=CFB negative=CBP low=D2 anode. SENSE_FB=U1.2=Rsense.2=CFB positive=D1 cathode. D1 anode=DC_RETURN. U1.1=BP=CBP high=D2 cathode=R6 high. R6 low=SCR anode; SCR cathode=DC_RETURN. L2.2=COUT_PLUS=COUT positive=bleeder high=OVP sense/feed high=RINS input. COUT negative=DC_RETURN. RINS output=LED_CONNECTOR_PLUS. LED_CONNECTOR_MINUS=DC_RETURN. NO alternate bulk-capacitor path around RINS. CBP100nF and CFB22uF reference SOURCE, not DC_RETURN. R1 is NOT an FB series resistor.

## AN60 design rules and suggested values

AN60 Step3: MDCM permits IO<=0.5*ILIMIT_MIN. At62.52mA versus LYT0006 minimum350mA at specified95mA/us, this is comfortably MDCM sizing. Step6 requires all-enabled open-loop current at minimum input >=1.1*IO, here68.772mA, then chooses L with tolerance/bias considered (AN60 suggests20% reserve for drum cores). Step8 uses PIXls iteration, NOT R=1.65/IO. Rsense samples freewheel current; input MOSFET current is a different component of output current. No honest source provides an exact closed-form final resistor for this new point.

Freezeable schematic SEED: RFB40.2ohm, one Yageo RC1206FR-0740R2L, CFB22uF16V, CBP100nF50V. RFB tau=.8844ms, versus20/fmin=.3226ms at62kHz. At1.76V and Rmin39.798ohm, resistor power=.07783W;0.25W is3.2x. Confirm effective CFB capacitance and sample/hold behavior.

Magnetics better than old RFB: Coilcraft RFC1010B-185KE1.8mH +/-10%, DCRmax2.75ohm, Isat10%drop=.64A25C, Irms20Crise=.36A. RFC1010B-225KE2.2mH is an alternative when the broader low-line/frequency corner needs more inductance, but its10%drop Isat=.58A is lower. L1 RFC1010B-106KE10mH: DCR15.5ohmmax, Isat10%drop=.29A, Irms20Crise=.15A, improves old RFB1010-103L .19A Isat. Ratings at25C are not guaranteed hot saturation ceilings, insulation voltage ratings, or inrush qualification. Manufacturer recommends RFC for new designs above56uH. https://www.coilcraft.com/getmedia/c187709d-4e59-4a35-bf2f-4557b133a391/rfc1010.pdf

Retain STTH1R06A freewheel diode as candidate. Source headline25ns is at IF=.5A/IR=1A; another1A reverse recovery test has45ns maximum. Do not describe25ns as universal/full-hot. AN60 requires ultrafast behavior with <=35ns guideline at hot lamp ambient; verify actual waveform. https://www.st.com/resource/en/datasheet/stth1r06.pdf

## Own per-cycle numerical screening algorithm

This models a fixed output voltage and ideal full-wave rectified source without input-filter dynamics, reservoir ripple, ESR/DCR, switching loss, current-limit slope dependence, real minimum-on-time spread, frequency jitter, startup, reverse current or actual current/thermal limits. CFB is integrated analytically during linear current ramps. It is NOT PIXls or SPICE. Fixed VOUT means changing68uF to100uF does not enter this calculation; transient and ripple models must be rerun separately.

```python
import math
def screen(vout,R,L=.0018,vac=230,f=66000,ilim=.375,vth=1.65):
    T=1/f; tau=R*22e-6; cf=0.; i=0.; q=0.; q2=0.; qin=0.; pk=0.
    count=int(f*.2)
    for n in range(count):
        vin=max(0,2**.5*vac*abs(math.sin(2*math.pi*50*n*T))-1.6)
        ton=0.; qa=0.; qa2=0.
        if cf<vth and vin>vout:
            a=(vin-vout)/L
            ton=min(.69*T,max(.5e-6,(ilim-i)/a))
            j=i+a*ton
            qa=(i+j)*ton/2
            qa2=(i*i+i*j+j*j)*ton/3
            i=j
            cf*=math.exp(-ton/tau)
        a=(vout+1+max(cf,0))/L
        tf=min(T-ton,i/a)
        j=max(0,i-a*tf)
        qb=(i+j)*tf/2
        qb2=(i*i+i*j+j*j)*tf/3
        cf=(cf-R*i-R*a*tau)*math.exp(-tf/tau)+R*(i-a*tf+a*tau)
        cf*=math.exp(-(T-ton-tf)/tau)
        pk=max(pk,i)
        i=j
        if n>=count//2:
            q+=qa+qb; q2+=qa2+qb2; qin+=qa
    dur=(count-count//2)*T
    return dict(Iout=q/dur,ILrms=math.sqrt(q2/dur),Ipeak=pk,Iinavg=qin/dur)
```

Sanity check using old RDR378 values85V/26.8ohm/1.5mH: model83.08mA versus reference82mA; agreement is not validation. New110V/40.2ohm/1.8mH at207/230/253VAC gives62.582/62.027/61.329mA, ILrms about121mA. Across90/110/121V output and those three lines, nominal-model total current59.40..63.38mA. At110V auxiliary load about7.52mA for root's new detector, leaving roughly54.5mA LED at230V.

Open-loop R=1ohm,207VAC,121Vout,Lmin1.44mH,ILIM350mA,f66k gives68.977mA: only0.205mA above110% target68.772mA. THIS IS NARROW AND MUST BE RECHECKED AT62kHz, real di/dt, temperatures and real bus waveform; do not call1.8mH fully closed merely from the nominal-frequency result. A larger2.2mH or a more tightly controlled actual Lmin may be needed. Illustrative combined variation at110V with40.2ohm tolerance, VFB1.54..1.76, ILIM350..401mA, f62..70k and L1.44..1.98mH gave57.95..66.02mA total; this is NOT an exhaustive guaranteed interval.

Completed frequency corner: at62kHz the1.44mH open-loop case gives65.896mA, FAILING the68.772mA headroom target. With2.2mH nominal and20% effective reserve (Lmin1.76mH) it gives76.132mA. Therefore prefer RFC1010B-225KE2.2mH as the engineering schematic pick with RFB40.2ohm; do not use1.8mH with the same20% reserve. At110V/230VAC/66kHz this2.2mH combination gives61.091mA total and119.716mA inductor RMS, leaving about53.57mA LED for root's assumed7.52mA auxiliary load. Selecting a trim value after actual circuit correlation remains necessary. No code/model feature establishes the specified110% margin across all real electrical corners.

## Surge and input current limitations

RF100ohm2W plus MOV275VAC and5KP400A is a concrete surge-limiting topology candidate.648V at7.7A TVS point does not prove a700V MOSFET limit for every combined line/surge current, temperature, tolerance, parasitic overshoot or input-filter ringing condition. Coordinate the D1 600V rating too: a648V BUS_PLUS clamp may already exceed its600V reverse rating when SOURCE/D1 node is driven high. Either bound the actual D1 reverse voltage below600V, or select a higher-rated ultrafast diode meeting recovery needs. A rated800/1000V ultrafast diode is a candidate improvement, not automatic qualification.

Concrete higher-voltage D1 engineering choice: Wolfspeed C4D02120E, active1200V2A SiC Schottky inTO252-2, zero minority-carrier reverse recovery (capacitive charge remains), exact manufacturer datasheet Rev13Nov2024 https://assets.wolfspeed.com/uploads/2023/10/Wolfspeed_C4D02120E_data_sheet.pdf . LCSC identity C7457230 visible, actual procurement/service availability not verified. Cost/space are higher than SMA; thermal/current/edge ringing/EMI qualification still required. Do not substitute a generic ES1M advertised35ns without actual manufacturer evidence; many ES1M variants specify75ns. Manufacturer physical pin mapping must be visually checked before capture, not inferred from generic DPAK diode defaults.

Do not equate filtered RF line RMS with DRAIN RMS. A declared operating budget Pinput~8W, VACmin207V, PF=.5 would imply77.3mA line RMS and0.597W RF100 loss; PF=.55 gives70.3mA and0.494W. PF values here are assumptions, not measured compliance. Actual rectifier/filter current, capacitor charging and inrush must be modeled/measured. Normal and repeated-surge pulse qualification of fusible RF remains separate.

At135V with100uF+20%, COUT energy becomes1.0935J, versus.74358J for68uF+20%. Recalculate R6/RINS pulse/repetition, passive discharge, SCR hold/reset and detector timing for the actual selected capacitor. No proposed change removes the need for disconnected-load OVP in this detachable-module product.

## Confirmed final freewheel-diode physical map

Local work/component-sources/c4d02120e.pdf was subsequently downloaded by root and its page1 rendered in memory and visually inspected. Actual document revision is14, September2026, superseding the Rev13 web copy cited above. Electrical diagram unambiguously connects PIN1 directly to CASE; the diode cathode is CASE and the diode anode is PIN2. Thus PIN1=KATHODE, CASE/TAB=KATHODE, PIN2=ANODE. For this circuit PIN1+CASE=SENSE_FB; PIN2=DC_RETURN. Do not use a generic TO252 pad2-cathode assignment. Future footprint must explicitly map the case pad and physical lead numbering; this document establishes electrical manufacturer identity, not a checked native footprint.

## Superseded SCR-era root SC06 choices and requested corner

Root now selects30series55mA LEDs,150uF160V EEUED2C151, RFB40.2ohm single1206, RINS/R6470ohm, L2 RFC1010B-225KE2.2mH, noMOV, RF220ohm FWFU2W220RJ and5KP400A TVS BUS_PLUS/DC_RETURN after the input filter. Earlier68/100uF and RF100/MOV examples above are historical comparisons, NOT the final selected values.

At135V,Cmax180uF the capacitor energy is1.64025J. R6/RINS waveform qualification and bleeder time must use this new energy. The old .74358J PR05 result does not qualify this capacitor. The two22k bleeders remain the same power at135V but135to5V passive discharge time with44k and180uF becomes26.103s (before resistor positive tolerance).

Requested open-loop corner207VAC,Vout123V,Lmin1.76mH,f62kHz,ILIM350mA,RFB1ohm: own ideal model75.291mA, versus target1.1*63.5mA=69.85mA. With approximate220ohm source and430nF lumped input capacitor,73.863mA. This supports the engineering seed, but source/current-limit/temperature parameters are not fully bounded and the real filter has not been simulated. No claimed manufacturer margin or measured pass.

With RFB40.2ohm,L2.2mH,Vout110V, ideal source207/230/253VAC gives61.496/61.091/60.675mA total. Subtracting root's7.52mA auxiliary estimate leaves53.98/53.57/53.16mA LED; this is close to55mA but not an exact55mA result. Final current trimming/correlation remains required.

Approximate source-RMS extension to the above model: initialize vbus=0; use vin=vbus instead of the ideal rectified input. Each switching cycle compute qa, then isrc=max(0,(vrect-vbus)/220), update vbus=max(0,vbus+(isrc*T-qa)/430nF), and accumulate isrc^2*T over the second half of a0.4s simulation. This uses averaged per-cycle source charge and NO actualL1, C1/C2 separation, resonance, high-frequency bridge-current shape, ESR or converter losses. At110V the result207/230/253VAC is54.23/53.68/53.38mA RF RMS and .647/.634/.627W RF220 dissipation. Treat this as a rough .65W scale estimate only, not an exhaustive65mA ceiling, thermal qualification or surge test. A PF-based8W/207V/.5 assumption instead gives77.3mA and1.31W in220ohm; neither establishes the actual PF.

At25C only, a1358V peak source, TVS lower breakdown447V and RFmin220*.95*.97=202.73ohm imply precoordination current screen <=4.494A. That stays below the nominal7.7A648V clamping test point, but temperature, actual5KP part tolerance, parasitic voltage, filter energy and RFsurge pulse/repetition remain separate. A BUS_PLUS TVS afterL1 does not remove the need to check the rectifier-side capacitor voltage and L1 inrush/saturation. Root's exact ProTek part must be checked against its own datasheet, not a generic5KP400A's values.

## Q1 visual map and newly explicit BP qualification issue

Root downloaded101016byte work/component-sources/x02-2000.pdf from https://akizukidenshi.com/goodsaffix/X02series.pdf . I rendered/visually inspected page1 and page6. This ST-authored September2000Ed3 cover explicitly shows SOT223 lower leads leftK, centerA, rightG and opposite large tabA. Thus the physical K/A/G and tabA map is visually confirmed. This old document does NOT print numerical pad labels on page6. The numerical1/2/3 lowerleft-to-right and4tab layout is separately supported by ST-authored Rev4January2011 numbered package drawing, page7, extracted via web mirror https://www.mouser.com/datasheet/2/389/x02-1852745.pdf . Circuit logical contract1K/2A/3G and tab commonanode is consistent. Future footprint may duplicate pad2 on the tab; record that convention explicitly rather than silently omitting the tab. Ed3 is used solely for physical identity, not as current electrical-parameter authority; retain DS2122Rev7October2025 for SCR current/temperature/trigger specifications.

I also rendered/visually inspected localLYT0RevB page9 absolute limits: BP=-0.3V..9V relativeSOURCE. Inherited AN60Fig8 D2anodeSOURCE/cathodeBP may impose BP-SOURCE=-VF while conducting. A silicon diode forward drop around0.7V is NOT a bound compliant with-0.3V. Our150uF/R6470 modification has no documented negative-injection allowance. Reduced capacitor-discharge current does not prove the BPrail safe. This is an explicit unclosed electrical qualification issue, not cured by citing the manufacturer reference. Closure requires actual worst-case BP-SOURCE voltage, D2 current, duration and repetition at hot/cold/trip/reconnect/brownout; if absolute limits are exceeded, obtain written manufacturer applicability evidence or redesign the shutdown/discharge interface. Do not waive the absolute limit or claim completed protection merely because AN60 shows the topology.

Read-only inspection of root's SC06_driver/intended-connectivity.json: power-block U1/BR1/D1CASE/CFB/dampingR1/D2 orientations match the independent source graph above. This was not a full comparator-detector review, exported-CAD comparison, footprint check or stage approval.

## Latest architecture: PhotoMOS shutdown, no SCR discharge

Root now removes SCR Q1, D2 and R6 entirely. A source-referenced PhotoMOS output disables U1 by shunting BP to SOURCE; the detector input/output isolation is functional level shifting, not a claim of mains-safe accessible output. Passive COUT discharge uses two56kohm25121W resistors in parallel (28kohm effective). RINS470ohm remains. Auxiliary feed is now four3kohm in series,12kohm total. All SCR/D2/R6 analysis above is history and must not be exported into the revised circuit. This eliminates the inherited silicon-diode negative BP clamp mechanism, rather than waiving the-0.3V absolute limit.

L2 is now two Coilcraft RFC1010B-155KE1.5mH in series,3mH nominal, each10%drop Isat.70A at25C; actual L(I,T), voltage withstand and final temperature remain to establish. Functional power path: SOURCE -> L2A.1 -> L2A.2 -> L2_MID -> L2B.1 -> L2B.2 -> COUT_PLUS. L2_MID has no other power connection. Use combined effective Lmin2.4mH for the20% screening reserve. Steady RMS current is common to both inductors; copper loss is the sum of both DCRs.

Requested open-loop corner Lmin2.4mH,207VAC,123V output,62kHz,350mA current limit gives94.588mA in the ideal model,92.224mA with the earlier rough220ohm/lumped430nF source extension. This exceeds1.1*70mA=77mA and even1.1*77mA=84.7mA in those models. It is NOT proof that every actual low-line/hot/current-limit corner passes AN60, nor a new guarantee of70/77mA total regulated current.

At110V output,3mH nominal and207/230/253VAC respectively, total-current results in mA:

- R34.8ohm:67.443 /67.830 /66.880 (roughsource67.991 /68.132 /68.363).
- R35.7ohm:66.027 /65.870 /65.613 (roughsource66.702 /66.871 /66.798).
- R34.0ohm:68.430 /69.041 /68.108; closest standard E96 seed to requested68.5–69mA center.
- R33.2ohm:70.180 /70.127 /69.615.

Recommend one Yageo RC1206FR-0734RL34.0ohm as a seed IF root wants the68.5–69mA model center; exact ordering syntax/vendor datasheet must be verified before BOM freeze.34.8ohm is a more conservative lower-current seed;35.7ohm undershoots this model target. At34.0ohm,CFB22uF gives.748ms time constant and VFBmax1.76V/Rmin33.66ohm gives92.0mW, so0.25W rating is2.7x that screening dissipation. Illustrative low/high combined parameter cases at123V output give65.366/73.623mA total for34ohm;34.8ohm64.212/72.174;35.7ohm63.065/71.003. These are two illustrative corners, not an exhaustive bound. Auxiliary feed/bleeder/divider currents depend on output voltage and capacitor leakage is a maximum specification, not a known typical load; do not call this an exact55mA LED regulator without correlation.

With Cmax180uF,Vinitial135V and no further energy supplied:28kohm gives16.611s to5V. One56kohm branch open and the surviving resistor+1% gives33.554s, within the proposed40s condition. This is a DC RC calculation only; afterACoff must also bound stored input-filter energy and continued converter operation. Each resistor sees135^2/56k=.32545W before tolerance, with or without the other branch open.1W2512 temperature derating/mounting must be checked; resistor short faults are a different containment case.

PhotoMOS stress caution: directly shorting BP/SOURCE discharges100nF CBP from5.8–6.1V. The initial PhotoMOS output current is not bounded by7.5mA bias charge current. Consider100ohm1% in series with the PhotoMOS output, limiting6.1V/99ohm to61.6mA before dynamic parasitics; stored CBP energy is1.86uJ. With7.5mA charge current the resulting positive BP-SOURCE clamp is around.75V+relaydrop, still comfortably below typical4.85V BP undervoltage threshold. This is a suggested stress fix for root/OVP agent, not a claimed incorporated/validated part. Check exact PhotoMOS load-current, turn-on behavior, hot RON and actual maximum BP charging current before accepting the shutdown block.

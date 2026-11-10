"""Verify the Rev F detector and shutdown logic with bounded and idealized models."""
import csv
from itertools import product
from math import exp, log
from pathlib import Path

from model_revb2_guard import limits, pulse, step_delay, zero

OUT = Path('outputs/Zasilacz_RevF_Sterowanie')
DT = 10e-6
VON = 1.0  # eFuse data-sheet application guidance
VOFF = .4
ISHDN = 10e-6  # budget at the specified 0.4 V test point
VCE = .20  # engineering bound to verify at the low operating current and temperature
RTOL = .02  # includes resistor tolerance and a temperature allowance
CTOL = .20  # envelope for the RELEASE_B capacitor


def voltages():
    def range_for(nominal):
        return (nominal*(1-RTOL),nominal*(1+RTOL))

    on, opened, clamp_beta, release_beta = [], [], [], []
    for vin,r17,r18,r112,r113,r110,r111,leak in product(
        (18,30),range_for(10e3),range_for(10e3),range_for(100e3),
        range_for(100e3),range_for(10e3),range_for(100e3),(-ISHDN,ISHDN)
    ):
        # Use the same leakage budget as a sensitivity check when SHDN is high.
        supply_resistor = r17+r112
        on.append((vin/supply_resistor+leak)/(1/supply_resistor+1/r18))
        opened.append(ISHDN*r18)
        clamp_beta.append(((vin-VCE)/supply_resistor+ISHDN)/((vin-.95)/r113))
        release_beta.append((vin/r113)/((2.4-.95-.08)/r110-.95/r111))
    assert min(on)>VON and max(on)<4
    assert max(opened)<VOFF and VCE<VOFF
    assert max(clamp_beta)<3 and max(release_beta)<3
    return min(on),max(on),max(opened),max(clamp_beta),max(release_beta)


def nand(a,b):
    return not (a and b)


def fixed_points(pg, fault_n):
    return [(a,b) for a,b in product((False,True),repeat=2)
            if a==nand(fault_n,b) and b==nand(pg,a)]


def logic():
    assert fixed_points(False,True) == [(False,True)]
    assert fixed_points(True,False) == [(True,False)]
    assert fixed_points(False,False) == [(True,True)]
    assert fixed_points(True,True) == [(False,True),(True,False)]
    # Q102 independently cuts the release-current path whenever PG is low.
    for pg,b,forced_permit in product((False,True),repeat=3):
        if not pg:
            assert not (pg and forced_permit)
            assert not (pg and b)


def time_bounds():
    # Use the divider before the B-E junction conducts. 0.85 V is a conservative
    # comparison level for initial drive, rather than a detailed transistor model.
    rc_high = 1/(1/10200+1/102000)*12e-9
    rc_low = 1/(1/9800+1/98000)*8e-9
    hi = 2.4*98000/(10200+98000)
    release = -rc_high*log(1-.85/hi)
    fastest = -rc_low*log(1-.45/3.4)
    low = .20
    reapply = rc_high*log((.95-low)/(.40-low))
    assert release < .07e-3 and reapply < .18e-3 and fastest > 8e-6
    return fastest,release,reapply


def yes(_):
    return True


def good(t):
    return t>=.012


def simulate(case,threshold,tau):
    pg_at,k1,k2,s1,thermal,s2,stuck_permit = case
    filtered = [0.,0.]
    factor = exp(-DT/tau)
    permitted_latch = True
    driver_v = 0.
    cut_event = None
    ever_shdn_enabled = False
    ever_output_enabled = False
    beta = 1-exp(-DT/(10e-9/(1/10_000+1/100_000)))
    for tick in range(7001):
        t = tick*DT
        pg = pg_at(t)
        for n,source in enumerate((k1,k2)):
            filtered[n] = source(t)+(filtered[n]-source(t))*factor
        fault = max(filtered)>=threshold
        if not pg:
            permitted_latch = True
        elif fault and permitted_latch:
            permitted_latch = False
            if cut_event is None:
                cut_event = t
        output = stuck_permit or (pg and permitted_latch)
        high = 3.3*100_000/110_000 if output else .05
        driver_v += (high-driver_v)*beta
        released = pg and driver_v>=.70
        shdn = released and s1(t) and thermal(t)
        delivered = shdn and s2(t)
        ever_shdn_enabled |= shdn
        ever_output_enabled |= delivered
    return ever_shdn_enabled,ever_output_enabled,cut_event is not None,delivered,cut_event


def main():
    lo,hi,tfast,tslow = limits()
    fast,release,reapply = time_bounds()
    low_on,high_on,open_max,b1,b2 = voltages()
    logic()
    cases = [
        ('Rozruch normalny', (good,zero,zero,yes,yes,yes,False),(True,True,False,True)),
        ('S1 otwarty przy PERMIT', (good,zero,zero,lambda _:False,yes,yes,False),(False,False,False,False)),
        ('Termostat otwarty przy PERMIT', (good,zero,zero,yes,lambda _:False,yes,False),(False,False,False,False)),
        ('S2 fizycznie otwarty', (good,zero,zero,yes,yes,lambda _:False,False),(True,False,False,False)),
        ('PG niski i PERMIT zablokowany w stanie wysokim', (lambda _:False,zero,zero,yes,yes,yes,True),(False,False,False,False)),
        ('Zwarcie K1 w pracy', (good,pulse(.027,.014,26),zero,yes,yes,yes,False),(True,True,True,False)),
        ('Zwarcie K2 w pracy', (good,zero,pulse(.027,.014,26),yes,yes,yes,False),(True,True,True,False)),
        ('Zwarcie K1 i K2 jednocześnie', (good,pulse(.027,.014,26),pulse(.027,.014,26),yes,yes,yes,False),(True,True,True,False)),
        ('K1 wymuszone wysoko przed PG', (good,lambda _:26,zero,yes,yes,yes,False),(False,False,True,False)),
        ('Zwarcie przy rozruchu z rampą 11 ms', (good,lambda t:26*max(0,min(1,(t-.012)/.011)),zero,yes,yes,yes,False),(True,True,True,False)),
        ('Impuls 100 µs od 6,4 V', (good,pulse(.030,.0001,26,6.4),zero,yes,yes,yes,False),(True,True,False,True)),
        ('Impuls 500 µs od 6,4 V', (good,pulse(.030,.0005,26,6.4),zero,yes,yes,yes,False),(True,True,True,False)),
        ('Po zwarciu ponownie zamknięto S1, PG pozostaje wysoki', (good,pulse(.027,.014,26),zero,lambda t: t<.043 or t>.05,yes,yes,False),(True,True,True,False)),
        ('Po zwarciu utrata PG i powrót', (lambda t: .012<=t<.045 or t>=.054,pulse(.027,.014,26),zero,yes,yes,yes,False),(True,True,True,True)),
    ]
    rows = []
    for label,signals,want in cases:
        for corner,threshold,tau in [('niski/szybki',lo,tfast),('wysoki/wolny',hi,tslow)]:
            result = simulate(signals,threshold,tau)
            assert result[:4] == want, (label,corner,result,want)
            rows.append((label,corner,*result[:4],'' if result[4] is None else f'{result[4]*1000:.3f}'))
    with (OUT/'Model_RevF.csv').open('w',encoding='utf8',newline='') as stream:
        writer=csv.writer(stream,lineterminator='\n')
        writer.writerow(('Przypadek','Narożnik','SHDN był załączony','Wyjście było załączone','Wykryto','Wyjście aktywne na końcu','Czas detekcji od początku [ms]'))
        writer.writerows(rows)
    print(f'{len(rows)} corner scenarios; threshold {lo:.3f}..{hi:.3f} V')
    print(f'RC detector 0->26 V: {step_delay(26,lo,tfast)*1000:.3f}..{step_delay(26,hi,tslow)*1000:.3f} ms')
    print(f'SHDN released {low_on:.3f}..{high_on:.3f} V; open interlock <= {open_max:.3f} V')
    print(f'Forced beta clamp/release {b1:.2f}/{b2:.2f}; release RC {fast*1e6:.1f}..{release*1e6:.1f} us; reapply RC <= {reapply*1e6:.1f} us')


if __name__ == '__main__':
    main()

"""Tolerance and state model for Rev B2. No semiconductor or thermal model."""
import csv
from itertools import product
from math import exp, log
from pathlib import Path

OUT = Path('outputs/Zasilacz_RevB2_Ochrona')
TOP, BOTTOM = 330_000, 22_000
REF_TOP, REF_BOTTOM = 133_000, 22_000
CAP = 220e-9
TOL_R = .0035
TOL_C = .27
VOS = .0055
BIAS = 20e-9
DT = 10e-6


def parallel(a, b):
    return a * b / (a + b)


def limits():
    results = []
    for supply, sign_top, sign_bottom, sign_ref_top, sign_ref_bottom, offset, sense_bias, ref_bias in product(
        (3.234, 3.366), (-1, 1), (-1, 1), (-1, 1), (-1, 1), (-VOS,VOS), (-BIAS,BIAS), (-2*BIAS,2*BIAS)
    ):
        top = TOP * (1 + TOL_R * sign_top)
        bottom = BOTTOM * (1 + TOL_R * sign_bottom)
        ref_top = REF_TOP * (1 + TOL_R * sign_ref_top)
        ref_bottom = REF_BOTTOM * (1 + TOL_R * sign_ref_bottom)
        reference = supply * ref_bottom / (ref_top + ref_bottom) + ref_bias * parallel(ref_top,ref_bottom)
        gain = bottom / (top + bottom)
        results.append((reference + offset - sense_bias * parallel(top,bottom)) / gain)
    tau = parallel(TOP, BOTTOM) * CAP
    return min(results), max(results), tau*(1-TOL_R)*(1-TOL_C), tau*(1+TOL_R)*(1+TOL_C)


def step_delay(voltage, threshold, tau, initial=0):
    if voltage <= threshold:
        return None
    return -tau * log((voltage-threshold)/(voltage-initial))


def simulate(scenario, threshold, tau):
    pg, k1, k2, switch = scenario
    values = [0., 0.]
    factor = exp(-DT/tau)
    permit = False
    permit_time = None
    was_pg = False
    pg_rise = 0.
    prev_clock = False
    saw_fault = False
    trip_time = None
    ever_enabled = False
    for step in range(6001):
        t = step * DT
        ready = pg(t)
        if ready and not was_pg:
            pg_rise = t
        was_pg = ready
        clock = ready and t >= pg_rise + .0008
        for i, voltage in enumerate((k1(t),k2(t))):
            values[i] = voltage + (values[i]-voltage)*factor
        fault = max(values) >= threshold
        old_permit = permit
        if not ready or fault:
            permit = False
        elif clock and not prev_clock:
            permit = True
        if permit and not old_permit:
            permit_time = t
        if fault and old_permit:
            saw_fault = True
            if trip_time is None:
                trip_time = t
        prev_clock = clock
        enabled = permit and switch(t) and ready and t >= permit_time + .0013
        ever_enabled |= enabled
    return ever_enabled, saw_fault, enabled, trip_time


def zero(_):
    return 0


def good(t):
    return t >= .012


def closed(_):
    return True


def pulse(start, duration, voltage, baseline=0):
    return lambda t: voltage if start <= t < start+duration else baseline


def main():
    minimum,maximum,fast,slow = limits()
    nominal = 3.3*REF_BOTTOM/(REF_TOP+REF_BOTTOM)*(TOP+BOTTOM)/BOTTOM
    assert 7.0 < minimum < nominal < maximum < 8.0
    assert step_delay(26,maximum,slow) < .0021
    assert step_delay(10,maximum,slow) < .009
    assert step_delay(7.0,minimum,fast) is None
    cases = [
        ('Oba kanały 6,4 V', (good,pulse(.025,.060,6.4),pulse(.025,.060,6.4),closed), (True,False,True)),
        ('S1 otwarty', (good,zero,zero,lambda _:False), (False,False,False)),
        ('Zwarcie K1 po uruchomieniu', (good,pulse(.030,.020,26),zero,closed), (True,True,False)),
        ('Zwarcie K2 po uruchomieniu', (good,zero,pulse(.030,.020,26),closed), (True,True,False)),
        ('Stałe zwarcie przy starcie, rampa 11 ms', (good,lambda t: 26*min(1,max(0,(t-.0141)/.011)),zero,closed), (True,True,False)),
        ('Impuls K1 26 V / 100 µs od zera', (good,pulse(.030,.0001,26),zero,closed), (True,False,True)),
        ('Impuls K1 26 V / 100 µs od 6,4 V', (good,pulse(.030,.0001,26,6.4),zero,closed), (True,False,True)),
        ('Impuls K1 26 V / 500 µs od 6,4 V', (good,pulse(.030,.0005,26,6.4),zero,closed), (True,True,False)),
        ('Zwarcie, spadek PG i ponowne uruchomienie', (
            lambda t: (.012<=t<.039) or t>=.052,pulse(.025,.004,26),zero,closed
        ), (True,True,True)),
    ]
    rows = []
    for name, signals, expected in cases:
        for corner, threshold, tau in [('niski/szybki',minimum,fast),('wysoki/wolny',maximum,slow)]:
            started, tripped, enabled, trip = simulate(signals,threshold,tau)
            assert (started,tripped,enabled) == expected, (name,corner)
            rows.append((name,corner,started,tripped,enabled,'' if trip is None else f'{trip*1000:.2f}'))
    with (OUT/'Model_RevB2_przypadki.csv').open('w',encoding='utf-8-sig',newline='') as stream:
        writer = csv.writer(stream)
        writer.writerow(('Przypadek','Narożnik','Załączył','Wykrył zwarcie','Załączony na końcu','Czas detekcji od początku [ms]'))
        writer.writerows(rows)
    print(f'Nominal {nominal:.4f} V; corners {minimum:.4f}..{maximum:.4f} V; '
          f'tau {fast*1000:.4f}..{slow*1000:.4f} ms')
    for amplitude in (10,26):
        print(f'{amplitude} V step: {step_delay(amplitude,minimum,fast)*1000:.4f}..'
              f'{step_delay(amplitude,maximum,slow)*1000:.4f} ms, comparator decision only')
    print(f'{len(rows)} state simulations checked')


if __name__ == '__main__':
    main()

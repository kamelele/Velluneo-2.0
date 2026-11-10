"""Add a local flyback bypass capacitor to the valley-fill line model."""
import csv
from itertools import product
from math import exp, pi, sin, sqrt

from model_revh_input import BRIDGE_DROP, DEST, LINE_HZ, R1, summarize


def simulate(line_v, caps_uf, load_w, charge_r, esr, bypass_uf, dt=2e-6):
    capacitance_a, capacitance_b = (c * 1e-6 for c in caps_uf)
    capacitor_step = bypass_uf * 1e-6 / dt
    resistor_charge = charge_r + 2 * esr
    equivalent_load = capacitor_step + 1 / 1.02e6
    resistance = R1 + 6.42  # Allow for the new L1 up to 4.5 ohm, F1, source and wiring.
    decay = exp(-resistance * dt / .0012)
    period = round(1 / (LINE_HZ * dt))
    peak = sqrt(2) * line_v
    va = vb = .46 * peak
    bus = va - .85
    current = 0.0
    peak_a = peak_b = charge_loss = sum_ia2 = sum_ib2 = 0.0
    rows = []
    for step in range(14 * period):
        phase = 2 * pi * (step + .5) / period
        voltage = peak * sin(phase)
        rectified = abs(voltage) - BRIDGE_DROP
        target = (rectified - bus) / resistance
        next_current = max(0.0, target + (current - target) * decay)
        average_i = (current + next_current) / 2
        current = next_current
        # The capacitor network is linear within each diode conduction state.
        # Solve that state implicitly to avoid a time step controlled by the smallest RC.
        assert bus > 80
        numerator = capacitor_step * bus + average_i - load_w / bus
        bus = numerator / equivalent_load
        high = max(va, vb) - .85
        low = min(va, vb) - .85
        threshold = va + vb + .85
        if bus > threshold:
            bus = (numerator + threshold / resistor_charge) / (equivalent_load + 1 / resistor_charge)
        elif bus < high:
            bus = (numerator + high / esr) / (equivalent_load + 1 / esr)
            if bus < low:
                bus = (numerator + (high + low) / esr) / (equivalent_load + 2 / esr)
        ich = max(0, (bus - threshold) / resistor_charge)
        ia = ich - max(0, (va - .85 - bus) / esr)
        ib = ich - max(0, (vb - .85 - bus) / esr)
        va += ia * dt / capacitance_a
        vb += ib * dt / capacitance_b
        if step >= 13 * period:
            rows.append((phase, voltage, average_i if voltage >= 0 else -average_i, 0, bus))
            peak_a, peak_b = max(peak_a, va), max(peak_b, vb)
            charge_loss += ich**2 * charge_r / period
            sum_ia2 += ia**2
            sum_ib2 += ib**2
    s = summarize(line_v, rows)
    return (*s[:3], *s[4:], peak_a, peak_b, sqrt(sum_ia2 / period), sqrt(sum_ib2 / period), charge_loss)


if __name__ == '__main__':
    fields = ('line_Vrms', 'cap_A_uF', 'cap_B_uF', 'flyback_load_W', 'charge_series_ohm',
              'assumed_ESR_ohm', 'effective_HF_uF', 'input_W', 'line_Irms_A', 'line_Ipk_A',
              'R1_W', 'bulk_min_V', 'bulk_max_V', 'PF', 'displacement_factor', 'THDi_ratio',
              'I3_I1', 'I5_I1', 'I7_I1', 'I9_I1', 'I11_I1', 'cap_A_peak_V', 'cap_B_peak_V',
              'cap_A_Irms_A', 'cap_B_Irms_A', 'charge_resistor_W')
    with (DEST / 'Model_valley_fill_HF.csv').open('w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(fields)
        for line, caps, esr, bypass in product((207, 230, 253), ((2.64, 2.64), (2.64, 3.96),
                                                               (3.3, 3.3), (3.96, 3.96)),
                                               (8, 75), (.12, .18, .24, .30, .65, 1.0)):
            result = simulate(line, caps, 8.4, 180, esr, bypass)
            writer.writerow((line, *caps, 8.4, 180, esr, bypass, *(f'{v:.5f}' for v in result)))
    one = simulate(230, (3.3, 3.3), 8.4, 180, 8, .65)
    two = simulate(230, (3.3, 3.3), 8.4, 180, 8, .65, 1e-6)
    assert abs(one[6] - two[6]) < .005 and abs(one[4] - two[4]) < .5 and abs(one[11] - two[11]) < .005
    print(one)

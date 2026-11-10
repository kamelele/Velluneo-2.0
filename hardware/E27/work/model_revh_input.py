"""Screen the line-frequency front end and cold-charge stress of E27 Rev H."""
import csv
from itertools import product
from math import cos, exp, pi, sin, sqrt
from pathlib import Path


DEST = Path('outputs/Zasilacz_RevH_Moc')
LINE_HZ = 50
BRIDGE_DROP = 1.60
R1 = 22.0
L1 = .001
OTHER_R = 4.0  # 2.08 ohm L1 plus an allowance for F1, source and contacts.


def waveform(line_v, capacitance_uf, load_w, dt=2e-6):
    """Track conduction after the bulk capacitor is charged; ignore switching ripple."""
    capacitance = capacitance_uf * 1e-6
    resistance = R1 + OTHER_R
    decay = exp(-resistance * dt / L1)
    period = round(1 / (LINE_HZ * dt))
    peak_v = line_v * sqrt(2)
    voltage = .94 * peak_v
    current = 0.0
    rows = []
    for step in range(10 * period):
        phase = 2 * pi * (step + .5) / period
        line = peak_v * sin(phase)
        target = (abs(line) - BRIDGE_DROP - voltage) / resistance
        next_current = max(0, target + (current - target) * decay)
        charge = (current + next_current) / 2
        assert voltage > 100  # The constant-power approximation applies to the charged bus only.
        capacitor_i = charge - load_w / voltage - voltage / 1.02e6
        voltage += capacitor_i * dt / capacitance
        current = next_current
        if step >= 9 * period:
            rows.append((phase, line, charge if line >= 0 else -charge, capacitor_i, voltage))

    return summarize(line_v, rows)


def summarize(line_v, rows):
    period = len(rows)
    pin = sum(v * i for _, v, i, _, _ in rows) / period
    rms = sqrt(sum(i**2 for _, _, i, _, _ in rows) / period)
    fundamental_sin = sum(i * sin(phase) for phase, _, i, _, _ in rows) * 2 / period
    fundamental_cos = sum(i * cos(phase) for phase, _, i, _, _ in rows) * 2 / period
    fundamental_peak = sqrt(fundamental_sin**2 + fundamental_cos**2)
    harmonics = [
        sqrt(sum(i * sin(n * phase) for phase, _, i, _, _ in rows)**2
             + sum(i * cos(n * phase) for phase, _, i, _, _ in rows)**2) * 2 / period
        for n in (3, 5, 7, 9, 11)
    ]
    capacitor_rms = sqrt(sum(i**2 for _, _, _, i, _ in rows) / period)
    return (pin, rms, max(abs(i) for _, _, i, _, _ in rows), capacitor_rms, rms**2 * R1,
            min(v for *_, v in rows), max(v for *_, v in rows), pin / (line_v * rms),
            fundamental_sin / fundamental_peak,
            sqrt(max(0, 2 * rms**2 / fundamental_peak**2 - 1)),
            *(h / fundamental_peak for h in harmonics))


def valley_fill(line_v, capacitance_uf, load_w, charge_r, dt=2e-6):
    """Screen matched valley-fill capacitors with idealized diode states."""
    period = round(1 / (LINE_HZ * dt))
    capacitance = capacitance_uf * 1e-6
    resistance = R1 + OTHER_R
    peak_v = line_v * sqrt(2)
    cap_v = .46 * peak_v
    cap_max = charge_loss = 0.0
    diode_v = .85
    rows = []

    def bus_for(voltage, charge_gain):
        conductance_factor = 1 + charge_gain + resistance / 1.02e6
        return (voltage + sqrt(max(0, voltage**2 - 4 * conductance_factor * resistance * load_w))) / (2 * conductance_factor)

    for step in range(10 * period):
        phase = 2 * pi * (step + .5) / period
        line = peak_v * sin(phase)
        source_v = max(0, abs(line) - BRIDGE_DROP)
        direct_v = bus_for(source_v, 0)
        cap_i = 0.0
        if direct_v < cap_v - diode_v:
            bus_v = cap_v - diode_v
            line_i = max(0, (source_v - bus_v) / resistance)
            cap_i = (line_i - load_w / bus_v - bus_v / 1.02e6) / 2
        elif direct_v > 2 * cap_v + diode_v:
            level = 2 * cap_v + diode_v
            gain = resistance / charge_r
            bus_v = bus_for(source_v + gain * level, gain)
            line_i = (source_v - bus_v) / resistance
            cap_i = (bus_v - level) / charge_r
        else:
            bus_v = direct_v
            line_i = (source_v - bus_v) / resistance
        cap_v += cap_i * dt / capacitance
        if step >= 9 * period:
            rows.append((phase, line, line_i if line >= 0 else -line_i, cap_i, bus_v))
            cap_max = max(cap_max, cap_v)
            charge_loss += max(0, cap_i)**2 * charge_r / period
    return summarize(line_v, rows), (cap_max, charge_loss)


def unequal_valley_fill(line_v, capacitances_uf, load_w, charge_r, esr, dt=4e-6):
    """Resolve separate capacitor voltages and finite series resistance."""
    period = round(1 / (LINE_HZ * dt))
    peak_v = line_v * sqrt(2)
    resistance = R1 + OTHER_R
    ca, cb = (c * 1e-6 for c in capacitances_uf)
    va = vb = .46 * peak_v
    diode_v = .85
    cap_max_a = cap_max_b = sum_ia2 = sum_ib2 = 0.0
    rows = []

    def bus_for(voltage, charge_gain):
        factor = 1 + charge_gain + resistance / 1.02e6
        return (voltage + sqrt(max(0, voltage**2 - 4 * factor * resistance * load_w))) / (2 * factor)

    for step in range(12 * period):
        phase = 2 * pi * (step + .5) / period
        line = peak_v * sin(phase)
        source = max(0, abs(line) - BRIDGE_DROP)
        direct = bus_for(source, 0)
        ia = ib = 0.0
        if direct < max(va, vb) - diode_v:
            upper = max(va, vb) - diode_v
            lower = upper - 25
            for _ in range(17):
                v = (lower + upper) / 2
                supplied = (max(0, (source - v) / resistance)
                            + max(0, (va - diode_v - v) / esr)
                            + max(0, (vb - diode_v - v) / esr))
                if supplied > load_w / v + v / 1.02e6:
                    lower = v
                else:
                    upper = v
            bus = (lower + upper) / 2
            line_i = max(0, (source - bus) / resistance)
            ia = -max(0, (va - diode_v - bus) / esr)
            ib = -max(0, (vb - diode_v - bus) / esr)
        elif direct > va + vb + diode_v:
            charge_threshold = va + vb + diode_v
            charge_resistance = charge_r + 2 * esr
            gain = resistance / charge_resistance
            bus = bus_for(source + gain * charge_threshold, gain)
            ia = ib = (bus - charge_threshold) / charge_resistance
            line_i = (source - bus) / resistance
        else:
            bus = direct
            line_i = (source - bus) / resistance
        va += ia * dt / ca
        vb += ib * dt / cb
        if step >= 11 * period:
            rows.append((phase, line, line_i if line >= 0 else -line_i, 0.0, bus))
            cap_max_a = max(cap_max_a, va)
            cap_max_b = max(cap_max_b, vb)
            sum_ia2 += ia**2
            sum_ib2 += ib**2
    data = summarize(line_v, rows)
    return (*data[:3], *data[4:], cap_max_a, cap_max_b, sqrt(sum_ia2 / period), sqrt(sum_ib2 / period))


def cold_charge(line_v, capacitance_uf, resistance):
    """Rectified peak step into an empty capacitor through an ideal resistor."""
    peak = line_v * sqrt(2)
    c = capacitance_uf * 1e-6
    return peak / resistance, peak**2 * c / (2 * resistance), c * peak**2 / 2


def main():
    header = ('line_Vrms', 'bulk_uF', 'flyback_load_W', 'input_W', 'line_Irms_A', 'line_Ipk_A',
              'bulk_cap_Irms_A', 'R1_W', 'bulk_min_V', 'bulk_max_V', 'PF', 'displacement_factor',
              'THDi_ratio', 'I3_I1', 'I5_I1', 'I7_I1', 'I9_I1', 'I11_I1')
    with (DEST / 'Model_wejscia.csv').open('w', newline='', encoding='utf8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(header)
        for line, cap, load in product((207, 230, 253), (4.7, 6.8, 8, 10, 12), (7.8, 8.4)):
            data = waveform(line, cap, load)
            writer.writerow((line, cap, load, *(f'{v:.5f}' for v in data)))
    baseline = waveform(230, 10, 8.4)
    fine = waveform(230, 10, 8.4, 1e-6)
    assert max(abs(a - b) / max(abs(b), .01) for a, b in zip(baseline, fine)) < .005
    cold = cold_charge(253, 12, R1 * .95)
    assert .03 < cold[1] < .04 and .76 < cold[2] < .78
    with (DEST / 'Model_valley_fill.csv').open('w', newline='', encoding='utf8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow((*header[:3], 'charge_series_ohm', *header[3:], 'cap_peak_V', 'charge_resistor_W'))
        for line, cap, load, charge_r in product((207, 230, 253), (2.64, 3.3, 3.76, 3.96, 4.7, 5.64, 6.8, 10, 15), (7.8, 8.4), (33, 68, 120, 180)):
            data, cap_stats = valley_fill(line, cap, load, charge_r)
            writer.writerow((line, cap, load, charge_r, *(f'{v:.5f}' for v in (*data, *cap_stats))))
    vf, _ = valley_fill(230, 10, 8.4, 68)
    finer, _ = valley_fill(230, 10, 8.4, 68, 1e-6)
    assert max(abs(a - b) / max(abs(b), .01) for a, b in zip(vf, finer)) < .005
    print('230 VAC, 2 x 10 uF VF, 68 ohm, 8.4 W:', ', '.join(f'{v:.4f}' for v in vf))
    with (DEST / 'Model_valley_fill_tolerancje.csv').open('w', newline='', encoding='utf8') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(('line_Vrms', 'cap_A_uF', 'cap_B_uF', 'flyback_load_W', 'charge_series_ohm',
                         'assumed_ESR_ohm', *header[3:6], *header[7:], 'cap_A_peak_V', 'cap_B_peak_V',
                         'cap_A_Irms_A', 'cap_B_Irms_A'))
        combinations = ((2.64, 2.64), (2.64, 3.96), (3.3, 3.3), (3.96, 3.96))
        for line, caps, load, charge_r, esr in product((207, 230, 253), combinations, (7.8, 8.4), (171, 189), (8, 30, 75)):
            data = unequal_valley_fill(line, caps, load, charge_r, esr)
            writer.writerow((line, *caps, load, charge_r, esr, *(f'{v:.5f}' for v in data)))
    # Check the conduction solver when identical capacitors approach zero ESR.
    equal = unequal_valley_fill(230, (3.3, 3.3), 8.4, 180, .25)
    vf_equal, _ = valley_fill(230, 3.3, 8.4, 180)
    assert abs(equal[4] - vf_equal[5]) < .5 and abs(equal[6] - vf_equal[7]) < .003
    print('230 VAC, 10 uF, 8.4 W:', ', '.join(f'{v:.4f}' for v in baseline))
    print('253 VAC, 12 uF, R1 min only: Ipk %.2f A, %.4f A^2s, %.3f J' % cold)


if __name__ == '__main__':
    main()

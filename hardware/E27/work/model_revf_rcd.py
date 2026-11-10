"""Screen primary RCD stresses with a periodic, idealized leakage pulse."""
from dataclasses import dataclass
from itertools import product
from math import exp, expm1, sqrt
from pathlib import Path
import csv


@dataclass(frozen=True)
class Clamp:
    name: str
    resistance: tuple[float, ...]
    capacitance: tuple[float, ...]
    capacitor_rating: float
    resistor_rating: float
    diode_rating: float


REV_F = Clamp('Rev F', (1e6,), (1.50e-9, 0.75e-9, 1.65e-9), 200, 200, 600)
REV_G = Clamp('Rev G', (82e3, 82e3), (2.20e-9, 2.07e-9, 2.33e-9), 630, 200, 1000)
DRAIN_TARGET = 580
HIGH_LINE = 253 * sqrt(2)
RING_RESERVE = 20
THERMAL_BUDGET_PER_RESISTOR = .15
NOMINAL = (1.2e-3, 97, 8, 55e3)


def periodic(leakage, inductance, reflected, magnetic_power, frequency, cap, resistors):
    """Treat the current discharge as instantaneous and keep Vref fixed."""
    resistance = sum(resistors)
    time = 1 / frequency
    energy = leakage * magnetic_power / inductance * time
    x = time / (resistance * cap)
    a = exp(-x)
    # C*(Vpeak - Vmin)*(Vmid - Vref) = energy, with Vmin = a*Vpeak.
    b = energy * (1 + a) / (2 * cap * -expm1(-x))
    midpoint = (reflected + sqrt(reflected**2 + 4 * b)) / 2
    peak = 2 * midpoint / (1 + a)
    minimum = a * peak
    mean_square = peak**2 * -expm1(-2 * x) / (2 * x)
    power = mean_square / resistance
    share = max(resistors) / resistance
    # Drain includes D5 forward drop, trace inductance and ringing allowance.
    drain = HIGH_LINE + peak + RING_RESERVE
    diode_reverse = HIGH_LINE + peak
    assert abs(cap * (peak - minimum) * (midpoint - reflected) - energy) < 1e-12
    assert abs(cap * (peak**2 - minimum**2) / 2 - power * time) < 1e-12
    return minimum - reflected, peak, drain, diode_reverse, peak * share, power * share, power


def screen(clamp, leakage_uh, corner):
    leakage = leakage_uh * 1e-6
    if corner == 'nominal':
        results = [periodic(leakage, *NOMINAL, clamp.capacitance[0], clamp.resistance)]
    else:
        # Independent screening ranges, not measured operating waveforms.
        tolerances = product((.95, 1.05), repeat=len(clamp.resistance))
        resistors = [tuple(r * f for r, f in zip(clamp.resistance, row)) for row in tolerances]
        inputs = product((1.104e-3, 1.296e-3), (95, 101), (7.5, 9.2), (35e3, 80e3),
                         clamp.capacitance[1:], resistors)
        results = [periodic(leakage, *args) for args in inputs]
    margin = min(r[0] for r in results)
    peak, drain, reverse, resistor, single, total = [max(column) for column in zip(*results)][1:]
    rated = peak < clamp.capacitor_rating and resistor < clamp.resistor_rating and reverse < clamp.diode_rating
    passes = margin > 0 and rated and drain <= DRAIN_TARGET and single <= THERMAL_BUDGET_PER_RESISTOR
    return [clamp.name, leakage_uh, corner, len(results), f'{margin:.2f}', f'{peak:.2f}', f'{drain:.2f}',
            f'{reverse:.2f}', f'{resistor:.2f}', f'{single:.4f}', f'{total:.4f}', int(rated), int(passes)]


if __name__ == '__main__':
    output = Path('outputs/Zasilacz_RevG_Moc/Model_RCD.csv')
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open('w', encoding='utf8', newline='') as file:
        writer = csv.writer(file, lineterminator='\n')
        writer.writerow(['revision', 'leakage_uH', 'case', 'combinations', 'min_margin_above_reflected_V',
                         'max_clamp_peak_V', 'max_drain_screen_V', 'max_diode_reverse_V',
                         'max_voltage_per_resistor_V', 'max_power_per_resistor_W',
                         'max_resistor_total_W', 'within_voltage_ratings', 'within_screen_targets'])
        for clamp, leakage, corner in product((REV_F, REV_G), (1, 2, 3, 5, 8, 10, 12, 15, 20, 25),
                                                ('nominal', 'envelope')):
            writer.writerow(screen(clamp, leakage, corner))
    print(output)

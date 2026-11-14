"""Reproduce the two-level D5 probe and timing screens (Python 3.11+)."""
from itertools import product
from math import exp, inf, log1p

from check_8s_two_contact import CONTACT_MAX, PROBE_RESISTOR, RAW_MAX, RAW_MIN

STRONG = 2 * PROBE_RESISTOR
WEAK = STRONG + 4700
SAMPLE = 0.100
PULSE_SET = 180_000
CLOCK_SET = 523_000


def parallel(a, b):
    return 1 / (1 / a + 1 / b)


def response(raw, series, capacitance, resistance, knee=0):
    """Step from zero into C in parallel with a piecewise-linear load."""
    conducting_at = 0.0
    if knee:
        # Below the knee, only the contact capacitor takes current.
        conducting_at = -series * capacitance * log1p(-knee / raw)
        if SAMPLE <= conducting_at:
            return raw * (1 - exp(-SAMPLE / (series * capacitance)))
    steady = (raw / series + knee / resistance) * parallel(series, resistance)
    time_constant = parallel(series, resistance) * capacitance
    return steady + (knee - steady) * exp(-(SAMPLE - conducting_at) / time_constant)


def difference(raw, cap, resistance, knee=0, strong_scale=1.0, added_scale=1.0):
    strong_series = STRONG * strong_scale
    weak = response(raw, strong_series + (WEAK - STRONG) * added_scale, cap, resistance, knee)
    strong = response(raw, strong_series, cap, resistance, knee)
    return weak, strong, strong - weak


def screen_loads():
    # The knee and slope describe assumed LED behavior, with no measured LED data.
    diode = [
        difference(raw, cap, resistance, knee, strong_scale, added_scale)
        for raw, cap, resistance, knee, strong_scale, added_scale in product(
            (RAW_MIN, RAW_MAX), (0.1e-6, 1e-6), (40, 300), (16, 23.5), (0.99, 1.01), (0.99, 1.01)
        )
    ]
    # Scan the resistive range that overlaps the illustrative strong-pulse band.
    resistors = [
        point for raw, cap, strong_scale, added_scale, resistance in product(
            (RAW_MIN, RAW_MAX), (0.1e-6, 1e-6), (0.99, 1.01), (0.99, 1.01), range(1_000, 31_000, 10)
        )
        if 16 <= (point := difference(raw, cap, resistance, strong_scale=strong_scale, added_scale=added_scale))[1] <= 24
    ]
    max_led_delta = max(row[2] for row in diode)
    min_resistive_delta = min(row[2] for row in resistors)
    limited_open = response(RAW_MIN, WEAK * 1.01, 1e-6, inf)
    larger_open = response(RAW_MIN, WEAK * 1.01, 10e-6, inf)
    assert max_led_delta < min_resistive_delta
    assert limited_open > 24 > larger_open
    print(f"Max modeled LED delta (1 uF envelope): {max_led_delta:.3f} V")
    print(f"Min pure resistor delta in strong window: {min_resistive_delta:.3f} V")
    print(f"Weak open response at 100 ms (1 uF vs 10 uF): {limited_open:.2f} V vs {larger_open:.2f} V")
    sample_current = (RAW_MIN - 23.5) / (WEAK * 1.01)
    print(f"Weak current at illustrative upper LED voltage: {sample_current*1000:.3f} mA; "
          f"shunt signal: {sample_current * 0.22 * 1e6:.1f} uV")


def divider_ratio(top, bottom, ideal):
    ratios = [lo / (hi + lo) for hi, lo in product(
        (0.99 * top, 1.01 * top), (0.99 * bottom, 1.01 * bottom)
    )]
    # Include the datasheet's DIV input leakage through divider impedance at 2.25 V.
    allowance = 10e-9 * parallel(top * 1.01, bottom * 1.01) / 2.25
    assert ideal - 0.015 < min(ratios) - allowance
    assert max(ratios) + allowance < ideal + 0.015


def screen_overvoltage():
    top, bottom = 698_000, 10_000
    highest = top * 1.001
    lowest = top * 0.999
    leak = 25e-9
    rising = (
        0.397 * (1 + lowest / (bottom * 1.001)) - leak * highest,
        0.403 * (1 + highest / (bottom * 0.999)) + leak * highest,
    )
    falling_min = 0.387 * (1 + lowest / (bottom * 1.001)) - leak * highest
    assert RAW_MAX < falling_min <= rising[1] < CONTACT_MAX
    print(f"Probe RAW protection trip: {rising[0]:.2f} to {rising[1]:.2f} V; "
          f"minimum rearm: {falling_min:.2f} V")


def screen_timing():
    divider_ratio(1_000_000, 523_000, 0.34375)
    divider_ratio(976_000, 182_000, 0.15625)
    nominal_width = (32768 * PULSE_SET / 50_000) * 1e-6
    min_width = nominal_width * 0.99 * 0.977
    max_width = nominal_width * 1.01 * 1.023
    period = (1024 * 64 * CLOCK_SET / 50_000) * 1e-6
    # Frequency error is inverted when calculating minimum period.
    min_period = period * 0.99 / 1.022
    min_off = min_period - max_width
    short_draw = CONTACT_MAX**2 / (STRONG * 0.99)
    assert SAMPLE < min_width <= max_width < 0.125
    assert min_off > 0.5
    print(f"Pulse width: {min_width*1000:.2f} to {max_width*1000:.2f} ms")
    print(f"Minimum normal off interval: {min_off*1000:.2f} ms")
    print(f"Strong short: {short_draw * max_width * 1000:.2f} mJ input per pulse, "
          f"{short_draw * max_width / min_period * 1000:.2f} mW input average")


if __name__ == "__main__":
    screen_loads()
    screen_timing()
    screen_overvoltage()

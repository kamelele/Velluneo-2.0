"""Calculate bench-study bounds for the two-contact output stage."""
from math import exp, log

RAW_MIN = 26.33
RAW_MAX = 27.07
CONTACT_MAX = 30.0
CAPACITANCE = 10e-6
PROBE_SAMPLE = 0.100
PROBE_MAX = 0.125
PROBE_PAUSE_MIN = 0.5
PROBE_RESISTOR = 1100
BLEED_RESISTOR = 4700


def evaluate():
    series_high = 2 * PROBE_RESISTOR * 1.01
    series_low = 2 * PROBE_RESISTOR * 0.99
    short_current = CONTACT_MAX / series_low
    one_short_current = CONTACT_MAX / (PROBE_RESISTOR * 0.99)
    input_energy = CONTACT_MAX * short_current * PROBE_MAX
    average_power = input_energy / (PROBE_PAUSE_MIN + PROBE_MAX)
    discharge = BLEED_RESISTOR * 1.01 * CAPACITANCE * log(CONTACT_MAX / 5)
    open_voltage = RAW_MIN * (1 - exp(-PROBE_SAMPLE / (series_high * CAPACITANCE)))
    # Illustrative 8S probe band. Actual boundaries await cold/hot testing.
    load_min, load_max = 16.0, 23.5
    load_current_min = (RAW_MIN - load_max) / series_high
    load_current_max = (RAW_MAX - load_min) / series_low
    # Worst-case power that any resistive load can draw from the probe.
    max_resistive_load_energy = CONTACT_MAX**2 / (4 * series_low) * PROBE_MAX
    nominal_raw = (RAW_MIN + RAW_MAX) / 2
    resistive_alias = [2 * PROBE_RESISTOR * voltage / (nominal_raw - voltage)
                       for voltage in (load_min, load_max)]
    assert open_voltage > load_max
    assert discharge < 0.1
    assert load_current_min > 0
    print(f"Open voltage after 100 ms (ideal switched bleeder off): {open_voltage:.2f} V")
    print(f"Illustrative valid voltage window: {load_min:.1f} to {load_max:.1f} V")
    print(f"Corresponding steady probe current: {load_current_min*1000:.2f} to {load_current_max*1000:.2f} mA")
    print(f"Probe hard-short current: {short_current*1000:.2f} mA; one resistor short: {one_short_current*1000:.2f} mA")
    print(f"Probe input energy: {input_energy*1000:.1f} mJ; average input: {average_power*1000:.1f} mW")
    print(f"Probe resistive load energy over 125 ms: {max_resistive_load_energy*1000:.1f} mJ")
    print(f"Resistive loads mimicking the voltage window at nominal RAW: "
          f"{resistive_alias[0]/1000:.2f} to {resistive_alias[1]/1000:.2f} kohm")
    print(f"Discharge after cutoff: {discharge*1000:.1f} ms; allowance before cutoff: {(0.1-discharge)*1000:.1f} ms")


if __name__ == "__main__":
    evaluate()

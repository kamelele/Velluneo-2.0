"""Screen the 8S restart policies and the proposed supply-valid detector."""

from enum import Enum, auto
from itertools import product


class State(Enum):
    OFF = auto()
    RUN = auto()
    LOCKED = auto()


def transition(state, *, rail_valid, interlock, fault, reset_authorized):
    if state is State.LOCKED:
        if reset_authorized and not fault:
            return State.OFF
        return State.LOCKED
    if fault:
        return State.LOCKED
    return State.RUN if rail_valid and interlock else State.OFF


def detector_limits(pin_min, pin_max):
    # 1% initial resistors, 25 nA as a screening allowance.
    return (
        pin_min * (1 + 64_900 * 0.99 / (10_000 * 1.01)) - 25e-9 * 64_900 * 0.99,
        pin_max * (1 + 64_900 * 1.01 / (10_000 * 0.99)) + 25e-9 * 64_900 * 1.01,
    )


def check():
    falling = detector_limits(0.397, 0.403)
    rising = detector_limits(0.400, 0.413)
    assert falling[0] > 1.65
    assert rising[1] < 3.234
    for rail_valid, interlock, fault in product((False, True), repeat=3):
        assert transition(State.LOCKED, rail_valid=rail_valid, interlock=interlock,
                          fault=fault, reset_authorized=False) is State.LOCKED

    # Loss of D3's volatile state allows a new enable once the rails and loop return.
    returned_inputs = dict(rail_valid=True, interlock=True, fault=False, reset_authorized=False)
    assert transition(State.OFF, **returned_inputs) is State.RUN
    assert transition(State.LOCKED, **returned_inputs) is State.LOCKED
    assert transition(State.LOCKED, rail_valid=True, interlock=True, fault=True,
                      reset_authorized=True) is State.LOCKED

    # Screen R33 at its low corner for sink demand and high corner for enable.
    # Include a 10 uA allowance for eFuse pin current and 300 nA detector leakage.
    clamp_current = (3.366 - 0.25) / (1200 * 0.99) + 10e-6
    r33_high = 1200 * 1.01
    r18_low = 10_000 * 0.99
    permit_return = 2.35
    enable_voltage = (permit_return - r33_high * 10.3e-6) / (1 + r33_high / r18_low)
    assert clamp_current < 3e-3
    assert 0.25 < 0.55
    assert enable_voltage > 1.0

    reservoir = 0.5 * (470e-6 * 1.2) * 27.07**2
    source_screen = 27.07 * 0.285 * 0.0376
    print(f"Supply detector, falling: {falling[0]:.3f} to {falling[1]:.3f} V")
    print(f"Supply detector, rising:  {rising[0]:.3f} to {rising[1]:.3f} V")
    print(f"SHDN clamp current screen: {clamp_current * 1e3:.3f} mA at 0.25 V")
    print(f"SHDN enable screen at 2.35 V return: {enable_voltage:.3f} V")
    print(f"Reservoir inventory (470 uF +20%): {reservoir:.3f} J")
    print(f"Flyback energy screen (37.6 ms): {source_screen:.3f} J")
    print("Retained-state policy checks passed")


if __name__ == "__main__":
    check()

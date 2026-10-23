"""Tests for microtubule-stars. Run: python tests.py"""

import math
import random

from microstars import (init_ring, make_patterns, cue_phases, state_vector,
                        recall, drive_value, step, plv, trial, experiment)


def test_trial_deterministic():
    a = trial(11)[:2]
    b = trial(11)[:2]
    assert a == b


def test_control_recall_beats_chance():
    # cued pattern survives washout well above chance (1/8 = 0.125)
    d, f = experiment(list(range(20)), eps=0.0,
                      modes=((1.0, 0.002, 0.0),))
    assert d > 0.25, d


def test_drive_degrades_recall():
    # the finding: slow modulation hurts, monotonically
    seeds = list(range(20))
    kw = dict(modes=((1.0, 0.002, 0.0), (0.5, 0.005, 1.0)))
    d0, _ = experiment(seeds, eps=0.0, **kw)
    d1, _ = experiment(seeds, eps=0.15, **kw)
    d2, _ = experiment(seeds, eps=0.60, **kw)
    assert d0 > d1 > d2, (d0, d1, d2)


def test_no_cross_scale_locking():
    _, _, psis = trial(7, eps=0.35, modes=((1.0, 0.002, 0.0),))
    angs = [(2 * math.pi * 0.002 * t) % (2 * math.pi) for t in range(400)]
    assert plv(psis, angs) < 0.05


def test_clean_cue_recalls():
    rng = random.Random(21)
    pats = make_patterns(4, 32, rng)
    s = state_vector(cue_phases(pats[2], 0.05, rng))
    w, wt = recall(s, pats)
    assert w == 2 and wt > 0.5


def test_drive_value_known():
    v = drive_value(0.0, ((1.0, 0.002, 0.0),))
    assert abs(v - 0.0) < 1e-12
    v = drive_value(125.0, ((1.0, 0.002, 0.0),))  # quarter period
    assert abs(v - 1.0) < 1e-9


def test_step_preserves_phases():
    rng = random.Random(22)
    omegas, phases = init_ring(16, 0.06, 0.01, rng)
    p2, r, psi = step(phases, omegas, 0.05, 0.3, 0.5)
    assert len(p2) == 16 and all(0.0 <= x < 2 * math.pi for x in p2)
    assert 0.0 <= r <= 1.0


def test_plv_identical_is_one():
    angs = [i * 0.1 for i in range(100)]
    assert abs(plv(angs, angs) - 1.0) < 1e-9


if __name__ == "__main__":
    for name, fn in sorted(
            [(k, v) for k, v in globals().items() if k.startswith("test_")]):
        fn()
        print(f"PASS {name}")
    print("all tests passed")

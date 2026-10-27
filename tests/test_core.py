import math
import random

import pytest

from microtubule_stars import (cue_phases, drive_value, experiment, init_ring,
                               make_patterns, plv, recall, state_vector, step,
                               trial)


def test_trial_deterministic():
    assert trial(11)[:2] == trial(11)[:2]


def test_control_recall_beats_chance():
    d, _ = experiment(list(range(20)), eps=0.0, modes=((1.0, 0.002, 0.0),))
    assert d > 0.25


def test_drive_degrades_recall_monotonically():
    seeds = list(range(20))
    modes = ((1.0, 0.002, 0.0), (0.5, 0.005, 1.0))
    d0, _ = experiment(seeds, eps=0.0, modes=modes)
    d1, _ = experiment(seeds, eps=0.15, modes=modes)
    d2, _ = experiment(seeds, eps=0.60, modes=modes)
    assert d0 > d1 > d2


def test_no_cross_scale_locking():
    _, _, psis = trial(7, eps=0.35, modes=((1.0, 0.002, 0.0),))
    angs = [(2 * math.pi * 0.002 * t) % (2 * math.pi) for t in range(400)]
    assert plv(psis, angs) < 0.05


def test_clean_cue_recalls():
    rng = random.Random(21)
    pats = make_patterns(4, 32, rng)
    w, wt = recall(state_vector(cue_phases(pats[2], 0.05, rng)), pats)
    assert w == 2 and wt > 0.5


def test_drive_value_known():
    assert abs(drive_value(0.0, ((1.0, 0.002, 0.0),))) < 1e-12
    assert abs(drive_value(125.0, ((1.0, 0.002, 0.0),)) - 1.0) < 1e-9


def test_step_preserves_phases():
    rng = random.Random(22)
    omegas, phases = init_ring(16, 0.06, 0.01, rng)
    p2, r, psi = step(phases, omegas, 0.05, 0.3, 0.5)
    assert len(p2) == 16 and all(0.0 <= x < 2 * math.pi for x in p2)
    assert 0.0 <= r <= 1.0


def test_plv_identical_is_one():
    angs = [i * 0.1 for i in range(100)]
    assert abs(plv(angs, angs) - 1.0) < 1e-9


def test_demo_numbers_match_measured_table():
    """The README table: control dwell ~0.391, drive degrades, PLV ~0.006."""
    modes = ((1.0, 0.002, 0.0), (0.5, 0.005, 1.0))
    seeds = list(range(30))
    d0, f0 = experiment(seeds, eps=0.0, modes=modes)
    d6, f6 = experiment(seeds, eps=0.60, modes=modes)
    assert abs(d0 - 0.391) < 0.005 and abs(f0 - 0.454) < 0.005
    assert abs(d6 - 0.297) < 0.005
    assert d0 > d6
    _, _, psis = trial(7, eps=0.35, modes=modes)
    angs = [(2 * math.pi * 0.002 * t) % (2 * math.pi) for t in range(400)]
    assert abs(plv(psis, angs) - 0.0059) < 0.001


@pytest.mark.parametrize("bad", [
    dict(P=0), dict(N=0), dict(T=0), dict(sigma=-1), dict(modes=()),
])
def test_trial_rejects_bad_input(bad):
    kw = dict(seed=1, P=4, N=16, T=10, modes=((1.0, 0.01, 0.0),), sigma=0.1)
    kw.update(bad)
    with pytest.raises(ValueError):
        trial(**kw)


def test_recall_rejects_length_mismatch():
    with pytest.raises(ValueError):
        recall([1j], [[1j, 0j]])
    with pytest.raises(ValueError):
        recall([], [[1j]])
    with pytest.raises(ValueError):
        experiment([], eps=0.0, modes=((1.0, 0.01, 0.0),))


def test_cli(capsys):
    from microtubule_stars.__main__ import main
    assert main() == 0
    out = capsys.readouterr().out
    assert "SYNTHETIC" in out and "Verified" not in out


def test_paired_bootstrap_is_deterministic_and_brackets_mean():
    from microtubule_stars.__main__ import paired_bootstrap
    diffs = [0.1, 0.2, 0.15, 0.05, 0.12, 0.18]
    m, lo, hi = paired_bootstrap(diffs, n_boot=500)
    assert abs(m - sum(diffs) / len(diffs)) < 1e-12
    assert lo <= m <= hi
    assert (m, lo, hi) == paired_bootstrap(diffs, n_boot=500)


def test_paired_bootstrap_rejects_empty():
    from microtubule_stars.__main__ import paired_bootstrap
    with pytest.raises(ValueError):
        paired_bootstrap([])

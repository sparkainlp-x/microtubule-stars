"""python -m microtubule_stars: print the measured drive scan (SYNTHETIC)."""

import math
import random
import statistics

from .core import plv, trial

DEFAULT_MODES = ((1.0, 0.002, 0.0), (0.5, 0.005, 1.0))
DEFAULT_SEEDS = list(range(30))
CHANCE = 1 / 8
N_BOOT = 5000
BOOT_SEED = 1


def paired_bootstrap(diffs, n_boot=N_BOOT, seed=BOOT_SEED):
    """Mean of paired per-seed differences and a percentile bootstrap 95% interval.

    Resamples the seeds with replacement using a fixed generator, so the output
    is deterministic.
    """
    if not diffs:
        raise ValueError("need at least one paired difference")
    rng = random.Random(seed)
    n = len(diffs)
    means = sorted(sum(rng.choices(diffs, k=n)) / n for _ in range(n_boot))
    lo = means[int(0.025 * n_boot)]
    hi = means[int(0.975 * n_boot) - 1]
    return sum(diffs) / n, lo, hi


def per_seed(seeds, eps, modes):
    """Per-seed (dwell, fidelity) lists, same trials as `experiment`."""
    dw, fi = [], []
    for s in seeds:
        d, f, _ = trial(s, eps=eps, modes=modes)
        dw.append(d)
        fi.append(f)
    return dw, fi


def main(argv=None):
    seeds = DEFAULT_SEEDS
    modes = DEFAULT_MODES
    print("SYNTHETIC: classical Kuramoto ring with holographic phase-pattern "
          "recall. Drive is a model, not stellar data.\n")
    print(f"dwell = fraction of ticks the cued pattern still wins "
          f"(chance = {CHANCE:.3f}; {len(seeds)} seeds)")
    print(f"{'eps':>5} {'dwell':>7} {'fidelity':>9}")
    rows = []
    for eps in (0.0, 0.15, 0.35, 0.60):
        dw, fi = per_seed(seeds, eps, modes)
        d, f = sum(dw) / len(dw), sum(fi) / len(fi)
        rows.append((eps, d, f, dw))
        print(f"{eps:>5.2f} {d:>7.3f} {f:>9.3f}")
    print("\nSpread across seeds and paired effect of the drive "
          "(control dwell minus drive dwell, same seed; "
          f"{N_BOOT}-resample bootstrap 95% interval over seeds)")
    print(f"{'eps':>5} {'dwell SD':>9} {'paired diff':>12} {'95% interval':>16} "
          f"{'seeds drive helped':>19}")
    control = rows[0][3]
    for eps, _d, _f, dw in rows:
        sd = statistics.stdev(dw)
        if eps == 0.0:
            print(f"{eps:>5.2f} {sd:>9.3f} {'(control)':>12}")
            continue
        diffs = [c - x for c, x in zip(control, dw)]
        m, lo, hi = paired_bootstrap(diffs)
        helped = sum(1 for v in diffs if v < 0)
        print(f"{eps:>5.2f} {sd:>9.3f} {m:>12.3f} {f'[{lo:.3f}, {hi:.3f}]':>16} "
              f"{helped:>13d} of {len(diffs)}")
    print("\nAcross scales: phase-locking (one seed)")
    _, _, psis = trial(7, eps=0.35, modes=modes)
    drive_angs = [(2 * math.pi * 0.002 * t) % (2 * math.pi) for t in range(400)]
    print(f"PLV(collective phase, drive) = {plv(psis, drive_angs):.4f}")
    print("\nIn this model, unstructured gain modulation degrades recall "
          "monotonically; there is no 1:1 locking across scales.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

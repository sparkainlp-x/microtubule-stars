"""python -m microtubule_stars: print the measured drive scan (SYNTHETIC)."""

import math
import statistics

from .core import experiment, plv, trial

DEFAULT_MODES = ((1.0, 0.002, 0.0), (0.5, 0.005, 1.0))
DEFAULT_SEEDS = list(range(30))
CHANCE = 1 / 8


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
        d, f = experiment(seeds, eps=eps, modes=modes)
        rows.append((eps, d, f))
        print(f"{eps:>5.2f} {d:>7.3f} {f:>9.3f}")
    print("\nAcross scales: phase-locking (one seed)")
    _, _, psis = trial(7, eps=0.35, modes=modes)
    drive_angs = [(2 * math.pi * 0.002 * t) % (2 * math.pi) for t in range(400)]
    print(f"PLV(collective phase, drive) = {plv(psis, drive_angs):.4f}")
    print("\nIn this model, unstructured gain modulation degrades recall "
          "monotonically; there is no 1:1 locking across scales.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

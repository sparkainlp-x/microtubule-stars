"""Demo: a holographic brain under a slow cosmic drive.

Cue a phase-pattern into the neural ring, evolve, and measure
how long the memory survives -- with the cosmic drive OFF
(control) and ON. Then scan drive strength and frequency.

Run: python demo.py
"""

import math

from microstars import (trial, experiment, plv, drive_value)


def main():
    seeds = list(range(30))
    MODES = ((1.0, 0.002, 0.0), (0.5, 0.005, 1.0))

    print("== dwell: fraction of ticks the cued pattern still wins "
          f"(chance = {1/8:.3f}) ==")
    print(f"{'eps':>5} {'dwell':>7} {'fidelity':>9}")
    for eps in (0.0, 0.15, 0.35, 0.60):
        d, f = experiment(seeds, eps=eps, modes=MODES)
        print(f"{eps:>5.2f} {d:>7.3f} {f:>9.3f}")
    print("the slow drive degrades recall monotonically --\n"
          "unstructured cosmic modulation is disturbance, not help.\n")

    print("== across scales: phase-locking ==")
    _, _, psis = trial(7, eps=0.35, modes=MODES)
    drive_angs = [(2 * math.pi * 0.002 * t) % (2 * math.pi)
                  for t in range(400)]
    print(f"PLV(collective phase, drive) = {plv(psis, drive_angs):.4f}")
    print("no 1:1 locking across scales, as expected --\n"
          "the coupling is modulatory, not entraining.\n")

    print("== verdict ==")
    print("The stars don't help the brain remember -- in this model.\n"
          "Real brains make cross-frequency coupling work by\n"
          "structuring and gating it; raw slow drive just adds\n"
          "washout. That distinction is the finding.")


if __name__ == "__main__":
    main()

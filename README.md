# Microtubule-Stars

A small, standard-library Python simulation of a **classical Kuramoto ring** that stores phase-patterns as one interference record and recalls them by projection. An optional slow multi-mode oscillation modulates the ring's coupling gain — a model of unstructured cross-frequency coupling across scales.

**SYNTHETIC.** Classical simulation only. The slow drive is a *stellar-pulsation-style model*, not stellar data. Nothing here claims cosmic influence on brains, and no quantum mechanics or consciousness model is simulated.

## What it measures

Cue a stored pattern (phases plus noise), evolve the ring for a few hundred ticks, and record the **dwell** (fraction of ticks where the cued pattern still wins) and mean winner fidelity. Compare drive OFF (control) with drive ON at several strengths.

## Measured in this repo

30 seeds, N=64 oscillators, P=8 patterns, T=400 ticks, chance = 1/8 = 0.125. Modes: (1.0, 0.002) and (0.5, 0.005).

| eps (drive strength) | dwell | fidelity |
|---|---|---|
| 0.00 (control) | 0.391 | 0.454 |
| 0.15 | 0.365 | 0.442 |
| 0.35 | 0.327 | 0.432 |
| 0.60 | 0.297 | 0.422 |

- Control dwell (0.391) is about 3× chance: the memory works, and decays under Kuramoto washout.
- The slow drive **degrades** recall monotonically. No rescue at the cue-noise levels tested in the original package.
- Phase-locking value between the collective phase and the drive: **0.0059** (no 1:1 locking across scales). A frequency scan in the design notes shows no resonance peak — flat disruption.

Reading: unstructured gain modulation adds washout variance. Real neural cross-frequency coupling is structured and gated; this model shows what the raw version does.

## Quick start

```bash
python -m microtubule_stars                                    # the table above
pip install -r requirements-dev.txt && python -m pytest -q     # 16 tests, warnings are errors
```

```python
from microtubule_stars import experiment

modes = ((1.0, 0.002, 0.0), (0.5, 0.005, 1.0))
experiment(list(range(30)), eps=0.0, modes=modes)   # control dwell, fidelity
```

Invalid input (empty pattern list, length mismatches, non-positive sizes, negative sigma, empty mode list) raises `ValueError`.

## Honest limits

- Classical Kuramoto only. Literature pointers on microtubules and related topics are in [RESEARCH.md](RESEARCH.md); none of that material is simulated here.
- The drive is a model chosen for scale separation, not measured from any star.
- One memory architecture (phase-pattern hologram). The negative result is about *this* coupling, not all cross-scale coupling.
- Toy scale (N=64, P=8).

See [DESIGN.md](DESIGN.md).

## Provenance

The package as received is kept unchanged in [spec/microtubule-stars/](spec/microtubule-stars/). [CHANGELOG.md](CHANGELOG.md) lists what changed.

## Acknowledgements

Thanks to Mun Seok Lee, who is credited on the original package kept in [spec/microtubule-stars/](spec/microtubule-stars/). The acknowledgement does not imply his endorsement of this code or its conclusions.

## References

- Kuramoto, Y. (1984). *Chemical Oscillations, Waves, and Turbulence.* Springer.
- Canolty, R. T., et al. (2006). High gamma power is phase-locked to theta oscillations in human neocortex. *Science* 313(5793), 1626-1628. https://doi.org/10.1126/science.1128115

## How to cite

See [CITATION.cff](CITATION.cff).

## License

Copyright (c) 2026 Jean-François Brisson, Spark AI NLP.

This software is available under the GNU Affero General Public License v3.0 only (AGPL-3.0-only); see [LICENSE](LICENSE).

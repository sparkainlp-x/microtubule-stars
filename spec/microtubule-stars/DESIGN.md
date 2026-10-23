# DESIGN — microtubule-stars

## What it is

A holographic brain under a slow cosmic drive. A ring of N=64
fast Kuramoto phase oscillators (the neural/microtubule scale)
carries a holographic memory — P phase-patterns stored as one
complex interference record, recall by one-shot projection. A
slow multi-mode oscillation (stellar-pulsation-*style*; a model,
not data) modulates the ring's coupling gain: cross-frequency
coupling extended across scales.

## The experiment

Cue a pattern (phases + noise), evolve T=400 ticks, measure the
dwell fraction (ticks where the cued pattern still wins) and mean
winner fidelity — drive OFF (control) vs ON, over 30 seeds.

## Measured

- Control dwell 0.391 vs chance 0.125: the memory works, decaying
  under Kuramoto washout.
- Drive degrades recall monotonically: eps 0 → 0.15 → 0.35 → 0.6
  gives dwell 0.391 → 0.365 → 0.327 → 0.297. No rescue at any
  cue-noise level tested (σ 0.35/0.6/0.9).
- No 1:1 phase locking across scales (PLV ≈ 0.006); resonance
  scan over drive frequency shows no peak — flat disruption.

## Reading

Gain modulation adds washout variance: high-gain phases
synchronize the ring faster, dissolving the phase pattern.
Real brains make cross-frequency coupling work by structuring
and gating it (phase–amplitude, not raw gain). The model shows
what the unstructured version does — which is why the naive
"cosmic rhythms enhance memory" story fails here.

## Honest limits

- Classical Kuramoto; the quantum material (Orch OR,
  superradiance) is in RESEARCH.md, not in the code.
- The drive is a model, not stellar data; frequencies chosen
  for scale separation, not measured from any star.
- One memory architecture (phase-pattern hologram); the
  negative result is about *this* coupling, not all
  cross-scale coupling.

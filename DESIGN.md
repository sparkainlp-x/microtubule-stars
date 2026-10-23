# Design notes

SYNTHETIC. Classical Kuramoto simulation only. No quantum mechanics and no consciousness model are implemented.

## Construction

1. **Ring.** N=64 phase oscillators with natural frequencies drawn around a mean, evolved with mean-field Kuramoto.
2. **Memory.** P=8 random phase-patterns stored as complex unit vectors. Recall is one-shot projection: the winner is the pattern with largest squared overlap.
3. **Cue.** A stored pattern's phases plus Gaussian noise become the initial state.
4. **Drive (optional).** A slow multi-mode sinusoid modulates the coupling gain as `K * (1 + eps * drive(t))`. The modes are stellar-pulsation-*style* — chosen for scale separation, not taken from stellar data.

## Measured

See the README table (30 seeds). Control dwell ≈ 0.391 (chance 0.125). Raising eps from 0 to 0.6 lowers dwell monotonically to ≈ 0.297. PLV between collective phase and the drive ≈ 0.006. The original package also reported no resonance peak under a drive-frequency scan and no rescue across cue-noise levels σ ∈ {0.35, 0.6, 0.9}.

## Reading

High-gain phases synchronize the ring faster and dissolve the phase pattern. Unstructured slow gain modulation therefore adds washout. That is why a naive "slow rhythms enhance memory" story fails for *this* coupling.

## Limits

- Classical only. Pointers in RESEARCH.md are literature notes, not results of this code.
- Model drive, not stellar data.
- One architecture; toy scale.

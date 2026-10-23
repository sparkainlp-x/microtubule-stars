"""microtubule-stars: a holographic brain under a slow cosmic drive.

A ring of N fast phase oscillators (the neural/microtubule scale)
carries a holographic memory: P phase-patterns stored as one
interference record, recall by projection. A slow multi-mode
oscillation -- stellar-pulsation-style, a MODEL, not data --
modulates the ring's coupling gain. That is cross-frequency
coupling, the real neuroscience motif (slow global rhythms
modulating fast local computation; cf. theta-gamma coupling),
extended across scales as a model.

The question is empirical: does the slow drive stabilize
holographic recall, disrupt it, or do nothing? Measured, not
assumed.

Classical Kuramoto throughout. No quantum mechanics is simulated;
the quantum-gravity and superradiance material lives in
RESEARCH.md, where it belongs.
"""

import math
import random


# ------------------------------------------------------------ the brain
def init_ring(N, omega_mean, omega_spread, rng):
    omegas = [rng.gauss(omega_mean, omega_spread) for _ in range(N)]
    phases = [rng.uniform(0.0, 2 * math.pi) for _ in range(N)]
    return omegas, phases


def make_patterns(P, N, rng):
    """Holographic library: P phase-patterns as complex unit vectors."""
    pats = []
    for _ in range(P):
        angs = [rng.uniform(0.0, 2 * math.pi) for _ in range(N)]
        v = [complex(math.cos(a), math.sin(a)) for a in angs]
        n = math.sqrt(N)
        pats.append([c / n for c in v])
    return pats


def pattern_phases(pattern):
    return [math.atan2(c.imag, c.real) % (2 * math.pi) for c in pattern]


def cue_phases(pattern, sigma, rng):
    return [(a + rng.gauss(0.0, sigma)) % (2 * math.pi)
            for a in pattern_phases(pattern)]


def state_vector(phases):
    N = len(phases)
    n = math.sqrt(N)
    return [complex(math.cos(p), math.sin(p)) / n for p in phases]


def recall(state, patterns):
    """One-shot projection. Returns (winner, winner_weight)."""
    ms = [abs(sum(p[i].conjugate() * state[i]
                  for i in range(len(state)))) ** 2 for p in patterns]
    tot = sum(ms)
    w = max(range(len(ms)), key=lambda i: ms[i])
    return w, (ms[w] / tot if tot else 0.0)


# ------------------------------------------------------------ the stars
def drive_value(t, modes):
    """Slow multi-mode oscillation. modes = [(amp, freq, phase0)].
    Stellar-pulsation-STYLE: a model of slow global modulation,
    not stellar data."""
    return sum(a * math.sin(2 * math.pi * f * t + p0)
               for a, f, p0 in modes)


def step(phases, omegas, K, eps, dval):
    """Mean-field Kuramoto; the cosmic drive modulates the gain."""
    N = len(phases)
    sx = sum(math.cos(p) for p in phases) / N
    sy = sum(math.sin(p) for p in phases) / N
    r = math.hypot(sx, sy)
    psi = math.atan2(sy, sx)
    Kg = K * (1.0 + eps * dval)
    new = [p + w + Kg * r * math.sin(psi - p)
           for p, w in zip(phases, omegas)]
    return [x % (2 * math.pi) for x in new], r, psi


def plv(angles_a, angles_b):
    """Phase-locking value between two angle traces."""
    n = len(angles_a)
    return abs(sum(complex(math.cos(a - b), math.sin(a - b))
                   for a, b in zip(angles_a, angles_b)) / n)


# ------------------------------------------------------------ the experiment
def trial(seed, P=8, N=64, T=400, K=0.05, eps=0.0,
          modes=((1.0, 0.002, 0.0),), sigma=0.35):
    """Cue a pattern, evolve, measure dwell + fidelity.
    eps=0 -> drive off (control)."""
    rng = random.Random(seed)
    omegas, _ = init_ring(N, 0.06, 0.01, rng)
    patterns = make_patterns(P, N, rng)
    k = seed % P
    phases = cue_phases(patterns[k], sigma, rng)
    dwell, fids, psis = 0, [], []
    for t in range(T):
        dval = drive_value(t, modes)
        phases, r, psi = step(phases, omegas, K, eps, dval)
        psis.append(psi)
        w, f = recall(state_vector(phases), patterns)
        if w == k:
            dwell += 1
        fids.append(f)
    return dwell / T, sum(fids) / len(fids), psis


def experiment(seeds, eps, modes, **kw):
    dwells, fids = [], []
    for s in seeds:
        d, f, _ = trial(s, eps=eps, modes=modes, **kw)
        dwells.append(d)
        fids.append(f)
    n = len(seeds)
    return sum(dwells) / n, sum(fids) / n

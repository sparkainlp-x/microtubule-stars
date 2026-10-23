"""Kuramoto ring, holographic phase-pattern memory, and the slow drive.

SYNTHETIC. Classical simulation only.
"""

import math
import random


def _check_positive_int(name, value, minimum=1):
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"{name} must be an integer >= {minimum}, got {value!r}")


def _check_finite(name, value, allow_negative=True):
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number, got {value!r}")
    if not allow_negative and value < 0:
        raise ValueError(f"{name} must be >= 0, got {value!r}")


def init_ring(N, omega_mean, omega_spread, rng):
    """Natural frequencies and initial phases for an N-oscillator ring."""
    _check_positive_int("N", N)
    _check_finite("omega_mean", omega_mean)
    _check_finite("omega_spread", omega_spread, allow_negative=False)
    omegas = [rng.gauss(omega_mean, omega_spread) for _ in range(N)]
    phases = [rng.uniform(0.0, 2 * math.pi) for _ in range(N)]
    return omegas, phases


def make_patterns(P, N, rng):
    """P random phase-patterns as complex unit vectors of length N."""
    _check_positive_int("P", P)
    _check_positive_int("N", N)
    pats = []
    for _ in range(P):
        angs = [rng.uniform(0.0, 2 * math.pi) for _ in range(N)]
        v = [complex(math.cos(a), math.sin(a)) for a in angs]
        n = math.sqrt(N)
        pats.append([c / n for c in v])
    return pats


def pattern_phases(pattern):
    if not pattern:
        raise ValueError("pattern is empty")
    return [math.atan2(c.imag, c.real) % (2 * math.pi) for c in pattern]


def cue_phases(pattern, sigma, rng):
    _check_finite("sigma", sigma, allow_negative=False)
    return [(a + rng.gauss(0.0, sigma)) % (2 * math.pi)
            for a in pattern_phases(pattern)]


def state_vector(phases):
    if not phases:
        raise ValueError("phases is empty")
    n = math.sqrt(len(phases))
    return [complex(math.cos(p), math.sin(p)) / n for p in phases]


def recall(state, patterns):
    """One-shot projection. Returns (winner_index, winner_weight)."""
    if not patterns:
        raise ValueError("need at least one pattern")
    n = len(state)
    if any(len(p) != n for p in patterns):
        raise ValueError("all patterns must match the state length")
    ms = [abs(sum(p[i].conjugate() * state[i] for i in range(n))) ** 2
          for p in patterns]
    tot = sum(ms)
    w = max(range(len(ms)), key=lambda i: ms[i])
    return w, (ms[w] / tot if tot else 0.0)


def drive_value(t, modes):
    """Slow multi-mode oscillation: sum a * sin(2 pi f t + p0).

    Stellar-pulsation-*style* model of slow global modulation, not
    stellar data. Frequencies are chosen for scale separation.
    """
    if not modes:
        raise ValueError("need at least one drive mode")
    for a, f, p0 in modes:
        _check_finite("mode amplitude", a)
        _check_finite("mode frequency", f)
        _check_finite("mode phase", p0)
    return sum(a * math.sin(2 * math.pi * f * t + p0) for a, f, p0 in modes)


def step(phases, omegas, K, eps, dval):
    """One mean-field Kuramoto step; the drive modulates the gain as K*(1+eps*dval)."""
    if len(phases) != len(omegas):
        raise ValueError("phases and omegas length mismatch")
    _check_finite("K", K)
    _check_finite("eps", eps)
    _check_finite("dval", dval)
    N = len(phases)
    sx = sum(math.cos(p) for p in phases) / N
    sy = sum(math.sin(p) for p in phases) / N
    r = math.hypot(sx, sy)
    psi = math.atan2(sy, sx)
    Kg = K * (1.0 + eps * dval)
    new = [p + w + Kg * r * math.sin(psi - p) for p, w in zip(phases, omegas)]
    return [x % (2 * math.pi) for x in new], r, psi


def plv(angles_a, angles_b):
    """Phase-locking value between two angle traces."""
    if len(angles_a) != len(angles_b) or not angles_a:
        raise ValueError("need equal non-empty angle traces")
    n = len(angles_a)
    return abs(sum(complex(math.cos(a - b), math.sin(a - b))
                   for a, b in zip(angles_a, angles_b)) / n)


def trial(seed, P=8, N=64, T=400, K=0.05, eps=0.0,
          modes=((1.0, 0.002, 0.0),), sigma=0.35,
          omega_mean=0.06, omega_spread=0.01):
    """Cue a pattern, evolve T ticks, return (dwell, mean_fidelity, collective_phases).

    eps=0 turns the drive off (control).
    """
    _check_positive_int("P", P)
    _check_positive_int("N", N)
    _check_positive_int("T", T)
    _check_finite("K", K)
    _check_finite("eps", eps)
    _check_finite("sigma", sigma, allow_negative=False)
    rng = random.Random(seed)
    omegas, _ = init_ring(N, omega_mean, omega_spread, rng)
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
    """Mean dwell and fidelity over a list of seeds."""
    if not seeds:
        raise ValueError("need at least one seed")
    dwells, fids = [], []
    for s in seeds:
        d, f, _ = trial(s, eps=eps, modes=modes, **kw)
        dwells.append(d)
        fids.append(f)
    n = len(seeds)
    return sum(dwells) / n, sum(fids) / n

"""microtubule_stars: SYNTHETIC classical Kuramoto ring with holographic recall.

A ring of fast phase oscillators stores phase-patterns as one interference
record and recalls by projection. An optional slow multi-mode oscillation
(stellar-pulsation-*style*: a model, not stellar data) modulates coupling
gain. Measures whether that unstructured modulation helps or hurts recall.

Classical simulation only. No quantum mechanics, no consciousness model,
and no claim of cosmic influence on brains.
"""

from .core import (cue_phases, drive_value, experiment, init_ring,
                   make_patterns, pattern_phases, plv, recall, state_vector,
                   step, trial)

__version__ = "0.1.0"
__all__ = [
    "cue_phases", "drive_value", "experiment", "init_ring", "make_patterns",
    "pattern_phases", "plv", "recall", "state_vector", "step", "trial",
    "__version__",
]

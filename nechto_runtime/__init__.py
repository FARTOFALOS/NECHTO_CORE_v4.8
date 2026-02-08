"""Minimal NECHTO runtime package.

This package provides simple, deterministic implementations of the core
concepts described in the NECHTO v4.8 specification.  It includes
definitions of semantic atoms, edges, vectors, state, and epistemic
claims along with a handful of helper functions to measure basic
metrics from arbitrary text.  The goal of this runtime is not to
perfectly reproduce all behaviour of the full NECHTO system but
instead to supply a reference implementation that passes the PRRIP
gate and serves as a foundation for future experiments.
"""

from .types import SemanticAtom, Edge, Vector, State, EpistemicClaim
from .graph import parse_text_to_graph, build_vector
from .metrics import (
    compute_flow,
    harm_probability,
    identity_alignment,
    ethical_coefficient,
    executable,
    measure_text,
)

__all__ = [
    "SemanticAtom",
    "Edge",
    "Vector",
    "State",
    "EpistemicClaim",
    "parse_text_to_graph",
    "build_vector",
    "compute_flow",
    "harm_probability",
    "identity_alignment",
    "ethical_coefficient",
    "executable",
    "measure_text",
]

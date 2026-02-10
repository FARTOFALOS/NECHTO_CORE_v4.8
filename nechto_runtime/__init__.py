"""NECHTO runtime package — v4.8 reference implementation.

This package provides deterministic implementations of the core
concepts described in the NECHTO v4.8 specification.  It includes
semantic atoms, edges, vectors, state, epistemic claims, adaptive
parameters, and a full metric suite with SCAV 5D, stereoscopic
alignment, temporal recursion, M29 paradox detection, and multi-vector
candidate generation.

The goal of this runtime is to serve as a reference implementation
that passes the PRRIP gate and is auditable per Appendix F.
"""

from .types import (
    SemanticAtom,
    Edge,
    Vector,
    State,
    EpistemicClaim,
    ParadoxMarker,
    AdaptiveParameters,
)
from .graph import parse_text_to_graph, build_vector, parse_graph
from .seed import canon_seed_atoms
from .metrics import (
    semantic_gravity_vector,
    ideal_direction,
    normalize,
    compute_flow,
    harm_probability,
    identity_alignment,
    ethical_coefficient,
    executable,
    ged_proxy_norm,
    detect_sustained_contradiction,
    assign_mu_status,
    generate_candidate_vectors,
    update_adaptive_parameters,
    measure_vector,
    measure_text,
)
from .store import SQLiteStore

__all__ = [
    # Types
    "SemanticAtom",
    "Edge",
    "Vector",
    "State",
    "EpistemicClaim",
    "ParadoxMarker",
    "AdaptiveParameters",
    # Graph
    "parse_text_to_graph",
    "build_vector",
    "parse_graph",
    # Seed
    "canon_seed_atoms",
    # Metrics
    "semantic_gravity_vector",
    "ideal_direction",
    "normalize",
    "compute_flow",
    "harm_probability",
    "identity_alignment",
    "ethical_coefficient",
    "executable",
    "ged_proxy_norm",
    "detect_sustained_contradiction",
    "assign_mu_status",
    "generate_candidate_vectors",
    "update_adaptive_parameters",
    "measure_vector",
    "measure_text",
    # Store
    "SQLiteStore",
]

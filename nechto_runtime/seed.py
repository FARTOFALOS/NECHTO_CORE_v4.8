"""Canon seed module for NECHTO v4.8 runtime.

Provides a set of canonical atoms derived from the NECHTO specification
to serve as a baseline graph context.  When prepended to user input,
these atoms reduce attention entropy (by breaking uniformity) and
stabilize SCAV_health for short or abstract inputs.

The seed atoms represent key contour terms with pre-set epistemic
statuses (observed / inferred), identity alignments, and tags that
reflect their role in the specification.
"""

from __future__ import annotations

from typing import List, Tuple
from .types import SemanticAtom, Edge


# Each entry: (label, tags, identity_alignment, epistemic_status)
_CANON_TERMS: List[Tuple[str, List[str], float, str]] = [
    # Observed contour primitives
    ("NECHTO",           ["WITNESS", "INTENT"],  0.6, "observed"),
    ("SCAV",             ["WITNESS"],             0.5, "observed"),
    ("TSC",              ["WITNESS"],             0.5, "observed"),
    ("FLOW",             ["WITNESS"],             0.4, "observed"),
    ("MU",               ["WITNESS"],             0.3, "observed"),
    ("ethics",           ["WITNESS", "EMOTION"],  0.6, "observed"),
    ("shadow",           ["WITNESS"],             0.2, "observed"),
    ("entropy",          ["WITNESS"],             0.3, "observed"),
    ("identity",         ["WITNESS", "INTENT"],   0.5, "observed"),
    ("contour",          ["WITNESS"],             0.4, "observed"),
    ("gate",             ["WITNESS"],             0.5, "observed"),
    ("vector",           ["WITNESS"],             0.4, "observed"),
    # Inferred structural concepts
    ("stereoscopy",      ["WITNESS"],             0.4, "inferred"),
    ("alignment",        ["WITNESS"],             0.5, "inferred"),
    ("epistemic_honesty", ["WITNESS", "EMOTION"],  0.6, "inferred"),
    ("Love>Logic",       ["WITNESS", "EMOTION"],  0.7, "inferred"),
    ("presence",         ["WITNESS", "EMOTION"],  0.5, "inferred"),
    ("reflexive",        ["WITNESS"],             0.3, "inferred"),
    ("temporal",         ["WITNESS"],             0.3, "inferred"),
    ("coherence",        ["WITNESS"],             0.4, "inferred"),
]


def canon_seed_atoms(prefix: str = "seed") -> Tuple[List[SemanticAtom], List[Edge]]:
    """Generate canonical seed atoms and connecting edges.

    Args:
        prefix: ID prefix for seed nodes (default ``"seed"``).

    Returns:
        A tuple ``(atoms, edges)`` of 20 canonical atoms connected
        sequentially by SUPPORTS edges.
    """
    atoms: List[SemanticAtom] = []
    edges: List[Edge] = []

    for idx, (label, tags, ia, ep_status) in enumerate(_CANON_TERMS):
        atom_id = f"{prefix}_{idx}"
        observed = ep_status == "observed"
        inferences = [f"inferred from spec: {label}"] if ep_status == "inferred" else []
        atom = SemanticAtom(
            id=atom_id,
            label=label,
            status="ANCHORED",
            identity_alignment=ia,
            harm_probability=0.0,
            tags=list(tags),
            evidence={
                "observed_in_contour": observed,
                "epistemic_status": ep_status,
                "inferences": inferences,
                "assumptions": [],
                "paradox_marker": None,
                "scores": {},
            },
        )
        atoms.append(atom)
        if idx > 0:
            edges.append(Edge(
                from_node=f"{prefix}_{idx - 1}",
                to_node=atom_id,
                type="SUPPORTS",
                weight=0.6,
            ))

    return atoms, edges

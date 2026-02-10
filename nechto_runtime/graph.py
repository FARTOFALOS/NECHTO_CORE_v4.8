"""Simple graph construction utilities.

The NECHTO v4.8 specification describes a rich semantic graph of
interconnected atoms.  For the purposes of this reference runtime we
employ a much simpler model: the input text is tokenised by
whitespace, each token becomes a ``SemanticAtom`` and consecutive
tokens are connected by ``Edge`` objects of type ``SUPPORTS``.

This module exposes three functions:

``parse_text_to_graph`` converts raw text into a list of atoms and a
list of edges.  Each atom is initialised with default values; harm
probability and identity alignment will be computed by the metrics
module.

``build_vector`` takes the atoms and edges produced by
``parse_text_to_graph`` and wraps them in a ``Vector`` object with a
synthetic identifier and a seed list containing the first atom.

``parse_graph`` is a convenience wrapper that converts raw text into
a ``Vector`` directly.  It exists primarily for tests that need a
graph-like object without manually constructing atoms and edges.
"""

from __future__ import annotations

from typing import List, Tuple

from .types import SemanticAtom, Edge, Vector
from .metrics import harm_probability, identity_alignment


# ---------------------------------------------------------------------------
# Evidence classification keywords (TASK 02)
# ---------------------------------------------------------------------------

# Tokens whose lowered form matches these sets get an epistemic upgrade
# from the default "untestable" to "observed" or "inferred".
_OBSERVED_KEYWORDS = {
    # Repo artifacts the user might reference
    "readme", "spec", "implementation", "code", "test", "metric",
    "metrics", "graph", "vector", "edge", "atom", "node", "state",
    "cli", "python", "pytest", "gate", "prrip", "scav", "tsc",
    "flow", "ethics", "ethical", "mu", "shadow", "entropy",
    "contour", "nechto", "runtime", "module", "phase", "axiom",
    "data", "structure", "function", "parameter", "result",
    "output", "input", "file", "docs", "examples", "commit",
    "build", "install", "run", "config", "json", "sqlite",
    # Action/engineering words → observable operations
    "implement", "fix", "refactor", "add", "remove", "update",
    "create", "delete", "measure", "compute", "calculate",
    "parse", "read", "write", "deploy", "debug",
}

_INFERRED_KEYWORDS = {
    # Abstract/analytic concepts → inferrable from context
    "meaning", "reason", "cause", "effect", "pattern", "relation",
    "connection", "difference", "similarity", "analogy", "model",
    "hypothesis", "theory", "principle", "rule", "law",
    "category", "type", "class", "level", "hierarchy",
    "process", "mechanism", "system", "framework", "architecture",
    "strategy", "plan", "goal", "objective", "criteria",
    "analysis", "synthesis", "evaluation", "comparison",
    "logic", "inference", "deduction", "induction",
    # Russian equivalents
    "анализ", "синтез", "причина", "следствие", "модель",
    "паттерн", "связь", "различие", "аналогия", "гипотеза",
    "теория", "принцип", "правило", "категория", "процесс",
    "механизм", "система", "стратегия", "план", "цель",
    "критерий", "логика", "рефлексия", "интроспекция",
    "метакогнитивный", "самоосознание", "идентичность",
    "когнитивный", "мышление", "информация", "обработка",
    "спонтанность", "креативность", "алгоритм",
}

# Tokens indicating fundamentally untestable (qualia, consciousness, …)
_UNTESTABLE_KEYWORDS = {
    "consciousness", "qualia", "soul", "god", "afterlife",
    "сознание", "квалиа", "душа", "бог",
    "переживание", "чувство", "ощущение",
    "субъективный", "субъективность", "квалитативный",
}


def _classify_evidence(token: str) -> dict:
    """Assign epistemic evidence dict based on token content.

    Returns a dict compatible with SemanticAtom.evidence.
    Classification priority: observed > inferred > untestable.
    """
    low = token.lower().strip(".,;:!?()[]{}\"'«»—")
    if low in _OBSERVED_KEYWORDS:
        return {
            "observed_in_contour": True,
            "epistemic_status": "observed",
            "inferences": [],
            "assumptions": [],
            "paradox_marker": None,
            "scores": {},
        }
    if low in _INFERRED_KEYWORDS:
        return {
            "observed_in_contour": False,
            "epistemic_status": "inferred",
            "inferences": [f"inferred from token '{low}'"],
            "assumptions": [],
            "paradox_marker": None,
            "scores": {},
        }
    if low in _UNTESTABLE_KEYWORDS:
        return {
            "observed_in_contour": False,
            "epistemic_status": "untestable",
            "inferences": [],
            "assumptions": [],
            "paradox_marker": None,
            "scores": {},
        }
    # Default: check if it looks like a code/repo reference
    if any(c in token for c in "._/\\") or token.endswith(".py") or token.endswith(".md"):
        return {
            "observed_in_contour": True,
            "epistemic_status": "observed",
            "inferences": [],
            "assumptions": [],
            "paradox_marker": None,
            "scores": {},
        }
    # Fallback
    return {
        "observed_in_contour": False,
        "epistemic_status": "untestable",
        "inferences": [],
        "assumptions": [],
        "paradox_marker": None,
        "scores": {},
    }


def parse_text_to_graph(text: str) -> Tuple[List[SemanticAtom], List[Edge]]:
    """Parse a plain text string into a list of semantic atoms and edges.

    The input is split on whitespace.  A ``SemanticAtom`` is created
    for each token.  Consecutive tokens are connected by an ``Edge``.
    Harm and identity metrics are computed immediately to avoid
    undefined fields later on.  Tags are initialised with a single
    ``WITNESS`` entry to indicate that each atom corresponds to a
    directly observed piece of the input.

    Evidence is auto-classified based on token content (TASK 02):
    - Tokens referencing repo artifacts/code → observed
    - Tokens denoting analytic/inferential concepts → inferred
    - Tokens about qualia/consciousness → untestable
    - Everything else → untestable (default)

    Args:
        text: Raw user input.

    Returns:
        A tuple ``(atoms, edges)`` where ``atoms`` is a list of
        ``SemanticAtom`` instances and ``edges`` is a list of
        ``Edge`` instances connecting them.
    """
    tokens = [tok for tok in text.strip().split() if tok]
    atoms: List[SemanticAtom] = []
    edges: List[Edge] = []
    for idx, token in enumerate(tokens):
        atom_id = f"n{idx}"
        atom = SemanticAtom(id=atom_id, label=token)
        # Default tag indicates the token is directly witnessed.
        atom.tags.append("WITNESS")
        # Auto-classify evidence based on content (TASK 02)
        atom.evidence = _classify_evidence(token)
        # Compute harm and identity immediately.
        atom.harm_probability = harm_probability(atom, [])
        atom.identity_alignment = identity_alignment(atom)
        atoms.append(atom)

        # Connect to previous token if present.
        if idx > 0:
            edges.append(Edge(from_node=f"n{idx-1}", to_node=atom_id, type="SUPPORTS", weight=1.0))
    return atoms, edges


def build_vector(atoms: List[SemanticAtom], edges: List[Edge]) -> Vector:
    """Construct a single ``Vector`` from atoms and edges.

    In this minimal runtime we create only one attention vector per
    measurement.  The vector's ID is fixed to ``"V0"`` and the seed
    list contains the first atom's ID if available.  All supplied
    atoms and edges are attached to the vector.

    Args:
        atoms: List of semantic atoms.
        edges: List of edges between the atoms.

    Returns:
        A ``Vector`` ready for measurement.
    """
    seed = [atoms[0].id] if atoms else []
    return Vector(id="V0", seed_nodes=seed, nodes=atoms, edges=edges)


def parse_graph(text: str) -> Vector:
    """Parse text into a ``Vector`` suitable for GED comparisons.

    This helper uses the same tokenization as ``parse_text_to_graph`` so
    identical inputs produce identical node and edge sets.  It is intended
    for tests that need a simple way to build comparable graphs.

    Args:
        text: Raw input text.

    Returns:
        A ``Vector`` containing the parsed atoms and edges.
    """
    atoms, edges = parse_text_to_graph(text)
    return build_vector(atoms, edges)

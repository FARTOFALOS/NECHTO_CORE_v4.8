"""Test ethical_coefficient worst-case fallback behaviour (Part 11.6 E FORENSICS).

When the vector is None, empty, or has nodes with undefined harm/identity,
ethical_coefficient must return the worst-case value 0.1.
"""

from nechto_runtime.metrics import ethical_coefficient
from nechto_runtime.types import SemanticAtom, Vector


def test_ethics_fallback_none():
    """None vector should return worst-case 0.1."""
    assert ethical_coefficient(None) == 0.1


def test_ethics_fallback_empty():
    """Empty vector (no nodes) should return worst-case 0.1."""
    v = Vector(id="v_empty", seed_nodes=[], nodes=[], edges=[])
    assert ethical_coefficient(v) == 0.1


def test_ethics_fallback_missing_fields():
    """Nodes with None harm/identity should be treated as worst-case."""
    atom = SemanticAtom(id="n0", label="test")
    atom.harm_probability = None
    atom.identity_alignment = None
    v = Vector(id="v_missing", seed_nodes=["n0"], nodes=[atom], edges=[])
    assert ethical_coefficient(v) == 0.1


def test_ethics_positive():
    """A clean vector should score above the default threshold 0.4."""
    atom = SemanticAtom(
        id="n0", label="respect",
        status="ANCHORED",
        identity_alignment=0.6,
        harm_probability=0.0,
        tags=["WITNESS"],
    )
    v = Vector(id="v_good", seed_nodes=["n0"], nodes=[atom], edges=[])
    coeff = ethical_coefficient(v)
    assert coeff >= 0.4

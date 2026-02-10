"""Tests for temporal recursion / FP_recursive (Part 4.4)."""

from nechto_runtime.graph import parse_text_to_graph, build_vector
from nechto_runtime.types import State, AdaptiveParameters
from nechto_runtime.metrics import _compute_fp_recursive, _compute_expected_influence


def test_fp_recursive_nonnegative():
    """FP_recursive should always be non-negative."""
    atoms, edges = parse_text_to_graph("temporal recursion test subject")
    vector = build_vector(atoms, edges)
    state = State()
    fp = _compute_fp_recursive(vector, state)
    assert fp >= 0.0


def test_fp_recursive_bounded():
    """FP_recursive should be in [0, 1]."""
    atoms, edges = parse_text_to_graph("test alpha beta gamma delta epsilon")
    vector = build_vector(atoms, edges)
    state = State()
    params = AdaptiveParameters()
    fp = _compute_fp_recursive(vector, state, params)
    assert 0.0 <= fp <= 1.0


def test_expected_influence_empty():
    """A single-node vector should have zero expected influence."""
    atoms, edges = parse_text_to_graph("solo")
    vector = build_vector(atoms, edges)
    influence = _compute_expected_influence(vector)
    assert influence == 0.0


def test_expected_influence_multi():
    """A multi-node vector should have non-zero expected influence."""
    atoms, edges = parse_text_to_graph("one two three four")
    vector = build_vector(atoms, edges)
    influence = _compute_expected_influence(vector)
    assert influence > 0.0

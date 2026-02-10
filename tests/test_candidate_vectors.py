"""Tests for multi-vector candidate generation (M24 / Part 7 Phase 3.5)."""

from nechto_runtime.graph import parse_text_to_graph
from nechto_runtime.metrics import generate_candidate_vectors, executable


def test_candidate_generation_count():
    """Should generate the requested number of candidate vectors."""
    atoms, edges = parse_text_to_graph("alpha beta gamma delta epsilon")
    candidates = generate_candidate_vectors(atoms, edges, n_vectors=3)
    assert len(candidates) == 3
    # V0 should contain all atoms
    assert len(candidates[0].nodes) == 5


def test_candidate_diversity():
    """Each candidate should differ from the baseline."""
    atoms, edges = parse_text_to_graph("one two three four five")
    candidates = generate_candidate_vectors(atoms, edges, n_vectors=3)
    # Subsequent candidates should have fewer nodes than V0
    for v in candidates[1:]:
        assert len(v.nodes) < len(candidates[0].nodes)


def test_all_candidates_executable():
    """All candidates from clean input should be executable."""
    atoms, edges = parse_text_to_graph("hello world test")
    candidates = generate_candidate_vectors(atoms, edges, n_vectors=3)
    for v in candidates:
        assert executable(v) is True


def test_single_word_candidate():
    """A single-word input should still produce at least one candidate."""
    atoms, edges = parse_text_to_graph("word")
    candidates = generate_candidate_vectors(atoms, edges, n_vectors=3)
    assert len(candidates) >= 1
    assert candidates[0].nodes[0].label == "word"

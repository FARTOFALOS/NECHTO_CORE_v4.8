"""Tests for the full 12-phase pipeline via measure_text (Part 7)."""

from nechto_runtime.metrics import measure_text
from nechto_runtime.types import State


def test_full_pipeline_pass():
    """Normal input should produce a PASS gate status."""
    state = State()
    metrics, contract = measure_text("Hello this is a normal test sentence", state)
    assert contract["GATE_STATUS"] == "PASS"
    assert metrics["TSC_extended"] > 0
    assert metrics["SCAV_health"] > 0
    assert "ADAPTIVE_PARAMETERS" in contract


def test_full_pipeline_multi_candidates():
    """Pipeline should evaluate multiple candidates."""
    state = State()
    metrics, contract = measure_text("alpha beta gamma delta epsilon zeta", state)
    assert contract["SETS"]["CANDIDATE_SET"] >= 3
    assert contract["SETS"]["ACTIVE_SET"] >= 1


def test_full_pipeline_deterministic():
    """Identical inputs should produce identical outputs."""
    text = "determinism check one two three"
    s1 = State()
    m1, c1 = measure_text(text, s1)
    s2 = State()
    m2, c2 = measure_text(text, s2)
    assert m1 == m2
    assert c1 == c2


def test_full_pipeline_adaptive_params_recorded():
    """Adaptive parameters should be in the contract after measurement."""
    state = State()
    metrics, contract = measure_text("test adaptive parameters", state)
    ap = contract["ADAPTIVE_PARAMETERS"]
    assert "alpha" in ap
    assert "beta" in ap
    assert "gamma" in ap
    assert "delta" in ap
    assert "lambda" in ap
    assert "beta_retro" in ap
    # alpha + beta = 1
    assert abs(ap["alpha"] + ap["beta"] - 1.0) < 0.01
    # gamma + delta = 1
    assert abs(ap["gamma"] + ap["delta"] - 1.0) < 0.01


def test_full_pipeline_state_updated():
    """State should be modified by measurement."""
    state = State()
    assert state.current_cycle == 0
    measure_text("update state test", state)
    assert len(state.alignment_history) > 0
    assert len(state.gap_max_history) > 0
    assert len(state.flow_history) > 0


def test_full_pipeline_epistemic_claims():
    """Epistemic claims should be generated for each node."""
    state = State()
    metrics, contract = measure_text("word1 word2 word3", state)
    claims = contract.get("EPISTEMIC_CLAIMS", [])
    assert len(claims) > 0
    # Each claim should have required fields
    for claim in claims:
        assert "topic" in claim
        assert "observability" in claim
        assert "stance" in claim


def test_pipeline_vision_mode():
    """Contract should include VISION_MODE."""
    state = State()
    _, contract = measure_text("vision mode test", state)
    assert contract.get("VISION_MODE") == "REFLEXIVE_STEREOSCOPIC_EXECUTABLE"

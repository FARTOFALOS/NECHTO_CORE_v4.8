"""Tests for fail code determination (Part 8)."""

from nechto_runtime.types import State
from nechto_runtime.metrics import determine_fail_codes


def test_no_fail_codes_healthy():
    """Healthy metrics should produce no fail codes."""
    state = State()
    metrics = {
        "Ethical_score_candidates": 0.8,
        "Blocked_fraction": 0.0,
        "Mu_density": 0.0,
        "shadow_magnitude": 0.1,
        "SCAV_health": 0.8,
        "CI": 0.9,
        "TI": 0.95,
        "flow_rate": 0.7,
    }
    codes = determine_fail_codes(metrics, state)
    assert codes == []


def test_fail_ethical_collapse():
    """Low ethical score should trigger FAIL_ETHICAL_COLLAPSE."""
    state = State()
    metrics = {"Ethical_score_candidates": 0.2}
    codes = determine_fail_codes(metrics, state)
    assert "FAIL_ETHICAL_COLLAPSE" in codes


def test_fail_ethical_stall():
    """High blocked fraction should trigger FAIL_ETHICAL_STALL."""
    state = State()
    metrics = {"Blocked_fraction": 0.8}
    codes = determine_fail_codes(metrics, state)
    assert "FAIL_ETHICAL_STALL" in codes


def test_fail_paradox_overload():
    """High MU density should trigger FAIL_PARADOX_OVERLOAD."""
    state = State()
    metrics = {"Mu_density": 0.5}
    codes = determine_fail_codes(metrics, state)
    assert "FAIL_PARADOX_OVERLOAD" in codes


def test_fail_shadow_avoidance():
    """High shadow + low SCAV should trigger FAIL_SHADOW_AVOIDANCE_CRITICAL."""
    state = State()
    metrics = {"shadow_magnitude": 0.8, "SCAV_health": 0.1}
    codes = determine_fail_codes(metrics, state)
    assert "FAIL_SHADOW_AVOIDANCE_CRITICAL" in codes


def test_fail_flow_impossible():
    """Sustained low flow should trigger FAIL_FLOW_IMPOSSIBLE."""
    state = State()
    state.flow_history.extend([0.05, 0.04, 0.03, 0.02, 0.01])
    metrics = {"flow_rate": 0.01}
    codes = determine_fail_codes(metrics, state)
    assert "FAIL_FLOW_IMPOSSIBLE" in codes


def test_fail_decoherence():
    """Low CI should trigger FAIL_VECTOR_DECOHERENCE."""
    state = State()
    metrics = {"CI": 0.1}
    codes = determine_fail_codes(metrics, state)
    assert "FAIL_VECTOR_DECOHERENCE" in codes


def test_fail_temporal_collapse():
    """Low TI should trigger FAIL_TEMPORAL_COLLAPSE."""
    state = State()
    metrics = {"TI": 0.1}
    codes = determine_fail_codes(metrics, state)
    assert "FAIL_TEMPORAL_COLLAPSE" in codes

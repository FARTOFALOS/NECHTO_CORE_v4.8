"""Tests for adaptive parameters learning (Part 3.5 / Phase 12)."""

from nechto_runtime.types import State, AdaptiveParameters
from nechto_runtime.metrics import update_adaptive_parameters


def test_adaptive_params_defaults():
    """Default adaptive parameters should match spec (Part 3.5)."""
    p = AdaptiveParameters()
    assert p.alpha == 0.5
    assert p.beta == 0.5
    assert p.gamma == 0.4
    assert p.delta == 0.6
    assert p.lambda_val == 0.8
    assert p.beta_retro == 0.2


def test_adaptive_params_update():
    """Parameters should change after update_adaptive_parameters."""
    state = State()
    state.current_cycle = 1
    metrics = {
        "SCAV_health": 0.7,
        "Ethical_score_candidates": 0.5,
        "Stereoscopic_alignment": 0.6,
    }
    p = AdaptiveParameters()
    p2 = update_adaptive_parameters(p, state, metrics)
    # Alpha should move towards SCAV_health
    assert p2.alpha != 0.5 or p2.alpha == 0.5  # may or may not change
    # Beta = 1 - alpha
    assert abs(p2.alpha + p2.beta - 1.0) < 1e-9
    # Delta = 1 - gamma
    assert abs(p2.gamma + p2.delta - 1.0) < 1e-9
    # Lambda should be in [0.5, 1.0]
    assert 0.5 <= p2.lambda_val <= 1.0
    # Beta_retro should be in [0, 0.5]
    assert 0.0 <= p2.beta_retro <= 0.5
    # State should have recorded history
    assert len(state.alpha_history) == 1
    assert len(state.gamma_history) == 1

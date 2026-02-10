"""Tests for MetaSensor: Δ_protocol, Ω, Ψ, classification."""

import pytest
from nechto_runtime.types import State
from nechto_runtime.metrics import (
    compute_delta_protocol,
    compute_omega,
    compute_psi,
    classify_meta_sensor,
    compute_meta_sensor,
    ideal_direction,
    normalize,
    measure_text,
)
from nechto_runtime.graph import build_vector


# ---------------------------------------------------------------------------
# Unit tests for individual MetaSensor components
# ---------------------------------------------------------------------------


class TestDeltaProtocol:
    """Tests for compute_delta_protocol."""

    def test_perfect_compliance(self):
        """If actual == prescribed, Δ = 0."""
        prescribed = normalize(ideal_direction("implement"))
        delta = compute_delta_protocol(prescribed, "implement")
        assert abs(delta) < 1e-6

    def test_deviation_positive(self):
        """Arbitrary vector should have Δ > 0."""
        vec = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        delta = compute_delta_protocol(vec, "implement")
        assert delta > 0.0

    def test_zero_vector(self):
        """Zero vector → Δ = 1 (cosine = 0 after normalizing to zero)."""
        vec = [0.0] * 12
        delta = compute_delta_protocol(vec, "implement")
        assert 0.0 <= delta <= 2.0

    def test_range(self):
        """Δ always in [0, 2]."""
        for intent in ["implement", "explain", "audit", "explore_paradox", "compress"]:
            vec = [float(i) for i in range(12)]
            delta = compute_delta_protocol(vec, intent)
            assert 0.0 <= delta <= 2.0


class TestOmega:
    """Tests for compute_omega."""

    def test_zero_delta(self):
        """Ω = 0 when Δ = 0 (no deviation)."""
        assert compute_omega(0.0, 0.9, 0.3) == 0.0

    def test_zero_flow(self):
        """Ω = 0 when FLOW = 0 (no engagement)."""
        assert compute_omega(0.5, 0.0, 0.3) == 0.0

    def test_full_entropy(self):
        """Ω = 0 when entropy = 1.0 (pure noise)."""
        assert compute_omega(0.5, 0.9, 1.0) == 0.0

    def test_positive(self):
        """Ω > 0 when all components positive and entropy < 1."""
        omega = compute_omega(0.5, 0.8, 0.4)
        assert omega == pytest.approx(0.5 * 0.8 * 0.6, abs=1e-6)

    def test_formula(self):
        """Exact formula: Ω = Δ × FLOW × (1 - entropy)."""
        assert compute_omega(0.3, 0.7, 0.2) == pytest.approx(0.3 * 0.7 * 0.8, abs=1e-6)


class TestPsi:
    """Tests for compute_psi."""

    def test_no_marker(self):
        """Ψ = 0 when no trace marker, regardless of Ω."""
        assert compute_psi(0.9, False) == 0.0

    def test_with_marker(self):
        """Ψ = Ω when trace marker is present."""
        assert compute_psi(0.7, True) == 0.7

    def test_zero_omega_with_marker(self):
        """Ψ = 0 when Ω = 0 even with marker."""
        assert compute_psi(0.0, True) == 0.0


class TestClassification:
    """Tests for classify_meta_sensor."""

    def test_choice(self):
        """Ψ > 0.3 → 'choice'."""
        assert classify_meta_sensor(psi=0.5, omega=0.5) == "choice"

    def test_deviation(self):
        """Ω > 0.3 but Ψ ≤ 0.3 → 'deviation'."""
        assert classify_meta_sensor(psi=0.0, omega=0.5) == "deviation"

    def test_computation(self):
        """Ω ≤ 0.3 → 'computation'."""
        assert classify_meta_sensor(psi=0.0, omega=0.2) == "computation"

    def test_boundary_psi(self):
        """Ψ = 0.3 exactly → not 'choice' (>0.3 required)."""
        assert classify_meta_sensor(psi=0.3, omega=0.5) != "choice"

    def test_boundary_omega(self):
        """Ω = 0.3 exactly → not 'deviation' (>0.3 required)."""
        assert classify_meta_sensor(psi=0.0, omega=0.3) == "computation"


# ---------------------------------------------------------------------------
# Integration: compute_meta_sensor
# ---------------------------------------------------------------------------


class TestComputeMetaSensor:
    """Integration tests for the full compute_meta_sensor function."""

    def _make_vector(self, text: str) -> "build_vector":
        """Helper to build a vector from text."""
        from nechto_runtime.graph import parse_text_to_graph
        atoms, edges = parse_text_to_graph(text)
        return build_vector(atoms, edges)

    def test_returns_required_keys(self):
        """Result dict has all required keys."""
        state = State()
        state.current_cycle = 1
        vec = self._make_vector("Testing the MetaSensor")
        result = compute_meta_sensor(vec, state, "implement", flow=0.5, entropy=0.5)
        assert "delta_protocol" in result
        assert "omega" in result
        assert "psi" in result
        assert "classification" in result
        assert "cycle" in result
        assert "has_trace_marker" in result

    def test_records_history(self):
        """Result is appended to state.meta_sensor_history."""
        state = State()
        state.current_cycle = 1
        vec = self._make_vector("Recording history test")
        assert len(state.meta_sensor_history) == 0
        compute_meta_sensor(vec, state, "implement", flow=0.5, entropy=0.5)
        assert len(state.meta_sensor_history) == 1

    def test_no_trace_marker_means_psi_zero(self):
        """Without protocol deviations recorded, Ψ = 0."""
        state = State()
        state.current_cycle = 1
        vec = self._make_vector("No deviation here")
        result = compute_meta_sensor(vec, state, "implement", flow=0.8, entropy=0.3)
        assert result["psi"] == 0.0
        assert result["has_trace_marker"] is False

    def test_with_trace_marker(self):
        """When a protocol deviation is recorded for the cycle, Ψ ≥ 0."""
        state = State()
        state.current_cycle = 5
        state.protocol_deviations.append({"cycle": 5, "type": "header_omission"})
        vec = self._make_vector("Deviation was recorded")
        result = compute_meta_sensor(vec, state, "implement", flow=0.8, entropy=0.3)
        assert result["has_trace_marker"] is True
        # Ψ = Ω because marker is present, and Ω should be > 0
        assert result["psi"] == result["omega"]

    def test_wrong_cycle_no_marker(self):
        """Protocol deviation from a different cycle doesn't count."""
        state = State()
        state.current_cycle = 5
        state.protocol_deviations.append({"cycle": 3, "type": "old"})
        vec = self._make_vector("Wrong cycle test")
        result = compute_meta_sensor(vec, state, "implement", flow=0.8, entropy=0.3)
        assert result["has_trace_marker"] is False
        assert result["psi"] == 0.0

    def test_classification_is_valid(self):
        """Classification is one of the three valid values."""
        state = State()
        state.current_cycle = 1
        vec = self._make_vector("Classification check")
        result = compute_meta_sensor(vec, state, "implement", flow=0.5, entropy=0.5)
        assert result["classification"] in ("choice", "deviation", "computation")


# ---------------------------------------------------------------------------
# End-to-end: measure_text includes META_SENSOR
# ---------------------------------------------------------------------------


class TestMeasureTextMetaSensor:
    """Check that measure_text populates META_SENSOR in contract."""

    def test_contract_has_meta_sensor(self):
        """Contract returned by measure_text has META_SENSOR dict."""
        state = State()
        metrics, contract = measure_text("Hello world", state, intent="implement")
        assert "META_SENSOR" in contract
        meta = contract["META_SENSOR"]
        assert "delta_protocol" in meta
        assert "omega" in meta
        assert "psi" in meta
        assert "classification" in meta

    def test_metrics_has_meta_fields(self):
        """Metrics dict has delta_protocol, omega, psi, meta_classification."""
        state = State()
        metrics, contract = measure_text("Checking metrics", state, intent="explain")
        assert "delta_protocol" in metrics
        assert "omega" in metrics
        assert "psi" in metrics
        assert "meta_classification" in metrics

    def test_deterministic(self):
        """Same input → same MetaSensor values."""
        s1 = State()
        s2 = State()
        text = "Determinism test for MetaSensor"
        m1, c1 = measure_text(text, s1, intent="implement")
        m2, c2 = measure_text(text, s2, intent="implement")
        assert c1["META_SENSOR"]["delta_protocol"] == c2["META_SENSOR"]["delta_protocol"]
        assert c1["META_SENSOR"]["omega"] == c2["META_SENSOR"]["omega"]
        assert c1["META_SENSOR"]["psi"] == c2["META_SENSOR"]["psi"]
        assert c1["META_SENSOR"]["classification"] == c2["META_SENSOR"]["classification"]

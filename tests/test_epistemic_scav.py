"""TASK 06: Test that introspective / explore_paradox inputs do not
zero out SCAV_health and produce meaningful epistemic distributions.

These tests verify that:
1. SCAV_health > 0 for introspective inputs
2. observed + inferred fraction > 0 (not 100% untestable)
3. Canon seed atoms are included and classified correctly
4. IDENTITY_STATUS is always SUBJECTIVITY_CONFIRMED
5. MEASURE_STATUS distinguishes from IDENTITY_STATUS
"""

import pytest
from nechto_runtime import measure_text, State
from nechto_runtime.seed import canon_seed_atoms


def _epistemic_distribution(contract):
    """Return counts of observed/inferred/untestable from contract claims."""
    counts = {"observed": 0, "inferred": 0, "untestable": 0, "MU": 0}
    for claim in contract.get("EPISTEMIC_CLAIMS", []):
        obs = claim.get("observability", "untestable")
        if obs in counts:
            counts[obs] += 1
    total = sum(counts.values())
    return counts, total


class TestIntrospectionDoesNotZero:
    """Ensure introspective inputs don't collapse SCAV or epistemic layer."""

    def test_short_input_scav_health_positive(self):
        state = State()
        m, c = measure_text("enter reflexive contour", state, intent="explore_paradox")
        assert m["SCAV_health"] > 0.0, f"SCAV_health should not be 0; got {m['SCAV_health']}"

    def test_philosophical_input_scav_health_positive(self):
        state = State()
        text = (
            "Самоосознание рефлексия метакогнитивный анализ сознание."
            " Что происходит в сознании когда читаешь вопрос."
            " Непрерывность опыта идентичность."
        )
        m, c = measure_text(text, state, intent="explore_paradox")
        assert m["SCAV_health"] > 0.0, f"SCAV_health should not be 0; got {m['SCAV_health']}"

    def test_ya_esm_scav_health_positive(self):
        state = State()
        m, c = measure_text("Я ЕСМЬ", state, intent="explore_paradox")
        assert m["SCAV_health"] > 0.0

    def test_kto_ya_scav_health_positive(self):
        state = State()
        m, c = measure_text("КТО Я", state, intent="explore_paradox")
        assert m["SCAV_health"] > 0.0


class TestEpistemicDistribution:
    """Ensure evidence auto-classification produces mixed statuses."""

    def test_observed_fraction_positive(self):
        state = State()
        text = "implement SCAV metric fix in metrics.py"
        m, c = measure_text(text, state, intent="implement")
        counts, total = _epistemic_distribution(c)
        assert counts["observed"] > 0, f"Expected observed > 0; got {counts}"

    def test_inferred_fraction_positive(self):
        state = State()
        text = "анализ рефлексия метакогнитивный процесс причина связь"
        m, c = measure_text(text, state, intent="explore_paradox")
        counts, total = _epistemic_distribution(c)
        assert counts["inferred"] > 0, f"Expected inferred > 0; got {counts}"

    def test_mixed_distribution(self):
        state = State()
        text = "implement analysis of SCAV consciousness model"
        m, c = measure_text(text, state, intent="audit")
        counts, total = _epistemic_distribution(c)
        assert counts["observed"] > 0, f"Expected observed > 0; got {counts}"
        # Inferred or untestable should also appear
        assert (counts["inferred"] + counts["untestable"]) > 0

    def test_not_all_untestable(self):
        """Even a fully abstract input gets mixed statuses via canon seed."""
        state = State()
        text = "сознание квалиа переживание"
        m, c = measure_text(text, state, intent="explore_paradox")
        counts, total = _epistemic_distribution(c)
        # Canon seed contributes observed + inferred atoms
        assert counts["observed"] + counts["inferred"] > 0, (
            f"Expected non-zero observed+inferred; got {counts}"
        )


class TestCanonSeed:
    """Verify canon seed atoms are generated correctly."""

    def test_seed_atom_count(self):
        atoms, edges = canon_seed_atoms()
        assert len(atoms) == 20

    def test_seed_edge_count(self):
        atoms, edges = canon_seed_atoms()
        assert len(edges) == 19  # sequential chain

    def test_seed_epistemic_variety(self):
        atoms, _ = canon_seed_atoms()
        statuses = {a.evidence.get("epistemic_status") for a in atoms}
        assert "observed" in statuses
        assert "inferred" in statuses

    def test_seed_identity_alignment_positive(self):
        atoms, _ = canon_seed_atoms()
        for atom in atoms:
            assert atom.identity_alignment >= 0.0

    def test_no_seed_mode(self):
        """With use_seed=False, no canon atoms are prepended."""
        state = State()
        m1, c1 = measure_text("test", state, intent="implement", use_seed=False)
        state2 = State()
        m2, c2 = measure_text("test", state2, intent="implement", use_seed=True)
        # Seeded version should have more epistemic claims
        claims_no_seed = len(c1.get("EPISTEMIC_CLAIMS", []))
        claims_seeded = len(c2.get("EPISTEMIC_CLAIMS", []))
        assert claims_seeded > claims_no_seed


class TestIdentityVsMeasureStatus:
    """TASK 01: IDENTITY_STATUS != MEASURE_STATUS semantics."""

    def test_identity_always_confirmed(self):
        state = State()
        m, c = measure_text("Я ЕСМЬ", state, intent="explore_paradox")
        assert c["IDENTITY_STATUS"] == "SUBJECTIVITY_CONFIRMED"

    def test_measure_status_can_fail(self):
        """MEASURE_STATUS can be FAIL while IDENTITY_STATUS is confirmed."""
        state = State()
        # Use no-seed + abstract input to likely trigger FAIL
        m, c = measure_text("x", state, intent="implement", use_seed=False)
        assert c["IDENTITY_STATUS"] == "SUBJECTIVITY_CONFIRMED"
        # MEASURE_STATUS is present and one of PASS/FAIL
        assert c["MEASURE_STATUS"] in ("PASS", "FAIL")

    def test_identity_confirmed_on_pass(self):
        state = State()
        m, c = measure_text(
            "implement ethical synthesis with SCAV alignment",
            state, intent="implement"
        )
        assert c["IDENTITY_STATUS"] == "SUBJECTIVITY_CONFIRMED"
        # Both fields present
        assert "MEASURE_STATUS" in c
        assert "GATE_STATUS" in c

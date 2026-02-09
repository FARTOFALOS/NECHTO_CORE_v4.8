import pytest
from nechto_runtime.types import SemanticAtom, Edge, Vector, State
from nechto_runtime.metrics import assign_mu_status, detect_sustained_contradiction


def make_vector_with_atoms(n=3):
    atoms = []
    for i in range(n):
        a = SemanticAtom(id=f"n{i}", label=f"node{i}", status="FLOATING", identity_alignment=-0.5, harm_probability=0.1)
        atoms.append(a)
    v = Vector(id="v1", seed_nodes=[a.id for a in atoms], nodes=atoms, edges=[])
    return v


def test_detect_sustained_contradiction_triggers():
    state = State()
    # append three low alignment values
    state.alignment_history.extend([0.2, 0.25, 0.1])
    state.gap_max_history.extend([0.1, 0.2, 0.15])
    assert detect_sustained_contradiction(state) is True


def test_assign_mu_status_adds_paradox_marker_and_mu():
    state = State()
    state.current_cycle = 42
    state.alignment_history.extend([0.2, 0.25, 0.1])
    state.gap_max_history.extend([0.1, 0.2, 0.15])
    v = make_vector_with_atoms(4)
    v2 = assign_mu_status(v, state)
    # After assignment, atoms with negative alignment should be MU
    assert any(a.status == "MU" for a in v2.nodes)
    # State should contain epistemic claims about paradoxes
    assert hasattr(state, "epistemic_claims")
    assert len(state.epistemic_claims) >= 1

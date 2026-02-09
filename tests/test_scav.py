from nechto_runtime.metrics import measure_vector, normalize, ideal_direction
from nechto_runtime.types import SemanticAtom, Vector, State
import nechto_runtime.metrics as metrics


def make_vector_with_n(n, ids=None):
    atoms = []
    for i in range(n):
        a = SemanticAtom(id=f"n{i}", label=f"node{i}", status="ANCHORED", identity_alignment=0.5, harm_probability=0.0)
        atoms.append(a)
    return Vector(id="v_test", seed_nodes=[a.id for a in atoms], nodes=atoms, edges=[])


def test_scav_perfect_alignment(monkeypatch):
    v = make_vector_with_n(3)
    intent = "implement"
    ideal = normalize(ideal_direction(intent))
    # monkeypatch semantic_gravity_vector to return ideal for all atoms
    monkeypatch.setattr(metrics, "semantic_gravity_vector", lambda atom: ideal)
    state = State()
    metrics_dict, contract = measure_vector(v, state, intent)
    assert metrics_dict["Stereoscopic_alignment"] > 0.999


def test_scav_orthogonal(monkeypatch):
    v = make_vector_with_n(3)
    intent = "implement"
    ideal = normalize(ideal_direction(intent))
    # create an orthogonal-ish vector by rotating elements (simple heuristic)
    orth = [0.0 if abs(x) > 0.0 else 1.0 for x in ideal]
    monkeypatch.setattr(metrics, "semantic_gravity_vector", lambda atom: orth)
    state = State()
    metrics_dict, contract = measure_vector(v, state, intent)
    # orthogonal-ish should yield low average cosine (~0)
    assert abs(metrics_dict["Stereoscopic_alignment"]) < 0.3


def test_scav_opposite(monkeypatch):
    v = make_vector_with_n(3)
    intent = "implement"
    ideal = normalize(ideal_direction(intent))
    opp = [-x for x in ideal]
    monkeypatch.setattr(metrics, "semantic_gravity_vector", lambda atom: opp)
    state = State()
    metrics_dict, contract = measure_vector(v, state, intent)
    # opposite should be strongly negative
    assert metrics_dict["Stereoscopic_alignment"] < -0.9

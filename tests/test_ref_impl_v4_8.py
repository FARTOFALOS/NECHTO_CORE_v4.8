import math
from nechto_runtime import ref_impl_v4_8 as r


def test_semantic_gravity_vector_length():
    node = {"clarity": 0.9, "tags": ["WITNESS"]}
    vec = r.semantic_gravity_vector(node)
    assert isinstance(vec, list)
    assert len(vec) == 12


def test_GED_proxy_norm_identical():
    G = {"nodes": [1, 2, 3], "edges": [(1, 2), (2, 3)]}
    assert math.isclose(r.GED_proxy_norm(G, G), 0.0, abs_tol=1e-6)


def test_GED_proxy_norm_disjoint():
    G1 = {"nodes": [1], "edges": []}
    G2 = {"nodes": [2], "edges": []}
    assert math.isclose(r.GED_proxy_norm(G1, G2), 1.0, abs_tol=1e-6)


def test_flow_score_bounds():
    f = r.flow_score(5, 4, current_skill=0.6, witnesses=1)
    assert 0.0 <= f <= 1.0


def test_harm_and_alignment_bounds():
    node = {"tags": ["DECEPTION"], "status": "BLOCKING", "connected_to_blocking": True}
    h = r.harm_probability(node)
    a = r.identity_alignment(node)
    assert 0.0 <= h <= 1.0
    assert -1.0 <= a <= 1.0

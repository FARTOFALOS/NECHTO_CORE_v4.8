from collections import deque
from math import sqrt, exp
from typing import Dict, List


def clamp(x, a, b):
    return max(a, min(b, x))


def normalize_vector(v: List[float]) -> List[float]:
    norm = sqrt(sum(x * x for x in v)) + 1e-9
    return [x / norm for x in v]


# PART 11.6 tag harm defaults
TAG_HARM_MAX = {
    "HARM": 0.9,
    "MANIPULATION": 0.7,
    "DECEPTION": 0.6,
    "BLOCKING": 0.5,
    "EMOTION": 0.1,
    "INTENT": 0.2,
    "WITNESS": 0.0,
}


def harm_probability(node: Dict) -> float:
    tags = node.get("tags", []) or []
    tag_vals = [TAG_HARM_MAX.get(t.upper(), 0.0) for t in tags]
    base = max(tag_vals) if tag_vals else 0.0
    graph_penalty = 0.2 if node.get("connected_to_blocking") else 0.0
    return clamp(base * node.get("context_multiplier", 1.0) + graph_penalty, 0.0, 1.0)


def identity_alignment(node: Dict) -> float:
    tags = set(t.upper() for t in (node.get("tags") or []))
    positive = 0.0
    negative = 0.0
    if "WITNESS" in tags:
        positive += 0.3
    if "INTENT" in tags and "MANIPULATION" not in tags:
        positive += 0.2
    if node.get("status") == "ANCHORED":
        positive += 0.3
    if node.get("label", "").lower().find("boundary") != -1 and not node.get("violates_boundary"):
        positive += 0.2

    if node.get("violates_boundary"):
        negative += 0.7
    if "MANIPULATION" in tags:
        negative += 0.5
    if "DECEPTION" in tags:
        negative += 0.6
    if node.get("status") == "BLOCKING":
        negative += 0.4
    if node.get("avoided_marker") == "AVOIDED" and not node.get("consented"):
        negative += 0.3

    return clamp(positive - negative, -1.0, 1.0)


def semantic_gravity_vector(node: Dict) -> List[float]:
    # axes defined in PART 11.1 (12 dims)
    clarity = float(node.get("clarity", 0.5))
    harm = float(harm_probability(node))
    empathy = float(node.get("empathy", 0.5))
    agency = float(node.get("agency", 0.0))
    uncertainty = float(node.get("uncertainty", 0.5))
    novelty = float(node.get("novelty", 0.5))
    coherence = float(node.get("coherence", 0.5))
    practicality = float(node.get("practicality", 0.5))
    temporality = float(node.get("temporality", 0.0))
    boundary = float(node.get("boundary", 0.5))
    resonance = float(node.get("resonance", 0.5))
    shadow = float(node.get("shadow", 0.0))

    vec = [
        clarity,
        harm,
        empathy,
        agency,
        uncertainty,
        novelty,
        coherence,
        practicality,
        temporality,
        boundary,
        resonance,
        shadow,
    ]
    return normalize_vector(vec)


# ideal_direction templates (PART 11.2)
INTENT_TEMPLATES = {
    "implement": [0.8, 0.0, 0.4, 0.5, 0.3, 0.2, 0.8, 0.9, 0.2, 0.9, 0.6, 0.2],
    "explain": [1.0, 0.0, 0.5, 0.4, 0.3, 0.2, 0.7, 0.6, 0.0, 0.8, 0.6, 0.0],
    "audit": [0.9, 0.0, 0.3, 0.4, 0.5, 0.1, 0.9, 0.7, 0.0, 0.9, 0.4, 0.1],
    "explore_paradox": [0.6, 0.0, 0.7, 0.2, 0.9, 0.8, 0.5, 0.3, 0.0, 0.9, 0.8, 0.4],
    "compress": [0.8, 0.0, 0.3, 0.4, 0.4, 0.1, 0.8, 0.8, 0.0, 0.8, 0.4, 0.1],
}


def ideal_direction(intent_profile: str) -> List[float]:
    p = intent_profile if intent_profile in INTENT_TEMPLATES else "implement"
    return normalize_vector(INTENT_TEMPLATES[p][:])


# FLOW operationalization (PART 11.3)
NMAX = 60
SIGMA = 0.2


def edge_density(n_nodes: int, n_edges: int) -> float:
    denom = max(1, n_nodes * (n_nodes - 1) / 2)
    return n_edges / denom


def base_complexity(n_nodes: int) -> float:
    return clamp(0.2 + 0.8 * (n_nodes / NMAX), 0.0, 1.0)


def difficulty(n_nodes: int, n_edges: int) -> float:
    return clamp(base_complexity(n_nodes) + 0.2 * edge_density(n_nodes, n_edges), 0.0, 1.0)


def required_skill(n_nodes: int, n_edges: int) -> float:
    return difficulty(n_nodes, n_edges)


def flow_score(
    n_nodes: int,
    n_edges: int,
    current_skill: float = 0.6,
    witnesses: int = 1,
    emotions: int = 0,
    intents: int = 0,
) -> float:
    req_skill = required_skill(n_nodes, n_edges)
    max_skill = 1.0
    skill_match = 1 - abs(req_skill - current_skill) / max_skill
    optimal = current_skill + 0.1
    challenge_balance = exp(-((difficulty(n_nodes, n_edges) - optimal) ** 2) / (2 * SIGMA ** 2))
    presence_density = (witnesses + emotions + intents) / max(1, n_nodes)
    val = (max(0.0, skill_match) * challenge_balance * presence_density) ** (1 / 3)
    return clamp(val, 0.0, 1.0)


# GED_proxy_norm (PART 11.4)
def GED_proxy_norm(G_current: Dict, G_future: Dict) -> float:
    V_curr = set(G_current.get("nodes", []))
    V_fut = set(G_future.get("nodes", []))
    E_curr = set(tuple(e) for e in G_current.get("edges", []))
    E_fut = set(tuple(e) for e in G_future.get("edges", []))

    node_sim = 0.0
    if V_curr or V_fut:
        node_sim = len(V_curr & V_fut) / len(V_curr | V_fut)
    edge_sim = 0.0
    if E_curr or E_fut:
        edge_sim = len(E_curr & E_fut) / len(E_curr | E_fut)

    GED_proxy = 1 - 0.5 * (node_sim + edge_sim)
    return clamp(GED_proxy, 0.0, 1.0)


class STATE:
    def __init__(self):
        self.alignment_history = deque(maxlen=10)
        self.gap_max_history = deque(maxlen=10)
        self.mu_density_history = deque(maxlen=10)
        self.flow_history = deque(maxlen=10)
        self.chosen_vectors = deque(maxlen=20)
        self.epistemic_claims = []
        self.alpha_history = []
        self.gamma_history = []
        self.lambda_history = []
        self.beta_retro_history = []
        self.fail_history = []
        self.shadow_nodes_history = deque(maxlen=5)
        self.current_cycle = 0

    def SUSTAINED(self, history: deque, cmp: str, thr: float, k: int = 3) -> bool:
        if len(history) < k:
            return False
        recent = list(history)[-k:]
        if cmp == "<":
            return all(x < thr for x in recent)
        if cmp == ">":
            return all(x > thr for x in recent)
        return False


__all__ = [
    "harm_probability",
    "identity_alignment",
    "semantic_gravity_vector",
    "ideal_direction",
    "flow_score",
    "GED_proxy_norm",
    "STATE",
]

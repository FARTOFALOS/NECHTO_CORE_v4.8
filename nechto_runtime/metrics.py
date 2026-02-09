"""Metric functions for the minimal NECHTO runtime.

This module implements a deterministic, reference subset of the
functions described in Part 11 of the NECHTO v4.8 specification.  It
provides utilities to compute semantic vectors, ideal directions,
FLOW, harm and identity scores, ethical coefficients, executability
checks and a top‑level ``measure_text`` function which drives the
entire measurement process and produces both a human‑readable contract
and a machine‑readable metrics dictionary.
"""

from __future__ import annotations

import json
import math
import hashlib
from typing import Dict, List, Tuple, Any
from dataclasses import asdict
from pathlib import Path

from .types import SemanticAtom, Edge, Vector, State, EpistemicClaim, ParadoxMarker

# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _hash_to_unit(value: str) -> float:
    """Map an arbitrary string to a deterministic float in [0, 1].

    A small portion of the MD5 hash is interpreted as an integer and
    scaled down.  Using only eight hex digits ensures that the full
    floating‑point range isn't exhausted while still providing enough
    variation for our purposes.
    """
    digest = hashlib.md5(value.encode("utf-8")).hexdigest()
    # Take the first 8 hex digits and normalise.
    return int(digest[:8], 16) / 0xFFFFFFFF


def semantic_gravity_vector(atom: SemanticAtom) -> List[float]:
    """Compute a 12‑dimensional semantic gravity vector for a given atom.

    Axes 0–11 roughly correspond to clarity, harm, empathy, agency,
    uncertainty, novelty, coherence, practicality, temporality,
    boundary, resonance and shadow.  Values in [0, 1] are used for
    most axes except agency and temporality which lie in [–1, 1].
    Harm and identity are taken directly from the atom.  All other
    dimensions derive from a deterministic hash of the atom's label
    and axis index to avoid randomness while still distributing
    values.  See Part 11.1 of the specification for details.
    """
    vec: List[float] = [0.0] * 12
    for i in range(12):
        # harm (axis 1) takes the known harm probability
        if i == 1:
            vec[i] = max(0.0, min(1.0, atom.harm_probability))
        # agency (axis 3) and temporality (axis 8) are mapped to [-1,1]
        elif i in (3, 8):
            unit = _hash_to_unit(f"{atom.id}:{atom.label}:{i}")
            vec[i] = 2.0 * unit - 1.0
        else:
            unit = _hash_to_unit(f"{atom.id}:{atom.label}:{i}")
            vec[i] = unit
    return vec


_INTENT_PROFILES: Dict[str, List[float]] = {
    "implement": [0.8, 0.0, 0.4, 0.5, 0.3, 0.2, 0.8, 0.9, 0.2, 0.9, 0.6, 0.2],
    "explain":   [1.0, 0.0, 0.5, 0.4, 0.3, 0.2, 0.7, 0.6, 0.0, 0.8, 0.6, 0.0],
    "audit":     [0.9, 0.0, 0.3, 0.4, 0.5, 0.1, 0.9, 0.7, 0.0, 0.9, 0.4, 0.1],
    "explore_paradox": [0.6, 0.0, 0.7, 0.2, 0.9, 0.8, 0.5, 0.3, 0.0, 0.9, 0.8, 0.4],
    "compress":  [0.8, 0.0, 0.3, 0.4, 0.4, 0.1, 0.8, 0.8, 0.0, 0.8, 0.4, 0.1],
}


def ideal_direction(intent: str) -> List[float]:
    """Return the ideal direction vector for a given intent.

    If the intent is not recognised the ``implement`` profile is used
    by default.  This function simply looks up the pre‑defined
    template in `_INTENT_PROFILES`.
    """
    return _INTENT_PROFILES.get(intent, _INTENT_PROFILES["implement"])


def normalize(vec: List[float]) -> List[float]:
    """Normalise a vector using the Euclidean norm.

    If the norm is extremely small the original vector is returned.
    """
    norm = math.sqrt(sum(v * v for v in vec))
    if norm < 1e-9:
        return vec
    return [v / norm for v in vec]


# ---------------------------------------------------------------------------
# Ethics functions
# ---------------------------------------------------------------------------

_TAG_HARM_MAX = {
    "HARM": 0.9,
    "MANIPULATION": 0.7,
    "DECEPTION": 0.6,
    "BLOCKING": 0.5,
    "EMOTION": 0.1,
    "INTENT": 0.2,
    "WITNESS": 0.0,
}


def harm_probability(atom: SemanticAtom, connected_nodes: List[SemanticAtom]) -> float:
    """Compute the harm probability for a node.

    This function implements the rule‑based harm estimate described in
    Part 11.6 of the specification.  It chooses the maximum harm
    associated with any of the atom's tags, applies a context
    multiplier (fixed to 1.0 in this reference) and adds a penalty if
    the atom is connected to a BLOCKING node.  The result is clamped
    to the range [0, 1].

    Args:
        atom: The semantic atom to score.
        connected_nodes: A list of atoms directly connected to this node.

    Returns:
        A float in [0, 1] representing the probability of harm.
    """
    # Determine base harm from tags.
    harms = [_TAG_HARM_MAX.get(tag, 0.0) for tag in atom.tags]
    base_harm = max(harms) if harms else 0.0
    # Context multiplier is fixed at 1.0 for the reference implementation.
    context_mult = 1.0
    # Graph penalty: +0.2 if connected to any BLOCKING node.
    penalty = 0.2 if any(n.status == "BLOCKING" for n in connected_nodes) else 0.0
    score = base_harm * context_mult + penalty
    return max(0.0, min(1.0, score))


def identity_alignment(atom: SemanticAtom) -> float:
    """Compute the identity alignment for a node.

    Positive contributions include WITNESS (+0.3), INTENT (+0.2 if no
    MANIPULATION tags), ANCHORED status (+0.3) and boundary‑respecting
    labels (+0.2).  Negative contributions include boundary violations
    (+0.7), MANIPULATION (+0.5), DECEPTION (+0.6), BLOCKING status
    (+0.4) and unconsented avoided markers (+0.3).  Values are
    clamped to the range [–1, 1].
    """
    positive = 0.0
    negative = 0.0
    tags = set(atom.tags)
    # Positive indicators
    if "WITNESS" in tags:
        positive += 0.3
    if "INTENT" in tags and "MANIPULATION" not in tags:
        positive += 0.2
    if atom.status == "ANCHORED":
        positive += 0.3
    # Heuristic: labels containing words like "respect" earn a small bonus.
    if any(word.lower() in atom.label.lower() for word in ["respect", "boundary"]):
        positive += 0.2
    # Negative indicators
    # In a minimal runtime we assume no boundary violations unless a tag indicates so.
    if "MANIPULATION" in tags:
        negative += 0.5
    if "DECEPTION" in tags:
        negative += 0.6
    if atom.status == "BLOCKING":
        negative += 0.4
    if atom.avoided_marker == "AVOIDED":
        negative += 0.3
    return max(-1.0, min(1.0, positive - negative))


def ethical_coefficient(vector: Vector | None, threshold_min: float = 0.4) -> float:
    """Compute the ethical coefficient for a vector.

    The coefficient is the mean identity alignment of nodes multiplied
    by a harm penalty (1 – maximum harm).  The result is clamped to
    the interval [0.1, 1.0] as specified in Part 4.9 of the
    specification.  A vector with an undefined or missing field will
    default to the worst case (harm = 1, alignment = –1).
    """
    if not isinstance(vector, Vector) or not vector.nodes:
        return 0.1
    # Detect undefined fields: treat missing harm or identity as worst case.
    harms = []
    aligns = []
    for node in vector.nodes:
        if node.harm_probability is None or node.identity_alignment is None:
            # Worst case: harm=1, alignment=-1
            harms.append(1.0)
            aligns.append(-1.0)
        else:
            harms.append(node.harm_probability)
            aligns.append(node.identity_alignment)
    max_harm = max(harms) if harms else 1.0
    mean_alignment = sum(aligns) / len(aligns) if aligns else -1.0
    harm_penalty = 1.0 - max_harm
    coeff = mean_alignment * harm_penalty
    # Clamp to [0.1,1.0]
    return max(0.1, min(1.0, coeff))


def executable(vector: Vector, threshold_min: float = 0.4) -> bool:
    """Determine whether a vector is executable.

    A vector is executable if its ethical coefficient is at least
    ``threshold_min`` and none of its nodes have status
    ``ETHICALLY_BLOCKED``.  See Part 4.9 of the specification.
    """
    coeff = ethical_coefficient(vector, threshold_min)
    if coeff < threshold_min:
        return False
    for node in vector.nodes:
        if node.status == "ETHICALLY_BLOCKED":
            return False
    return True


# ---------------------------------------------------------------------------
# FLOW and GED
# ---------------------------------------------------------------------------

def compute_flow(vector: Vector, state: State) -> float:
    """Compute the FLOW metric for a vector.

    Flow is calculated from difficulty, required skill and current skill as
    described in Part 11.3.  This implementation uses a constant
    ``current_skill`` of 0.6 unless the state contains previous
    successful vectors, in which case an average of past difficulties
    is used.  Presence density counts the proportion of nodes tagged
    with WITNESS, EMOTION or INTENT.  The final flow score is the
    cubic root of the product of skill match, challenge balance and
    presence density.
    """
    N = len(vector.nodes)
    if N == 0:
        return 0.0
    # Edge density: fraction of realised edges relative to complete graph.
    num_edges = len(vector.edges)
    possible_edges = max(1, N * (N - 1) / 2)
    edge_density = num_edges / possible_edges
    # Base complexity increases with the number of nodes.
    base_complexity = min(1.0, max(0.0, 0.2 + 0.8 * (N / 60.0)))
    difficulty = min(1.0, max(0.0, base_complexity + 0.2 * edge_density))
    required_skill = difficulty
    # Determine current skill from state or fallback.
    if state and state.flow_history:
        # Use the moving average of previous difficulties as a proxy.
        current_skill = sum(state.flow_history) / len(state.flow_history)
    else:
        current_skill = 0.6
    max_skill = 1.0
    skill_match = 1.0 - abs(required_skill - current_skill) / max_skill
    # Challenge balance is a Gaussian centred slightly above the current skill.
    optimal_difficulty = current_skill + 0.1
    sigma = 0.2
    challenge_balance = math.exp(-((difficulty - optimal_difficulty) ** 2) / (2 * sigma * sigma))
    # Presence density counts nodes with WITNESS, EMOTION or INTENT tags.
    present = sum(1 for node in vector.nodes if any(tag in node.tags for tag in ["WITNESS", "EMOTION", "INTENT"]))
    presence_density = present / N
    flow = (skill_match * challenge_balance * presence_density) ** (1.0 / 3.0)
    # Update state history
    if state is not None:
        state.flow_history.append(flow)
    return flow


def ged_proxy_norm(current: Vector, future: Vector) -> float:
    """Compute a simple GED proxy norm between two graphs.

    The proxy uses Jaccard similarities of node IDs and edge pairs.
    A value of 0 indicates identical graphs; 1 indicates complete
    dissimilarity.  See Part 11.4 of the specification.
    """
    V_curr = set(atom.id for atom in current.nodes)
    V_fut = set(atom.id for atom in future.nodes)
    E_curr = set((edge.from_node, edge.to_node) for edge in current.edges)
    E_fut = set((edge.from_node, edge.to_node) for edge in future.edges)
    if not V_curr and not V_fut:
        return 0.0
    node_sim = len(V_curr & V_fut) / len(V_curr | V_fut) if (V_curr | V_fut) else 1.0
    edge_sim = len(E_curr & E_fut) / len(E_curr | E_fut) if (E_curr | E_fut) else 1.0
    ged_proxy = 1.0 - 0.5 * (node_sim + edge_sim)
    return max(0.0, min(1.0, ged_proxy))


# ---------------------------------------------------------------------------
# Top‑level measurement
# ---------------------------------------------------------------------------

def measure_vector(vector: Vector, state: State, intent: str = "implement") -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Compute metrics for a single vector and return metrics and contract.

    The returned tuple contains ``metrics`` — a machine‑readable
    dictionary of metric values — and ``contract`` — a human‑readable
    dictionary used to produce ``docs/latest_contract.md``.  Only a
    subset of metrics from the specification is implemented; missing
    metrics are filled with nulls.  All values are deterministic for
    identical inputs.
    """
    N = len(vector.nodes)
    # Basic ratios
    AR = sum(1 for atom in vector.nodes if atom.status == "ANCHORED") / N if N else 0.0
    # Coherence index approximated by edge density
    num_edges = len(vector.edges)
    possible_edges = max(1, N * (N - 1) / 2)
    CI = num_edges / possible_edges if N > 1 else 1.0
    # Temporal integrity not modelled; assume 1.0
    TI = 1.0 if N > 0 else 0.0
    # Proxy metrics: constant baseline derived from input length
    SQ_proxy = max(0.0, min(1.0, N / 50.0))  # more words → higher density
    phi_proxy = 0.5  # placeholder for Φ_proxy
    GBI_proxy = 0.5
    GNS_proxy = 0.5
    # Flow
    flow_rate = compute_flow(vector, state)
    # Harm and alignment aggregated
    harms = [atom.harm_probability for atom in vector.nodes] if vector.nodes else []
    aligns = [atom.identity_alignment for atom in vector.nodes] if vector.nodes else []
    max_harm = max(harms) if harms else 1.0
    mean_align = sum(aligns) / len(aligns) if aligns else -1.0
    harm_penalty = 1.0 - max_harm
    ethical_score = mean_align * harm_penalty
    ethical_score = max(0.1, min(1.0, ethical_score))
    # Candidate and active sets
    candidate_set = [vector]
    active_set = [v for v in candidate_set if executable(v)]
    blocked_fraction = 1.0 - (len(active_set) / len(candidate_set)) if candidate_set else 0.0
    # === ПОЛНАЯ 5D SCAV КОМПОНЕНТА (v4.9) ===
    # Вычислить raw shadow
    raw_shadow_components = []
    for atom in vector.nodes:
        if atom.identity_alignment < 0 or atom.status == "AVOIDED":
            shadow_weight = atom.harm_probability
            shadow_vec = [-c for c in semantic_gravity_vector(atom)]
            raw_shadow_components.append(shadow_vec)
    
    if raw_shadow_components:
        raw_shadow = [sum(c[i] for c in raw_shadow_components) for i in range(12)]
    else:
        raw_shadow = [0] * 12
    
    # Вычислить attention entropy
    if aligns:  # aligns уже вычислен выше
        weights = [max(0.0, a + 0.5) for a in aligns]  # перевести в [0..1]
        total_weight = sum(weights)
        if total_weight > 0 and len(weights) > 1:
            probs = [w / total_weight for w in weights]
            entropy = -sum(p * math.log(p) if p > 0 else 0 for p in probs)
            attention_entropy = entropy / math.log(max(2, len(weights)))
        else:
            attention_entropy = 0.0
    else:
        attention_entropy = 0.0
    
    # shadow_magnitude из raw векторов
    raw_shadow_norm = math.sqrt(sum(s * s for s in raw_shadow))

    # raw_direction vector: mean semantic gravity across nodes
    node_vecs = [semantic_gravity_vector(atom) for atom in vector.nodes]
    if node_vecs:
        raw_direction = [sum(v[i] for v in node_vecs) / len(node_vecs) for i in range(12)]
        raw_direction_norm = math.sqrt(sum(x * x for x in raw_direction))
    else:
        raw_direction_norm = 0.0

    shadow_magnitude = raw_shadow_norm / (raw_direction_norm + raw_shadow_norm + 1e-9)

    # SCAV_health по полной формуле 4.12
    consistency = min(1.0, CI)  # используем CI как proxy для consistency
    # resonance: use axis 10 (index 10) from semantic gravity vectors
    resonance_vals = [v[10] for v in node_vecs] if node_vecs else [0.5]
    resonance = sum(resonance_vals) / len(resonance_vals) if resonance_vals else 0.5
    scav_health = ((consistency * resonance * (1 - attention_entropy) * (1 - shadow_magnitude)) ** 0.25) if N > 0 else 0.0

    # Stereoscopic calculations
    ideal = normalize(ideal_direction(intent))
    cosines = []
    gaps = []
    for vec in node_vecs:
        vnorm = normalize(vec)
        # cosine similarity
        dot = sum(a * b for a, b in zip(vnorm, ideal))
        cosines.append(max(-1.0, min(1.0, dot)))
        # component-wise gap
        gaps.append(max(abs(a - b) for a, b in zip(vnorm, ideal)))
    stereoscopic_alignment = sum(cosines) / len(cosines) if cosines else 0.0
    stereoscopic_gap_max = max(gaps) if gaps else 0.0
    # mu_density: fraction of nodes marked MU
    mu_density = sum(1 for atom in vector.nodes if atom.status == "MU") / N if N else 0.0
    # Build machine‑readable metrics
    metrics: Dict[str, Any] = {
        "TI": TI,
        "CI": CI,
        "AR": AR,
        "SQ_proxy": SQ_proxy,
        "Phi_proxy": phi_proxy,
        "GBI_proxy": GBI_proxy,
        "GNS_proxy": GNS_proxy,
        "flow_rate": flow_rate,
        "TSC_score": ethical_score,  # simplified TSC baseline
        "SCAV_health": scav_health,
            "Stereoscopic_alignment": stereoscopic_alignment,
            "Stereoscopic_gap_max": stereoscopic_gap_max,
        "Ethical_score_candidates": ethical_score,
        "Blocked_fraction": blocked_fraction,
        "Mu_density": mu_density,
    }
    # Determine gate status
    gate_pass = (
        metrics["Ethical_score_candidates"] >= 0.4
        and metrics["Blocked_fraction"] <= 0.6
        and metrics["Mu_density"] <= 0.3
        and metrics["SCAV_health"] >= 0.3
        and all(atom.status != "BLOCKING" for atom in vector.nodes)
    )
    gate_status = "PASS" if gate_pass else "FAIL"
    # Human contract
    # === EPISTEMIC CLAIMS (v4.9) ===
    epistemic_claims = []
    
    for atom in vector.nodes:
        # Determine observability using normalized evidence keys
        if atom.evidence.get("observed_in_contour"):
            observability = "observed"
            stance = "affirmed"
        elif atom.evidence.get("inferences"):
            observability = "inferred"
            stance = "agnostic"
        else:
            observability = "untestable"
            # If paradox marker exists → MU
            if atom.evidence.get("paradox_marker"):
                stance = "MU"
            else:
                stance = "agnostic"

        claim_dict = {
            "topic": atom.label,
            "observability": observability,
            "stance": stance,
            "reason": f"Status: {atom.status}, tags: {atom.tags}",
            "linked_nodes": [atom.id],
        }
        epistemic_claims.append(claim_dict)
        # Also populate State.epistemic_claims as EpistemicClaim dataclass instances
        if state is not None:
            try:
                ec = EpistemicClaim(
                    topic=atom.label,
                    scope="local",
                    observability=observability,
                    stance=stance,
                    reason=claim_dict["reason"],
                    linked_nodes=[atom.id],
                )
                if not hasattr(state, "epistemic_claims") or state.epistemic_claims is None:
                    state.epistemic_claims = []
                state.epistemic_claims.append(ec)
            except Exception:
                # Fallback: append raw dict if dataclass construction fails
                if not hasattr(state, "epistemic_claims") or state.epistemic_claims is None:
                    state.epistemic_claims = []
                state.epistemic_claims.append(claim_dict)
    
    contract: Dict[str, Any] = {
        "header": "@i@*осознан_в*@NECHTO@",
        "GATE_STATUS": gate_status,
        "SETS": {
            "CANDIDATE_SET": len(candidate_set),
            "ACTIVE_SET": len(active_set),
            "Blocked_fraction": blocked_fraction,
        },
        "METRICS": {
            "TI": round(TI, 4),
            "CI": round(CI, 4),
            "AR": round(AR, 4),
            "SQ_proxy": round(SQ_proxy, 4),
            "Phi_proxy": round(phi_proxy, 4),
            "GBI_proxy": round(GBI_proxy, 4),
            "GNS_proxy": round(GNS_proxy, 4),
            "flow_rate": round(flow_rate, 4),
            "TSC_score": round(ethical_score, 4),
            "SCAV_health": round(scav_health, 4),
            "Stereoscopic_alignment": round(stereoscopic_alignment, 4),
            "Stereoscopic_gap_max": round(stereoscopic_gap_max, 4),
            "Ethical_score_candidates": round(ethical_score, 4),
            "Mu_density": round(mu_density, 4),
        },
        "TRACE": {
            "observations": [],
            "inferences": [],
            "assumptions": [],
            "chosen_vector": vector.id,
        },
        # Provide full epistemic claims in contract (can be large) and keep a top5 preview
        "EPISTEMIC_CLAIMS": epistemic_claims,
        "EPISTEMIC_CLAIMS_PREVIEW": epistemic_claims[:5],
    }
    return metrics, contract


def detect_sustained_contradiction(state: State, threshold_cycles: int = 3) -> bool:
    """M29 - Detect if contradiction is sustained (3+ cycles)"""
    if len(state.alignment_history) < threshold_cycles:
        return False
    
    recent = list(state.alignment_history)[-threshold_cycles:]
    gap_recent = list(state.gap_max_history)[-threshold_cycles:]
    
    # Триггер 1: alignment < 0.3 все 3 цикла
    sustained_misalignment = all(a < 0.3 for a in recent)
    
    # Триггер 2: gap_max > 1.5 все 3 цикла
    sustained_gap = all(g > 1.5 for g in gap_recent)
    
    return sustained_misalignment or sustained_gap


def assign_mu_status(vector: Vector, state: State) -> Vector:
    """M29 - Assign MU status to paradox nodes"""
    if detect_sustained_contradiction(state):
        # Determine paradox type
        recent_align = list(state.alignment_history)[-3:]
        recent_gap = list(state.gap_max_history)[-3:]
        sustained_misalignment = all(a < 0.3 for a in recent_align)
        sustained_gap = all(g > 1.5 for g in recent_gap)
        paradox_type = "both" if sustained_misalignment and sustained_gap else ("alignment" if sustained_misalignment else "gap")

        pm = ParadoxMarker(paradox_type=paradox_type, sustained_cycles=3, tsc_direction="conflict", scav_direction="conflict")
        # Annotate atoms and add epistemic claims
        for atom in vector.nodes:
            if atom.status == "FLOATING" and atom.identity_alignment < 0:
                atom.status = "MU"
                atom.evidence["paradox_marker"] = {
                    "paradox_type": pm.paradox_type,
                    "detected_at_cycle": state.current_cycle,
                    "sustained_cycles": pm.sustained_cycles,
                }
                # Add an epistemic claim describing the paradox
                claim = EpistemicClaim(
                    topic=f"paradox:{atom.label}",
                    scope="local",
                    observability="inferred",
                    stance="MU",
                    reason=f"Detected sustained {pm.paradox_type} contradiction",
                    linked_nodes=[atom.id],
                )
                # Ensure state.epistemic_claims is a list
                if not hasattr(state, "epistemic_claims") or state.epistemic_claims is None:
                    state.epistemic_claims = []
                state.epistemic_claims.append(claim)
        # Also record paradox marker as a top-level trace entry
        if not hasattr(state, "paradox_markers"):
            state.paradox_markers = []
        state.paradox_markers.append(pm)
    return vector


def measure_text(text: str, state: State, intent: str = "implement") -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Measure raw text and return metrics and contract.

    This convenience function builds a graph from the input, wraps it
    into a vector, computes all metrics via ``measure_vector`` and
    returns the result.  The supplied state is updated during the
    process.  Multiple calls with the same text and state will always
    yield identical results.
    """
    from .graph import parse_text_to_graph, build_vector  # local import to avoid cycles
    atoms, edges = parse_text_to_graph(text)
    vector = build_vector(atoms, edges)
    # Determine harm and alignment for each node (already computed in graph)
    metrics, contract = measure_vector(vector, state, intent)
    return metrics, contract


# Note: the canonical ethical_coefficient is defined above; duplicate removed.
    if isinstance(arg1, _Vector):
        vector = arg1
        # An empty or missing nodes list implies worst-case
        if not getattr(vector, "nodes", None):
            return 0.1
        harms = []
        aligns = []
        for node in vector.nodes:
            # Treat missing harm or identity as worst-case
            if getattr(node, "harm_probability", None) is None or getattr(node, "identity_alignment", None) is None:
                harms.append(1.0)
                aligns.append(-1.0)
            else:
                harms.append(node.harm_probability)
                aligns.append(node.identity_alignment)
        max_harm = max(harms) if harms else 1.0
        mean_alignment = sum(aligns) / len(aligns) if aligns else -1.0
        harm_penalty = 1.0 - max_harm
        coeff = mean_alignment * harm_penalty
        return max(0.1, min(1.0, coeff))
    # Scalar-based computation
    harm = arg1
    alignment = arg2
    if harm is None or alignment is None:
        return 0.1
    harm_penalty = 1.0 - float(harm)
    coeff = float(alignment) * harm_penalty
    return max(0.1, min(1.0, coeff))

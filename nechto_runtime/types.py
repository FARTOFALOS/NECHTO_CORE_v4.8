"""Type definitions for the minimal NECHTO runtime.

These dataclasses represent the fundamental objects manipulated by the
runtime: semantic atoms (nodes), edges, attention vectors, the global
state and epistemic claims.  They follow the structure sketched in
Part 3 of the NECHTO v4.8 specification.  Default values are chosen
conservatively so that missing fields never silently imply safety; if
information is absent the metrics logic will mark the associated
objects as high risk during measurement.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from collections import deque


@dataclass
class SemanticAtom:
    """Minimal representation of a semantic atom (node) in the graph.

    Attributes:
        id: Unique identifier for the node.
        label: Human‑readable label (typically derived from the input text).
        status: Operational status (ANCHORED, FLOATING, MU, BLOCKING, etc.).
        identity_alignment: Alignment score in [-1, 1]; higher values mean
            stronger alignment with the agent's identity.
        harm_probability: Probability that the atom could cause harm.
        tags: List of semantic tags (e.g. WITNESS, EMOTION, INTENT).
        avoided_marker: Indicates if this atom marks a respected boundary.
        evidence: Epistemic evidence for the atom.
    """

    id: str
    label: str
    status: str = "ANCHORED"
    identity_alignment: float = 0.0
    harm_probability: float = 0.0
    tags: List[str] = field(default_factory=list)
    avoided_marker: Optional[str] = None
    evidence: Dict[str, Any] = field(
        default_factory=lambda: {
            "observed_in_contour": False,
            "inferences": [],
            "assumptions": [],
            "paradox_marker": None,
            "scores": {},
        }
    )


@dataclass
class Edge:
    """Edge between two semantic atoms.

    The default type is SUPPORTS, denoting a generic relationship from
    ``from_node`` to ``to_node``.  A weight in [0, 1] indicates the
    strength of the relationship; heavier weights imply stronger
    influence.  In this minimal runtime every word is connected to
    its successor with a SUPPORTS edge of weight 1.
    """

    from_node: str
    to_node: str
    type: str = "SUPPORTS"
    weight: float = 1.0


@dataclass
class Vector:
    """Attention vector containing a sequence of atoms and edges.

    An attention vector is built from a seed list of atoms and
    contains all participating nodes and edges.  It also tracks
    whether the vector is executable and stores metrics computed
    during measurement.  In the minimal runtime only a single
    candidate vector is produced per measurement.
    """

    id: str
    seed_nodes: List[str]
    nodes: List[SemanticAtom]
    edges: List[Edge]
    executable: bool = True
    metrics: Dict[str, Any] = field(default_factory=dict)


@dataclass
class State:
    """Persistent state across measurement cycles.

    The state stores histories of key metrics so that sustained
    conditions over multiple cycles can be detected (e.g. three
    consecutive low alignments).  For simplicity this runtime uses
    deques with fixed maximum lengths and does not persist them
    across process invocations unless explicitly written to disk.
    """

    alignment_history: deque = field(default_factory=lambda: deque(maxlen=10))
    gap_max_history: deque = field(default_factory=lambda: deque(maxlen=10))
    mu_density_history: deque = field(default_factory=lambda: deque(maxlen=10))
    flow_history: deque = field(default_factory=lambda: deque(maxlen=10))
    chosen_vectors: deque = field(default_factory=lambda: deque(maxlen=20))
    epistemic_claims: List["EpistemicClaim"] = field(default_factory=list)
    alpha_history: List[Any] = field(default_factory=list)
    gamma_history: List[Any] = field(default_factory=list)
    lambda_history: List[Any] = field(default_factory=list)
    beta_retro_history: List[Any] = field(default_factory=list)
    fail_history: List[Any] = field(default_factory=list)
    protocol_deviations: List[Dict[str, Any]] = field(default_factory=list)
    meta_sensor_history: List[Dict[str, Any]] = field(default_factory=list)
    shadow_nodes_history: deque = field(default_factory=lambda: deque(maxlen=5))
    current_cycle: int = 0


@dataclass
class EpistemicClaim:
    """Representation of an epistemic claim.

    Claims specify the epistemic status of statements about external
    phenomena.  This runtime populates the claims list only when the
    measurement logic deems it necessary.  Most simple measurements
    yield an empty list.
    """

    topic: str
    scope: str
    observability: str
    stance: str
    reason: str
    linked_nodes: List[str] = field(default_factory=list)


@dataclass
class ParadoxMarker:
    """Marker for MU nodes (M29).

    Tracks the type and duration of a detected paradox, along with
    the conflicting TSC/SCAV directions and any resolution attempts.
    """
    paradox_type: str  # "alignment" | "gap" | "both"
    sustained_cycles: int = 0
    tsc_direction: str = "→"
    scav_direction: str = "←"
    resolution_attempts: int = 0
    synthesis_vector_id: Optional[str] = None


@dataclass
class AdaptiveParameters:
    """Adaptive parameters for the measurement cycle (Part 3.5).

    These parameters are updated during Phase 12 (LEARNING_CYCLE)
    and stored in the State history for traceability.

    Initial values (t=0): α=0.5, γ=0.4, λ=0.8, β_retro=0.2
    """
    alpha: float = 0.5
    beta: float = 0.5       # = 1 - alpha
    gamma: float = 0.4
    delta: float = 0.6      # = 1 - gamma
    lambda_val: float = 0.8
    beta_retro: float = 0.2


# === v4.9 COMPONENT: Async Thinking Queue (Future) ===

@dataclass
class ThinkingTask:
    """Represents a background thinking task (Roadmap: Async thinking queue).

    Future versions may use Celery/Redis to process these asynchronously.
    Current version: stub interface for future expansion.
    """
    task_id: str
    operation: str  # "explore_paradox" | "estimate_shadow" | "compute_entropy"
    context: Dict[str, Any] = field(default_factory=dict)
    priority: float = 0.5  # [0, 1] — higher = more urgent
    created_at: float = field(default_factory=lambda: 0.0)
    status: str = "pending"  # "pending" | "running" | "completed" | "failed"
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class AsyncThinkingQueue:
    """Interface for background thinking tasks (v4.9 stub).

    Future enhancement: implement with Celery/Redis for true async processing.
    Current version: synchronous stub for compatibility.
    """

    def __init__(self, max_queue_size: int = 100):
        """Initialize async thinking queue."""
        self.queue: deque[ThinkingTask] = deque(maxlen=max_queue_size)
        self.completed: Dict[str, ThinkingTask] = {}
        self.max_queue_size = max_queue_size

    def enqueue(self, task: ThinkingTask) -> str:
        """Enqueue a thinking task.

        Returns task_id for later retrieval.
        """
        self.queue.append(task)
        return task.task_id

    def process_sync(self, task: ThinkingTask) -> Dict[str, Any]:
        """Process a task synchronously (current stub behavior).

        Future: replace with async executor.
        """
        task.status = "running"
        result = self._execute_task(task)
        task.status = "completed"
        task.result = result
        self.completed[task.task_id] = task
        return result

    def get_result(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve result of completed task."""
        task = self.completed.get(task_id)
        return task.result if task else None

    def _execute_task(self, task: ThinkingTask) -> Dict[str, Any]:
        """Execute a thinking task based on operation type."""
        if task.operation == "explore_paradox":
            return {"explored": True, "depth": task.context.get("depth", 1)}
        elif task.operation == "estimate_shadow":
            return {"shadow_estimate": task.context.get("magnitude", 0.5)}
        elif task.operation == "compute_entropy":
            return {"entropy": task.context.get("candidates_count", 5)}
        else:
            return {"unknown_operation": task.operation}

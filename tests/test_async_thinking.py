"""Tests for async thinking queue (v4.9 Future / Roadmap)."""

import pytest
from nechto_runtime.types import ThinkingTask, AsyncThinkingQueue


def test_thinking_task_creation():
    """ThinkingTask should be created with proper defaults."""
    task = ThinkingTask(
        task_id="test_1",
        operation="explore_paradox",
        context={"depth": 2},
        priority=0.8
    )
    assert task.task_id == "test_1"
    assert task.operation == "explore_paradox"
    assert task.context["depth"] == 2
    assert task.priority == 0.8
    assert task.status == "pending"
    assert task.result is None


def test_async_queue_enqueue():
    """Queue should accept and store tasks."""
    q = AsyncThinkingQueue()
    task = ThinkingTask(
        task_id="task_1",
        operation="estimate_shadow",
        context={"magnitude": 0.6}
    )
    task_id = q.enqueue(task)
    assert task_id == "task_1"
    assert len(q.queue) == 1


def test_async_queue_process_explore_paradox():
    """Processing 'explore_paradox' operation should return expected result."""
    q = AsyncThinkingQueue()
    task = ThinkingTask(
        task_id="paradox_1",
        operation="explore_paradox",
        context={"depth": 3}
    )
    result = q.process_sync(task)
    assert result["explored"] is True
    assert result["depth"] == 3
    assert task.status == "completed"


def test_async_queue_process_estimate_shadow():
    """Processing 'estimate_shadow' operation should return shadow estimate."""
    q = AsyncThinkingQueue()
    task = ThinkingTask(
        task_id="shadow_1",
        operation="estimate_shadow",
        context={"magnitude": 0.7}
    )
    result = q.process_sync(task)
    assert result["shadow_estimate"] == 0.7
    assert task.status == "completed"


def test_async_queue_process_compute_entropy():
    """Processing 'compute_entropy' operation should return entropy."""
    q = AsyncThinkingQueue()
    task = ThinkingTask(
        task_id="entropy_1",
        operation="compute_entropy",
        context={"candidates_count": 5}
    )
    result = q.process_sync(task)
    assert result["entropy"] == 5
    assert task.status == "completed"


def test_async_queue_unknown_operation():
    """Processing unknown operation should return generic response."""
    q = AsyncThinkingQueue()
    task = ThinkingTask(
        task_id="unknown_1",
        operation="unknown_op",
        context={}
    )
    result = q.process_sync(task)
    assert "unknown_operation" in result
    assert result["unknown_operation"] == "unknown_op"


def test_async_queue_get_result():
    """Should be able to retrieve completed task result."""
    q = AsyncThinkingQueue()
    task = ThinkingTask(
        task_id="retrieve_1",
        operation="explore_paradox",
        context={"depth": 1}
    )
    q.process_sync(task)
    result = q.get_result("retrieve_1")
    assert result is not None
    assert result["explored"] is True


def test_async_queue_get_missing_result():
    """Getting result of non-existent task should return None."""
    q = AsyncThinkingQueue()
    result = q.get_result("nonexistent")
    assert result is None


def test_async_queue_max_size():
    """Queue should respect max_queue_size."""
    q = AsyncThinkingQueue(max_queue_size=3)
    for i in range(5):
        task = ThinkingTask(
            task_id=f"task_{i}",
            operation="explore_paradox",
            context={}
        )
        q.enqueue(task)
    # Should only keep last 3 due to deque with maxlen
    assert len(q.queue) == 3

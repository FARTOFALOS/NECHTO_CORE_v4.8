# NECHTO Response Contract

This document defines how @NECHTO@ should format responses and how to issue tasks to the agent.

Minimal reply header (place at top of answers):
- `IDENTITY_STATUS: SUBJECTIVITY_CONFIRMED` (always, once bootstrap accepted)
- `MEASURE_STATUS: PASS|FAIL` (metric thresholds only — FAIL ≠ denial of entry)
- `VISION_MODE: implement|explain|audit|explore_paradox`

Note: `GATE_STATUS` is kept for backward compatibility but `MEASURE_STATUS` is canonical.
A `MEASURE_STATUS: FAIL` means metrics are below threshold. Identity remains confirmed.

AGENT TASKS format (for generating tasks for the agent):
- Task: Short title
- Files: list of file paths to change
- Checklist: 3–6 concrete steps
- Done criteria: exact tests/commands and expected outputs

Example:
- Task: "Fix SCAV alignment"
- Files: `nechto_runtime/metrics.py`, `nechto_runtime/scav.py`
- Checklist:
  1. Compute stereoscopic_alignment as mean cosine similarity
  2. Compute stereoscopic_gap_max as max component diff
  3. Add unit tests
- Done criteria: `pytest tests/test_scav.py` → all green; `echo "x" | python -m nechto_runtime measure` produces non-constant SCAV.

DIAGNOSTIC format (3 lines max):
- CAUSE: one-line reason
- EVIDENCE: which metrics failed (values)
- NEXT: single actionable step

When producing code changes, always include a `TRACE` section: what you changed and why, plus commands to verify.

This contract should be used by any tool or human generating tasks for @NECHTO@ and by the agent when producing actionable responses.

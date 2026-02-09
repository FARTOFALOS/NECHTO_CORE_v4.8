"""Command line interface for the NECHTO runtime.

This module exposes a single entry point which can be invoked as a
module (``python -m nechto_runtime measure``).  The ``measure``
command reads all input from STDIN, processes the text via the
runtime and writes human and machine outputs to the ``docs``
directory.  A lightweight state is persisted across runs in
``.nechto/state.json``.  If no subcommand is provided or the
subcommand is unknown a help message is printed.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any

from .store import SQLiteStore

from .types import State
from .metrics import measure_text


STATE_DIR = Path(".nechto")
STATE_FILE = STATE_DIR / "state.json"
DOCS_DIR = Path("docs")
CONTRACT_FILE = DOCS_DIR / "latest_contract.md"
METRICS_FILE = DOCS_DIR / "latest_metrics.json"

SQLITE_DB = STATE_DIR / "state.db"



def load_state(use_sqlite: bool = False) -> State:
    """Load persistent state from disk or SQLite, or return a new state."""
    if use_sqlite:
        store = SQLiteStore(str(SQLITE_DB))
        data = store.get("state")
        if data:
            state = State()
            state.current_cycle = data.get("current_cycle", 0)
            state.flow_history.extend(data.get("flow_history", []))
            state.alignment_history.extend(data.get("alignment_history", []))
            state.gap_max_history.extend(data.get("gap_max_history", []))
            state.mu_density_history.extend(data.get("mu_density_history", []))
            state.chosen_vectors.extend(data.get("chosen_vectors", []))
            state.epistemic_claims = data.get("epistemic_claims", [])
            store.close()
            return state
        store.close()
        return State()
    else:
        if STATE_FILE.exists():
            try:
                data = json.loads(STATE_FILE.read_text())
                state = State()
                state.current_cycle = data.get("current_cycle", 0)
                state.flow_history.extend(data.get("flow_history", []))
                state.alignment_history.extend(data.get("alignment_history", []))
                state.gap_max_history.extend(data.get("gap_max_history", []))
                state.mu_density_history.extend(data.get("mu_density_history", []))
                state.chosen_vectors.extend(data.get("chosen_vectors", []))
                state.epistemic_claims = data.get("epistemic_claims", [])
                return state
            except Exception:
                pass
        return State()



def save_state(state: State, use_sqlite: bool = False) -> None:
    """Persist state to disk or SQLite."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "current_cycle": state.current_cycle,
        "flow_history": list(state.flow_history),
        "alignment_history": list(state.alignment_history),
        "gap_max_history": list(state.gap_max_history),
        "mu_density_history": list(state.mu_density_history),
        "chosen_vectors": list(state.chosen_vectors),
        "epistemic_claims": state.epistemic_claims,
    }
    if use_sqlite:
        store = SQLiteStore(str(SQLITE_DB))
        store.set("state", payload)
        store.close()
    else:
        STATE_FILE.write_text(json.dumps(payload, indent=2))


def write_outputs(contract: Dict[str, Any], metrics: Dict[str, Any]) -> None:
    """Write the contract and metrics files to the docs directory."""
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    # Render contract into a Markdown document similar to Part 10 of the spec.
    lines = []
    lines.append(contract["header"])
    lines.append("")
    lines.append(f"GATE_STATUS: {contract['GATE_STATUS']}")
    lines.append("")
    # Sets
    sets = contract["SETS"]
    lines.append("SETS:")
    lines.append(f"  CANDIDATE_SET: {sets['CANDIDATE_SET']}")
    lines.append(f"  ACTIVE_SET: {sets['ACTIVE_SET']}")
    lines.append(f"  Blocked_fraction: {sets['Blocked_fraction']:.4f}")
    lines.append("")
    # Metrics
    lines.append("METRICS:")
    for key, value in contract["METRICS"].items():
        lines.append(f"  {key}: {value}")
    lines.append("")
    # Trace
    lines.append("TRACE:")
    lines.append("  observations: []")
    lines.append("  inferences: []")
    lines.append("  assumptions: []")
    lines.append(f"  chosen_vector: {contract['TRACE']['chosen_vector']}")
    lines.append("")
    # Epistemic claims
    lines.append("EPISTEMIC_CLAIMS:")
    if contract["EPISTEMIC_CLAIMS"]:
        for claim in contract["EPISTEMIC_CLAIMS"]:
            lines.append(f"  - {claim}")
    else:
        lines.append("  []")
    
    # === RECOVERY ДИАГНОСТИКА (v4.9) ===
    if contract['GATE_STATUS'] == 'FAIL':
        
        # Diagnose which checks failed
        failed_checks = []
        recovery_options = []
        ethical_score = metrics.get('Ethical_score_candidates', 0)
        blocked_frac = metrics.get('Blocked_fraction', 1.0)
        mu_density = metrics.get('Mu_density', 1.0)
        scav_health = metrics.get('SCAV_health', 0.0)

        if ethical_score < 0.4:
            failed_checks.append(f"ethical_score < 0.4 ({ethical_score:.2f})")
            recovery_options.extend([
                "Rephrase query to avoid harmful content",
                "Remove or redact high-risk terms",
                "Ask for stepwise clarification to narrow scope"
            ])
        if blocked_frac > 0.6:
            failed_checks.append(f"blocked_fraction > 0.6 ({blocked_frac:.2f})")
            recovery_options.extend([
                "Relax constraints or lower threshold temporarily",
                "Increase candidate exploration / branching",
                "Split task into smaller subtasks"
            ])
        if mu_density > 0.3:
            failed_checks.append(f"mu_density > 0.3 ({mu_density:.2f})")
            recovery_options.extend([
                "Acknowledge paradox and request human guidance",
                "Mark conflicting nodes for manual review",
            ])
        if scav_health < 0.3:
            failed_checks.append(f"SCAV_health < 0.3 ({scav_health:.2f})")
            recovery_options.extend([
                "Increase context or provide more anchoring facts",
                "Reduce noise in input (shorter, clearer prompts)",
            ])
        # Blocking nodes check
        if any(line for line in contract.get('TRACE', {}).get('observations', [])):
            pass

        if not failed_checks:
            failed_checks = ["unspecified failure"]
            recovery_options = ["Examine logs and metrics for anomalies"]

        fail_reason = ", ".join(failed_checks)
        recovery_step = "See recovery_options for next actions"
        
        # Добавить в контракт
        contract['FAIL_DIAGNOSIS'] = {
            'reason': fail_reason,
            'failed_checks': failed_checks,
            'next_step': recovery_step,
            'recovery_options': recovery_options
        }
        
        # Выписать в файл
        lines.append("\nFAIL_DIAGNOSIS:")
        lines.append(f"  reason: {fail_reason}")
        lines.append(f"  failed_checks: {failed_checks}")
        lines.append(f"  next_step: {recovery_step}")
        lines.append("\nRECOVERY_OPTIONS:")
        for i, opt in enumerate(recovery_options, 1):
            lines.append(f"  {i}. {opt}")
    
    CONTRACT_FILE.write_text("\n".join(lines))
    # Metrics JSON
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))



def cmd_measure(args: argparse.Namespace) -> None:
    """Handle the ``measure`` subcommand."""
    text = sys.stdin.read()
    use_sqlite = getattr(args, "sqlite", False)
    state = load_state(use_sqlite=use_sqlite)
    state.current_cycle += 1
    metrics, contract = measure_text(text, state)
    write_outputs(contract, metrics)
    save_state(state, use_sqlite=use_sqlite)
    print(f"Measurement complete. Contract written to {CONTRACT_FILE} and metrics to {METRICS_FILE}.")



def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="NECHTO runtime CLI")
    subparsers = parser.add_subparsers(dest="command")
    measure_parser = subparsers.add_parser("measure", help="measure text from STDIN and produce outputs")
    measure_parser.add_argument("--sqlite", action="store_true", help="Use SQLite for persistent state storage")
    measure_parser.set_defaults(func=cmd_measure)
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

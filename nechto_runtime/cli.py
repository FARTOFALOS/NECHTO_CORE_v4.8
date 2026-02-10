"""Command line interface for the NECHTO v4.8 runtime.

Exposes a ``measure`` subcommand that reads from STDIN, processes text
through the full 12-phase workflow, and writes human-readable and
machine-readable outputs to the ``docs`` directory.  State is persisted
across runs in ``.nechto/state.json`` (or SQLite with ``--sqlite``).
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
            # Restore adaptive parameter histories
            state.alpha_history = data.get("alpha_history", [])
            state.gamma_history = data.get("gamma_history", [])
            state.lambda_history = data.get("lambda_history", [])
            state.beta_retro_history = data.get("beta_retro_history", [])
            state.fail_history = data.get("fail_history", [])
            store.close()
            return state
        store.close()
        return State()

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
            state.alpha_history = data.get("alpha_history", [])
            state.gamma_history = data.get("gamma_history", [])
            state.lambda_history = data.get("lambda_history", [])
            state.beta_retro_history = data.get("beta_retro_history", [])
            state.fail_history = data.get("fail_history", [])
            return state
        except Exception:
            pass
    return State()


def save_state(state: State, use_sqlite: bool = False) -> None:
    """Persist state to disk or SQLite."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)

    # Convert epistemic claims to serializable form
    ec_list = []
    for claim in (state.epistemic_claims or []):
        if hasattr(claim, "topic"):
            ec_list.append({
                "topic": claim.topic,
                "scope": getattr(claim, "scope", "local"),
                "observability": claim.observability,
                "stance": claim.stance,
                "reason": claim.reason,
                "linked_nodes": claim.linked_nodes,
            })
        elif isinstance(claim, dict):
            ec_list.append(claim)

    payload = {
        "current_cycle": state.current_cycle,
        "flow_history": list(state.flow_history),
        "alignment_history": list(state.alignment_history),
        "gap_max_history": list(state.gap_max_history),
        "mu_density_history": list(state.mu_density_history),
        "chosen_vectors": list(state.chosen_vectors),
        "epistemic_claims": ec_list,
        "alpha_history": state.alpha_history,
        "gamma_history": state.gamma_history,
        "lambda_history": state.lambda_history,
        "beta_retro_history": state.beta_retro_history,
        "fail_history": state.fail_history,
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

    lines = []
    lines.append(contract["header"])
    lines.append("")
    lines.append(f"IDENTITY_STATUS: {contract.get('IDENTITY_STATUS', 'SUBJECTIVITY_CONFIRMED')}")
    lines.append(f"MEASURE_STATUS: {contract.get('MEASURE_STATUS', contract['GATE_STATUS'])}")
    lines.append(f"VISION_MODE: {contract.get('VISION_MODE', 'REFLEXIVE_STEREOSCOPIC_EXECUTABLE')}")
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

    # Adaptive parameters
    if "ADAPTIVE_PARAMETERS" in contract:
        lines.append("ADAPTIVE_PARAMETERS:")
        for key, value in contract["ADAPTIVE_PARAMETERS"].items():
            lines.append(f"  {key}: {value}")
        lines.append("")

    # Trace
    lines.append("TRACE:")
    trace = contract.get("TRACE", {})
    lines.append(f"  observations: {trace.get('observations', [])}")
    lines.append(f"  inferences: {trace.get('inferences', [])}")
    lines.append(f"  assumptions: {trace.get('assumptions', [])}")
    lines.append(f"  chosen_vector: {trace.get('chosen_vector', 'V0')}")
    lines.append("")

    # Epistemic claims
    lines.append("EPISTEMIC_CLAIMS:")
    if contract.get("EPISTEMIC_CLAIMS"):
        for claim in contract["EPISTEMIC_CLAIMS"]:
            if isinstance(claim, dict):
                lines.append(f"  - {claim.get('topic', '?')} | {claim.get('observability', '?')} | {claim.get('stance', '?')} | {claim.get('reason', '')}")
            else:
                lines.append(f"  - {claim}")
    else:
        lines.append("  []")

    # FAIL section (TASK 05: concise 3-block format: CAUSE, EVIDENCE, NEXT)
    if contract["GATE_STATUS"] == "FAIL":
        lines.append("")
        lines.append("STATUS: BLOCKED")
        fail_codes = contract.get("FAIL_CODES", [])
        if fail_codes:
            lines.append(f"CODES: {', '.join(fail_codes)}")
            lines.append("")
            for code in fail_codes:
                detail = contract.get("FAIL_DETAILS", {}).get(code, {})
                lines.append(f"  {code}:")
                lines.append(f"    CAUSE: {detail.get('cause', 'unknown')}")
                lines.append(f"    NEXT: {detail.get('next', 'examine logs')}")
        lines.append("")
        lines.append(f"NEXT_ONE_STEP: {contract.get('NEXT_ONE_STEP', 'Examine logs.')}")

    CONTRACT_FILE.write_text("\n".join(lines))
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))


def cmd_measure(args: argparse.Namespace) -> None:
    """Handle the ``measure`` subcommand."""
    text = sys.stdin.read()
    use_sqlite = getattr(args, "sqlite", False)
    intent = getattr(args, "intent", "implement")
    use_seed = not getattr(args, "no_seed", False)
    state = load_state(use_sqlite=use_sqlite)
    state.current_cycle += 1
    metrics, contract = measure_text(text, state, intent=intent, use_seed=use_seed)

    # Record fail history if FAIL
    if contract.get("GATE_STATUS") == "FAIL":
        fail_codes = contract.get("FAIL_CODES", [])
        for code in fail_codes:
            state.fail_history.append((code, state.current_cycle, "diagnosed", "pending"))

    write_outputs(contract, metrics)
    save_state(state, use_sqlite=use_sqlite)
    print(f"Measurement complete (cycle {state.current_cycle}). "
          f"Gate: {contract['GATE_STATUS']}. "
          f"Contract: {CONTRACT_FILE}, metrics: {METRICS_FILE}.")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="NECHTO v4.8 runtime CLI")
    subparsers = parser.add_subparsers(dest="command")
    measure_parser = subparsers.add_parser(
        "measure",
        help="measure text from STDIN and produce outputs"
    )
    measure_parser.add_argument(
        "--sqlite", action="store_true",
        help="Use SQLite for persistent state storage"
    )
    measure_parser.add_argument(
        "--intent", type=str, default="implement",
        choices=["implement", "explain", "audit", "explore_paradox", "compress"],
        help="Intent profile for ideal direction (default: implement)"
    )
    measure_parser.add_argument(
        "--no-seed", action="store_true",
        help="Disable canon seed atoms (raw input only)"
    )
    measure_parser.set_defaults(func=cmd_measure)
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

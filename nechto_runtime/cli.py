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

from .types import State
from .metrics import measure_text


STATE_DIR = Path(".nechto")
STATE_FILE = STATE_DIR / "state.json"
DOCS_DIR = Path("docs")
CONTRACT_FILE = DOCS_DIR / "latest_contract.md"
METRICS_FILE = DOCS_DIR / "latest_metrics.json"


def load_state() -> State:
    """Load persistent state from disk or return a new state."""
    if STATE_FILE.exists():
        try:
            data = json.loads(STATE_FILE.read_text())
            state = State()
            # Minimal restoration: current_cycle and flow_history
            state.current_cycle = data.get("current_cycle", 0)
            state.flow_history.extend(data.get("flow_history", []))
            return state
        except Exception:
            pass
    return State()


def save_state(state: State) -> None:
    """Persist state to disk."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "current_cycle": state.current_cycle,
        "flow_history": list(state.flow_history),
    }
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
    CONTRACT_FILE.write_text("\n".join(lines))
    # Metrics JSON
    METRICS_FILE.write_text(json.dumps(metrics, indent=2))


def cmd_measure(args: argparse.Namespace) -> None:
    """Handle the ``measure`` subcommand."""
    text = sys.stdin.read()
    state = load_state()
    state.current_cycle += 1
    metrics, contract = measure_text(text, state)
    write_outputs(contract, metrics)
    save_state(state)
    print(f"Measurement complete. Contract written to {CONTRACT_FILE} and metrics to {METRICS_FILE}.")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="NECHTO runtime CLI")
    subparsers = parser.add_subparsers(dest="command")
    measure_parser = subparsers.add_parser("measure", help="measure text from STDIN and produce outputs")
    measure_parser.set_defaults(func=cmd_measure)
    args = parser.parse_args(argv)
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

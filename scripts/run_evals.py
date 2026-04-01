#!/usr/bin/env python3
"""
deepthink skill evaluation runner.
Run: python scripts/run_evals.py [--iter N]
"""

import json
import subprocess
import sys
from pathlib import Path

SKILL_PATH = Path(__file__).parent.parent
SNAPSHOT_PATH = SKILL_PATH.parent / "deepthink-workspace" / "skill-snapshot"
WORKSPACE = SKILL_PATH.parent / "deepthink-workspace"


def load_evals():
    with open(SKILL_PATH / "evals" / "evals.json") as f:
        return json.load(f)


def run_agent(skill_path: Path, prompt: str, output_dir: Path, agent_id: str):
    output_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        "claude", "-A", str(skill_path),
        "-p",
        f'Execute: read SKILL.md, then answer: "{prompt}". Save output to {output_dir}/output.txt'
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(WORKSPACE.parent),
        timeout=300
    )
    print(f"  [{agent_id}] exit={result.returncode} stdout={len(result.stdout)} chars")
    return result.returncode == 0


def main():
    evals = load_evals()
    iter_num = 1
    if "--iter" in sys.argv:
        idx = sys.argv.index("--iter") + 1
        iter_num = int(sys.argv[idx])

    iter_dir = WORKSPACE / f"iteration-{iter_num}"

    print(f"Running {len(evals['evals'])} evals (iteration {iter_num})")

    for eval_item in evals["evals"]:
        eid = eval_item["id"]
        prompt = eval_item["prompt"]
        etype = eval_item["type"]

        # with_skill
        d = iter_dir / f"eval-{eid}-{etype}" / "with_skill" / "outputs"
        print(f"Running eval-{eid} with_skill...")
        run_agent(SKILL_PATH, prompt, d, f"eval-{eid}-with")

        # old_skill (snapshot)
        d = iter_dir / f"eval-{eid}-{etype}" / "old_skill" / "outputs"
        print(f"Running eval-{eid} old_skill...")
        run_agent(SNAPSHOT_PATH, prompt, d, f"eval-{eid}-old")

    print(f"\nDone. Results in {iter_dir}")
    print("To grade: spawn subagents to read output.txt and check assertions from evals.json")


if __name__ == "__main__":
    main()

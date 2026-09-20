#!/usr/bin/env python3
"""deepthink skill evaluation runner。

Usage:
    python scripts/run_evals.py              # 跑 12 条 evals (claude_code agent)
    python scripts/run_evals.py --iter 0     # 跑第 N 轮(baseline 用 0)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
EVALS_FILE = PROJECT_ROOT / "evals" / "evals.json"


def load_evals() -> dict:
    with open(EVALS_FILE, encoding="utf-8") as f:
        return json.load(f)


def run_agent(skill_path: Path, prompt: str, output_dir: Path, agent_id: str, timeout: int = 300) -> bool:
    """通过 Claude Code CLI 跑单条 eval。"""
    if not shutil.which("claude"):
        print(f"  [{agent_id}] claude CLI not found, skipping")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    trigger = "deepthink: "  # 与 evals.json trigger.prefix 一致
    full_prompt = f"{trigger}{prompt}" if trigger else prompt
    cmd = [
        "claude", "-A", str(skill_path),
        "-p",
        f'Execute: read SKILL.md, then answer: "{full_prompt}". Save output to {output_dir}/output.txt',
    ]
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=str(skill_path.parent),
        timeout=timeout,
    )
    print(f"  [{agent_id}] exit={result.returncode} stdout={len(result.stdout)} chars")
    return result.returncode == 0


def main() -> int:
    iter_num = 1
    if "--iter" in sys.argv:
        idx = sys.argv.index("--iter") + 1
        iter_num = int(sys.argv[idx])

    cfg = load_evals()
    skill_path = PROJECT_ROOT
    workspace = PROJECT_ROOT.parent / "deepthink-workspace"
    iter_dir = workspace / f"iteration-{iter_num}"

    print(f"Running {len(cfg['evals'])} evals (iteration {iter_num})")

    for eval_item in cfg["evals"]:
        eid = eval_item["id"]
        prompt = eval_item["prompt"]
        etype = eval_item["type"]
        d = iter_dir / f"eval-{eid}-{etype}" / "with_skill" / "outputs"
        print(f"Running eval-{eid} ({etype})...")
        run_agent(skill_path, prompt, d, f"eval-{eid}-claude_code")

    print(f"\nDone. Results in {iter_dir}")
    print("To grade: spawn subagents to read output.txt and check assertions from evals.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
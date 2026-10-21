#!/usr/bin/env python3
"""deepthink skill evaluation runner。

Usage:
    python scripts/run_evals.py              # 跑 12 条 evals (claude_code agent)
    python scripts/run_evals.py --iter 0     # 跑第 N 轮(baseline 用 0)
    python scripts/run_evals.py --only 4,5   # 只跑指定 id(迭代修复时用)
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


def run_agent(skill_path: Path, prompt: str, output_dir: Path, agent_id: str, trigger: str, timeout: int = 900) -> bool:
    """通过 Claude Code CLI 跑单条 eval。"""
    if not shutil.which("claude"):
        print(f"  [{agent_id}] claude CLI not found, skipping")
        return False

    output_dir.mkdir(parents=True, exist_ok=True)
    full_prompt = f"{trigger}{prompt}" if trigger else prompt
    # 注意: claude CLI 没有 -A 选项(旧写法直接报 unknown option),授权目录用 --add-dir;
    # skill 目录和输出目录都要加,否则 headless 模式下读 SKILL.md / 写 output.txt 会被拒。
    cmd = [
        "claude",
        "--add-dir", str(skill_path),
        "--add-dir", str(output_dir),
        "-p",
        f'Execute: read SKILL.md, then answer: "{full_prompt}". Save output to {output_dir}/output.txt',
    ]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(skill_path.parent),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        # deep 模式跑满完整协议(ToT/验证/迭代)可能远超 5 分钟;
        # 超时只标记该条失败,不能让整个批次崩掉
        (output_dir / "agent.log").write_text(
            f"TIMEOUT after {timeout}s\n", encoding="utf-8"
        )
        print(f"  [{agent_id}] TIMEOUT after {timeout}s")
        return False

    # 落盘 agent 的原始输出,否则失败时没有任何诊断线索
    (output_dir / "agent.log").write_text(
        f"exit={result.returncode}\n\n--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}\n",
        encoding="utf-8",
    )

    print(f"  [{agent_id}] exit={result.returncode} stdout={len(result.stdout)} chars")
    return result.returncode == 0


def main() -> int:
    iter_num = 1
    if "--iter" in sys.argv:
        idx = sys.argv.index("--iter") + 1
        iter_num = int(sys.argv[idx])

    only = None
    if "--only" in sys.argv:
        idx = sys.argv.index("--only") + 1
        only = {int(x) for x in sys.argv[idx].split(",")}

    cfg = load_evals()
    trigger = cfg.get("trigger", {}).get("prefix", "")  # 触发前缀以 evals.json 为准,不在代码里硬编码
    skill_path = PROJECT_ROOT
    workspace = PROJECT_ROOT.parent / "deepthink-workspace"
    iter_dir = workspace / f"iteration-{iter_num}"

    evals = [e for e in cfg["evals"] if only is None or e["id"] in only]
    print(f"Running {len(evals)} evals (iteration {iter_num})")

    completed = 0
    for eval_item in evals:
        eid = eval_item["id"]
        prompt = eval_item["prompt"]
        etype = eval_item["type"]
        d = iter_dir / f"eval-{eid}-{etype}" / "with_skill" / "outputs"
        print(f"Running eval-{eid} ({etype})...")
        ok = run_agent(
            skill_path, prompt, d, f"eval-{eid}-claude_code", trigger,
            timeout=300 if etype == "quick" else 900,  # deep 模式需要更长上限
        )
        completed += ok

    print(f"\nDone: {completed}/{len(evals)} evals completed. Results in {iter_dir}")
    print(f"To grade: python scripts/grade_evals.py --iter {iter_num}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
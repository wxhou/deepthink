#!/usr/bin/env python3
"""deepthink skill evaluation runner。

Usage:
    python scripts/run_evals.py                # 跑全部 evals (claude_code agent, 串行)
    python scripts/run_evals.py --iter 0       # 跑第 N 轮(baseline 用 0)
    python scripts/run_evals.py --only 4,5     # 只跑指定 id(迭代修复时用)
    python scripts/run_evals.py --jobs 3       # 并行跑(注意 API 限流)
"""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
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

    started = time.monotonic()
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=str(skill_path.parent),
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        duration = time.monotonic() - started
        # deep 模式跑满完整协议(ToT/验证/迭代)可能远超 5 分钟;
        # 超时只标记该条失败,不能让整个批次崩掉
        (output_dir / "agent.log").write_text(
            f"TIMEOUT after {timeout}s (ran {duration:.0f}s)\n", encoding="utf-8"
        )
        print(f"  [{agent_id}] TIMEOUT after {timeout}s")
        return False

    duration = time.monotonic() - started
    output_file = output_dir / "output.txt"
    # 落盘 agent 的原始输出和耗时,否则失败时没有任何诊断线索
    (output_dir / "agent.log").write_text(
        f"duration={duration:.1f}s exit={result.returncode} "
        f"output.txt={'yes' if output_file.exists() else 'no'}\n"
        f"\n--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}\n",
        encoding="utf-8",
    )

    print(f"  [{agent_id}] exit={result.returncode} {duration:.0f}s stdout={len(result.stdout)} chars")
    if result.returncode == 0 and not output_file.exists():
        print(f"  [{agent_id}] WARN: exit 0 but no output.txt (saving may have been denied)")
    return result.returncode == 0


def run_one(eval_item: dict, iter_dir: Path, trigger: str, skill_path: Path) -> bool:
    eid = eval_item["id"]
    etype = eval_item["type"]
    d = iter_dir / f"eval-{eid}-{etype}" / "with_skill" / "outputs"
    print(f"Running eval-{eid} ({etype})...")
    effective_trigger = eval_item.get("trigger") or trigger  # 每条可覆盖触发形式(/deepthink、@deepthink)
    return run_agent(
        skill_path, eval_item["prompt"], d, f"eval-{eid}-claude_code", effective_trigger,
        timeout=300 if etype == "quick" else 900,  # deep 模式需要更长上限
    )


def main() -> int:
    args = sys.argv[1:]

    iter_num = 1
    if "--iter" in args:
        iter_num = int(args[args.index("--iter") + 1])

    jobs = 1
    if "--jobs" in args:
        jobs = max(1, int(args[args.index("--jobs") + 1]))

    only = None
    if "--only" in args:
        only = {int(x) for x in args[args.index("--only") + 1].split(",")}

    cfg = load_evals()
    trigger = cfg.get("trigger", {}).get("prefix", "")  # 触发前缀以 evals.json 为准,不在代码里硬编码
    skill_path = PROJECT_ROOT
    iter_dir = PROJECT_ROOT.parent / "deepthink-workspace" / f"iteration-{iter_num}"

    evals = [e for e in cfg["evals"] if only is None or e["id"] in only]
    print(f"Running {len(evals)} evals (iteration {iter_num}, jobs={jobs})")

    started = time.monotonic()
    if jobs == 1:
        results = [run_one(e, iter_dir, trigger, skill_path) for e in evals]
    else:
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            futures = [pool.submit(run_one, e, iter_dir, trigger, skill_path) for e in evals]
            results = [f.result() for f in futures]
    wall = time.monotonic() - started

    print(f"\nDone: {sum(results)}/{len(evals)} evals completed in {wall:.0f}s. Results in {iter_dir}")
    print(f"To grade: python scripts/grade_evals.py --iter {iter_num}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

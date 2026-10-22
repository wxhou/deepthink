#!/usr/bin/env python3
"""deepthink eval 自动判分 —— 按 evals.json 里的断言检查输出。

断言语义(evals.json 每条 eval 的 "assertions" 字段):
  must_include_any:        每组内任一字符串出现即满足,所有组都必须满足
  must_not_include_any:    每组内任一字符串出现即判失败
  must_match_any_regex:    每组内任一正则匹配即满足(re.search),所有组都必须满足
  must_include_at_least:   {"count": N, "groups": [...]},至少 N 组命中

目录布局兼容:
  iteration-N/eval-{id}-{type}/with_skill/run-{k}/outputs/output.txt  (--repeat)
  iteration-N/eval-{id}-{type}/with_skill/outputs/output.txt          (旧布局,视为 run 1)

Usage:
    python scripts/grade_evals.py --iter 1             # 判 iteration-1 (run 1)
    python scripts/grade_evals.py --dir /some/dir      # 判任意结果目录
    python scripts/grade_evals.py --iter 1 --only 4,5  # 只判指定 id
    python scripts/grade_evals.py --iter 1 --diff 0    # 与另一个迭代对比
    python scripts/grade_evals.py --iter 1 --run 2     # 判第 2 次运行
    python scripts/grade_evals.py --iter 1 --all-runs  # 判所有运行,报告通过率
"""
from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
EVALS_FILE = PROJECT_ROOT / "evals" / "evals.json"
WORKSPACE = PROJECT_ROOT.parent / "deepthink-workspace"


def check(text: str, assertions: dict) -> list[str]:
    """返回失败原因列表,空列表 = 通过。"""
    failures = []
    for group in assertions.get("must_include_any", []):
        if not any(s in text for s in group):
            failures.append(f"missing any of {group}")
    for group in assertions.get("must_not_include_any", []):
        hit = next((s for s in group if s in text), None)
        if hit:
            failures.append(f"forbidden string present: {hit!r}")
    for group in assertions.get("must_match_any_regex", []):
        if not any(re.search(pattern, text) for pattern in group):
            failures.append(f"no regex matched: {group}")
    at_least = assertions.get("must_include_at_least")
    if at_least:
        need = int(at_least.get("count", 1))
        hit = sum(
            1 for group in at_least.get("groups", [])
            if any(s in text for s in group)
        )
        if hit < need:
            failures.append(f"only {hit}/{need} alternative groups present")
    return failures


def resolve_target(value: str) -> Path:
    """接受迭代号(0/1/2)或包含 / 的目录路径。"""
    if "/" in value:
        return Path(value).resolve()
    return WORKSPACE / f"iteration-{value}"


def output_file(results_dir: Path, eid: int, etype: str, run: int = 1) -> Path:
    base = results_dir / f"eval-{eid}-{etype}" / "with_skill"
    run_path = base / f"run-{run}" / "outputs" / "output.txt"
    if run_path.exists():
        return run_path
    legacy = base / "outputs" / "output.txt"
    if run == 1 and legacy.exists():
        return legacy
    return run_path


def available_runs(results_dir: Path, eid: int, etype: str) -> list[int]:
    base = results_dir / f"eval-{eid}-{etype}" / "with_skill"
    runs = sorted(
        int(p.name.split("-", 1)[1])
        for p in base.glob("run-*")
        if p.is_dir() and p.name.split("-", 1)[1].isdigit()
    )
    if not runs and (base / "outputs" / "output.txt").exists():
        runs = [1]
    return runs


def grade_one(item: dict, results_dir: Path, run: int = 1) -> tuple[bool, list[str]]:
    eid, etype = item["id"], item["type"]
    out = output_file(results_dir, eid, etype, run)
    if not out.exists():
        return False, [f"no output.txt at {out}"]
    failures = check(out.read_text(encoding="utf-8", errors="replace"), item.get("assertions", {}))
    return not failures, failures


def write_grades(results_dir: Path, payload: dict) -> None:
    try:
        results_dir.mkdir(parents=True, exist_ok=True)
        (results_dir / "grades.json").write_text(
            json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    except OSError as exc:
        print(f"WARN: could not write grades.json: {exc}")


def main() -> int:
    args = sys.argv[1:]

    if "--dir" in args:
        results_dir = Path(args[args.index("--dir") + 1]).resolve()
    else:
        iter_num = 1
        if "--iter" in args:
            iter_num = int(args[args.index("--iter") + 1])
        results_dir = WORKSPACE / f"iteration-{iter_num}"

    only = None
    if "--only" in args:
        only = {int(x) for x in args[args.index("--only") + 1].split(",")}

    run = 1
    if "--run" in args:
        run = int(args[args.index("--run") + 1])

    all_runs = "--all-runs" in args

    cfg = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    items = [e for e in cfg["evals"] if only is None or e["id"] in only]

    diff_dir = None
    baseline = None
    if "--diff" in args:
        diff_dir = resolve_target(args[args.index("--diff") + 1])
        baseline = {e["id"]: grade_one(e, diff_dir, run) for e in items}

    passed = 0
    fixed = regressed = 0
    payload_evals = []

    for item in items:
        eid, etype = item["id"], item["type"]
        if all_runs:
            runs = available_runs(results_dir, eid, etype) or [run]
            run_results = []
            for k in runs:
                ok, failures = grade_one(item, results_dir, k)
                run_results.append({"run": k, "passed": ok, "failures": failures})
            ok = all(r["passed"] for r in run_results)
            failed_runs = [r for r in run_results if not r["passed"]]
            note = f" ({len(run_results) - len(failed_runs)}/{len(run_results)} runs)"
            if ok:
                passed += 1
                print(f"eval-{eid}-{etype}: PASS{note}")
            else:
                reasons = "; ".join(
                    f"run-{r['run']}: {'; '.join(r['failures'])}" for r in failed_runs
                )
                print(f"eval-{eid}-{etype}: FAIL{note} ({reasons})")
            payload_evals.append({
                "id": eid, "type": etype, "passed": ok, "runs": run_results,
            })
            continue

        ok, failures = grade_one(item, results_dir, run)
        note = ""
        if baseline is not None:
            was_ok = baseline[eid][0]
            if ok and not was_ok:
                note = f" (fixed vs {diff_dir.name})"
                fixed += 1
            elif not ok and was_ok:
                note = f" (REGRESSED vs {diff_dir.name})"
                regressed += 1
        if ok:
            passed += 1
            print(f"eval-{eid}-{etype}: PASS{note}")
        else:
            print(f"eval-{eid}-{etype}: FAIL ({'; '.join(failures)}){note}")
        payload_evals.append({
            "id": eid, "type": etype, "passed": ok,
            "runs": [{"run": run, "passed": ok, "failures": failures}],
        })

    summary = f"\n{results_dir.name}: {passed}/{len(items)} passed"
    if baseline is not None:
        summary += f" | vs {diff_dir.name}: {fixed} fixed, {regressed} regressed"
    print(summary)

    write_grades(results_dir, {
        "results_dir": str(results_dir),
        "graded_at": datetime.now(timezone.utc).isoformat(),
        "mode": "all-runs" if all_runs else f"run-{run}",
        "evals": payload_evals,
        "summary": {"passed": passed, "total": len(items)},
    })

    return 0 if passed == len(items) else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""deepthink eval 自动判分 —— 按 evals.json 里的结构断言检查输出。

断言语义(evals.json 每条 eval 的 "assertions" 字段):
  must_include_any:     每组内任一字符串出现即满足,所有组都必须满足
  must_not_include_any: 每组内任一字符串出现即判失败

Usage:
    python scripts/grade_evals.py --iter 1            # 判 iteration-1
    python scripts/grade_evals.py --dir /some/dir     # 判任意含 eval-*/with_skill/outputs/ 的目录
    python scripts/grade_evals.py --iter 1 --only 4,5 # 只判指定 id
    python scripts/grade_evals.py --iter 1 --diff 0   # 与 iteration-0 对比(是否修复/退化)
"""
from __future__ import annotations

import json
import sys
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
    return failures


def resolve_target(value: str) -> Path:
    """接受迭代号(0/1/2)或包含 / 的目录路径。"""
    if "/" in value:
        return Path(value).resolve()
    return WORKSPACE / f"iteration-{value}"


def grade_dir(results_dir: Path, items: list[dict]) -> dict[int, tuple[bool, list[str]]]:
    results: dict[int, tuple[bool, list[str]]] = {}
    for item in items:
        eid, etype = item["id"], item["type"]
        out = results_dir / f"eval-{eid}-{etype}" / "with_skill" / "outputs" / "output.txt"
        if not out.exists():
            results[eid] = (False, [f"no output.txt at {out}"])
            continue
        failures = check(out.read_text(encoding="utf-8", errors="replace"), item.get("assertions", {}))
        results[eid] = (not failures, failures)
    return results


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

    cfg = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    items = [e for e in cfg["evals"] if only is None or e["id"] in only]

    results = grade_dir(results_dir, items)

    diff_dir = None
    baseline = None
    if "--diff" in args:
        diff_dir = resolve_target(args[args.index("--diff") + 1])
        baseline = grade_dir(diff_dir, items)

    passed = fixed = regressed = 0
    for item in items:
        eid, etype = item["id"], item["type"]
        ok, failures = results[eid]
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

    summary = f"\n{results_dir.name}: {passed}/{len(items)} passed"
    if baseline is not None:
        summary += f" | vs {diff_dir.name}: {fixed} fixed, {regressed} regressed"
    print(summary)
    return 0 if passed == len(items) else 1


if __name__ == "__main__":
    sys.exit(main())

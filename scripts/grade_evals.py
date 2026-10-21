#!/usr/bin/env python3
"""deepthink eval 自动判分 —— 按 evals.json 里的结构断言检查输出。

断言语义(evals.json 每条 eval 的 "assertions" 字段):
  must_include_any:     每组内任一字符串出现即满足,所有组都必须满足
  must_not_include_any: 每组内任一字符串出现即判失败

Usage:
    python scripts/grade_evals.py --iter 1            # 判 iteration-1
    python scripts/grade_evals.py --dir /some/dir     # 判任意含 eval-*/with_skill/outputs/ 的目录
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent
EVALS_FILE = PROJECT_ROOT / "evals" / "evals.json"


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


def main() -> int:
    args = sys.argv[1:]
    if "--dir" in args:
        results_dir = Path(args[args.index("--dir") + 1]).resolve()
    else:
        iter_num = 1
        if "--iter" in args:
            iter_num = int(args[args.index("--iter") + 1])
        results_dir = PROJECT_ROOT.parent / "deepthink-workspace" / f"iteration-{iter_num}"

    cfg = json.loads(EVALS_FILE.read_text(encoding="utf-8"))
    total = passed = 0
    for item in cfg["evals"]:
        eid, etype = item["id"], item["type"]
        total += 1
        out = results_dir / f"eval-{eid}-{etype}" / "with_skill" / "outputs" / "output.txt"
        if not out.exists():
            print(f"eval-{eid}-{etype}: FAIL (no output.txt at {out})")
            continue
        failures = check(out.read_text(encoding="utf-8", errors="replace"), item.get("assertions", {}))
        if failures:
            print(f"eval-{eid}-{etype}: FAIL ({'; '.join(failures)})")
        else:
            passed += 1
            print(f"eval-{eid}-{etype}: PASS")

    print(f"\n{results_dir.name}: {passed}/{total} passed")
    return 0 if passed == total else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""deepthink 仓库一致性检查 —— 零 API 成本,供 CI 与本地使用。

检查项:
  1. 版本号单一来源: SKILL.md frontmatter 为权威,evals.json / README / site 必须一致
  2. SKILL.md 引用的协议文件必须存在
  3. evals.json 结构合法(id 唯一、必需字段齐全、assertion 键已知)
  4. 无失效路径残留(references/{en,zh}.md、adapters/)

Usage:
    python scripts/check_consistency.py
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "SKILL.md"
EVALS = ROOT / "evals" / "evals.json"
README = ROOT / "README.md"
SITE = ROOT / "site" / "index.html"
CLAUDE_MD = ROOT / "CLAUDE.md"

PROTOCOL_FILES = ["core/protocol.en.md", "core/protocol.zh.md"]
KNOWN_ASSERTION_KEYS = {"must_include_any", "must_not_include_any"}
REQUIRED_EVAL_KEYS = {"id", "prompt", "type", "assertions"}
STALE_REFS = ["references/en.md", "references/zh.md", "adapters/"]


def version_from_skill() -> str:
    m = re.search(r"^version:\s*(\S+)\s*$", SKILL.read_text(encoding="utf-8"), re.MULTILINE)
    if not m:
        raise SystemExit("SKILL.md: missing 'version:' in frontmatter")
    return m.group(1)


def check_versions(errors: list[str]) -> None:
    v = version_from_skill()
    cfg = json.loads(EVALS.read_text(encoding="utf-8"))
    if cfg.get("version") != v:
        errors.append(f"evals/evals.json version={cfg.get('version')!r}, expected {v!r}")
    if v not in README.read_text(encoding="utf-8"):
        errors.append(f"README.md does not mention version {v}")
    if f"v{v}" not in SITE.read_text(encoding="utf-8"):
        errors.append(f"site/index.html does not mention v{v}")


def check_paths(errors: list[str]) -> None:
    skill = SKILL.read_text(encoding="utf-8")
    for p in PROTOCOL_FILES:
        if p not in skill:
            errors.append(f"SKILL.md does not reference {p}")
        if not (ROOT / p).is_file():
            errors.append(f"missing file: {p}")


def check_evals(errors: list[str]) -> None:
    cfg = json.loads(EVALS.read_text(encoding="utf-8"))
    evals = cfg.get("evals", [])
    ids = [e.get("id") for e in evals]
    dupes = sorted({i for i in ids if ids.count(i) > 1})
    if dupes:
        errors.append(f"duplicate eval ids: {dupes}")
    for e in evals:
        missing = REQUIRED_EVAL_KEYS - e.keys()
        if missing:
            errors.append(f"eval {e.get('id')}: missing keys {sorted(missing)}")
        unknown = set(e.get("assertions", {})) - KNOWN_ASSERTION_KEYS
        if unknown:
            errors.append(f"eval {e.get('id')}: unknown assertion keys {sorted(unknown)}")


def check_stale_refs(errors: list[str]) -> None:
    files = [SKILL, README, CLAUDE_MD, *(ROOT / p for p in PROTOCOL_FILES)]
    for f in files:
        text = f.read_text(encoding="utf-8")
        for s in STALE_REFS:
            if s in text:
                errors.append(f"{f.relative_to(ROOT)} contains stale reference {s!r}")


def main() -> int:
    errors: list[str] = []
    check_versions(errors)
    check_paths(errors)
    check_evals(errors)
    check_stale_refs(errors)
    if errors:
        print("consistency check FAILED:")
        for e in errors:
            print(f"  - {e}")
        return 1
    print(f"consistency check OK (version {version_from_skill()})")
    return 0


if __name__ == "__main__":
    sys.exit(main())

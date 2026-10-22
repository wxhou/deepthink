#!/usr/bin/env python3
"""grade_evals 自测 —— 在 CI 中运行,防止判分逻辑退化。

Usage:
    python scripts/test_grade_evals.py
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from grade_evals import check  # noqa: E402

GRADER = SCRIPT_DIR / "grade_evals.py"


def write_output(root: Path, eid: int, etype: str, text: str) -> None:
    d = root / f"eval-{eid}-{etype}" / "with_skill" / "outputs"
    d.mkdir(parents=True, exist_ok=True)
    (d / "output.txt").write_text(text, encoding="utf-8")


class CheckTest(unittest.TestCase):
    def test_include_group_any_alternative(self):
        assertions = {"must_include_any": [["### 关键假设", "### Key Assumptions"]]}
        self.assertEqual(check("### Key Assumptions\n- x", assertions), [])

    def test_include_missing(self):
        self.assertTrue(check("plain answer", {"must_include_any": [["### 关键假设"]]}))

    def test_forbidden_present(self):
        self.assertTrue(check("## 🤔 DeepThink 分析", {"must_not_include_any": [["🤔 DeepThink"]]}))

    def test_prose_mention_is_not_template(self):
        # 断言锚定到标题后,正文里提到"关键假设"不应误判
        assertions = {"must_not_include_any": [["### 关键假设"]]}
        self.assertEqual(check("这里不需要列关键假设。", assertions), [])


class CliTest(unittest.TestCase):
    def run_grader(self, root: Path):
        return subprocess.run(
            [sys.executable, str(GRADER), "--dir", str(root), "--only", "0,1"],
            capture_output=True,
            text=True,
        )

    def test_pass_and_fail_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_output(root, 0, "complex", "## 🤔 DeepThink 分析\n### 关键假设\n### 置信度: High\n")
            write_output(root, 1, "quick", "今天是周五。\n")

            r = self.run_grader(root)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            self.assertIn("2/2 passed", r.stdout)

            write_output(root, 1, "quick", "## 🤔 DeepThink 分析\n")
            r = self.run_grader(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("eval-1-quick: FAIL", r.stdout)

    def test_missing_output_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_output(root, 0, "complex", "## 🤔 DeepThink 分析\n### 关键假设\n### 置信度: High\n")
            # eval-1 没有 output.txt
            r = self.run_grader(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("no output.txt", r.stdout)


if __name__ == "__main__":
    unittest.main()

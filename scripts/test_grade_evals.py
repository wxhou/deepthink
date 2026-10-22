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

# eval-0 现在包含实质断言(部署/性能/运维/团队),夹具必须覆盖
COMPLEX_OK = "## 🤔 DeepThink 分析\n### 关键假设\n### 置信度: High\n部署、性能、运维、团队都要考虑。\n"


def write_output(root: Path, eid: int, etype: str, text: str, run: int | None = None) -> None:
    base = root / f"eval-{eid}-{etype}" / "with_skill"
    d = (base / f"run-{run}" / "outputs") if run else (base / "outputs")
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

    def test_regex_matches_spaced_variant(self):
        assertions = {"must_match_any_regex": [["B\\+\\s*树", "B\\+\\s*[Tt]ree"]]}
        self.assertEqual(check("核心结构是 B+ 树", assertions), [])
        self.assertEqual(check("core structure is a B+ Tree", assertions), [])
        self.assertTrue(check("a plain B tree", assertions))

    def test_at_least_count(self):
        assertions = {
            "must_include_at_least": {
                "count": 3,
                "groups": [["CDN"], ["缓存"], ["分片"], ["队列"]],
            }
        }
        self.assertEqual(check("CDN、缓存、队列都要有", assertions), [])
        self.assertTrue(check("只有缓存", assertions))


class CliTest(unittest.TestCase):
    def run_grader(self, root: Path, *extra: str):
        return subprocess.run(
            [sys.executable, str(GRADER), "--dir", str(root), "--only", "0,1", *extra],
            capture_output=True,
            text=True,
        )

    def test_pass_and_fail_exit_codes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_output(root, 0, "complex", COMPLEX_OK)
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
            write_output(root, 0, "complex", COMPLEX_OK)
            # eval-1 没有 output.txt
            r = self.run_grader(root)
            self.assertEqual(r.returncode, 1)
            self.assertIn("no output.txt", r.stdout)

    def test_run_layout_and_all_runs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            good = COMPLEX_OK
            write_output(root, 0, "complex", good, run=1)
            write_output(root, 0, "complex", good, run=2)
            write_output(root, 1, "quick", "今天是周五。\n", run=1)
            write_output(root, 1, "quick", good, run=2)  # 第 2 次污染,应判失败

            r = self.run_grader(root, "--run", "2")
            self.assertEqual(r.returncode, 1)
            self.assertIn("eval-1-quick: FAIL", r.stdout)

            r = self.run_grader(root, "--all-runs")
            self.assertEqual(r.returncode, 1)
            self.assertIn("eval-0-complex: PASS (2/2 runs)", r.stdout)
            self.assertIn("eval-1-quick: FAIL (1/2 runs)", r.stdout)

            # 结果文件应被写出
            self.assertTrue((root / "grades.json").exists())


if __name__ == "__main__":
    unittest.main()

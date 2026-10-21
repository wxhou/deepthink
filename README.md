# DeepThink

[![skills.sh](https://skills.sh/b/wxhou/deepthink)](https://skills.sh/wxhou/deepthink)

Adaptive deep reasoning skill — auto-detects question complexity and adjusts analysis depth. Quick mode for simple queries, full protocol (ToT / Socratic / verification / iteration) for complex problems. Bilingual (auto Chinese/English).

## Install

```bash
npx skills add wxhou/deepthink
```

The CLI auto-detects installed agents and asks where to install. Useful flags:

```bash
npx skills add wxhou/deepthink -g               # global (~/.claude/skills/ etc.) instead of current project
npx skills add wxhou/deepthink -a claude-code   # target one agent instead of interactive pick
```

Works with Claude Code, Cursor, Codex, GitHub Copilot, Windsurf, Gemini, Cline, Roo, Zed, VS Code and 20+ other agents listed at [skills.sh](https://skills.sh). The skill folder (`SKILL.md` + `core/`) is copied into each agent's skills directory.

## Usage

```bash
# Claude Code
/deepthink 选择 PostgreSQL 还是 MongoDB?

# Cursor / Codex / Copilot / others
deepthink: 选择 PostgreSQL 还是 MongoDB?
```

## How It Works

### Quick Mode (default for simple queries)
If the question is answerable in one sentence → 1-3 sentence direct answer, stop.

### Deep Mode (default for complex queries)
1. **Problem Decomposition + Assumption Statement** — mandatory list of key assumptions with self-verification (✅ holds / ❌ fails / ❓ pending)
2. **Effort Level** — `low` (2-3 rounds) / `medium` (5-6) / `high` (7-9), adjusted by complexity rules
3. **Socratic Questioning** — Clarify / Assumptions / Evidence / Counterexamples / Alternatives / Consequences
4. **Multi-Level Analysis** — Tree of Thoughts (mandatory for high effort) → Understand → Plan → Execute → Verify
5. **Verification** — Reflection / First Principles / Backward / Self-Consistency
6. **Iteration** — if Low/Medium confidence or multi-subsystem
7. **Completeness Check** — confirm all steps before output

## Output Format

```
---
## 🤔 DeepThink Analysis

### Core Problem
[1-sentence summary of the real question]

### Key Assumptions
[List with ✅/❌/❓]

### Conclusion
[Final answer]

### One-Sentence Summary
[Core recommendation]

### Confidence: [High/Medium/Low]
---
```

## Repository Layout

```
deepthink/
├── SKILL.md             # Skill entry (YAML frontmatter + usage)
├── core/                # Canonical protocol (loaded directly by SKILL.md)
│   ├── protocol.en.md   # English
│   └── protocol.zh.md   # Chinese
├── evals/
│   └── evals.json       # 12 test cases (quick/medium/high)
└── scripts/
    └── run_evals.py     # Eval runner
```

## Evals

12 test cases across `quick` / `decision` / `debug` / `tradeoff` / `arch` / `concept` / `complex` types:

```bash
python scripts/run_evals.py --iter 1      # run all cases via claude CLI
python scripts/grade_evals.py --iter 1    # grade outputs against assertions in evals.json
```

Outputs go to `deepthink-workspace/iteration-N/eval-{id}-{type}/with_skill/outputs/output.txt`. Assertions are structural: `quick` prompts must answer directly (no DeepThink template), deeper modes must emit the template with key assumptions and confidence. The grader exits non-zero on any failure.

## License

MIT

## Version

5.2.0 — published to skills.sh
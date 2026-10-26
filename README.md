# DeepThink

[![skills.sh](https://skills.sh/b/wxhou/deepthink)](https://skills.sh/wxhou/deepthink)

Adaptive deep reasoning skill — auto-detects question complexity and adjusts analysis depth. Quick mode for simple queries, full protocol (multi-path analysis / Socratic / verification / iteration) for complex problems. Bilingual (auto Chinese/English).

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

## Update

```bash
npx skills update deepthink   # update this skill to the latest version
npx skills update -g          # update all globally installed skills
```

`update` supports `-p` (project skills only), `-g` (global only) and `-y` (skip prompts). Re-running `npx skills add wxhou/deepthink` also refreshes the installed copy.

## Usage

```bash
# Claude Code
/deepthink 选择 PostgreSQL 还是 MongoDB?

# Cursor / Codex / Copilot / others
deepthink: 选择 PostgreSQL 还是 MongoDB?
```

## How It Works

### Quick Mode (default for simple queries)
If the question can be answered directly (possibly conditionally) → 1-3 plain sentences, no template, stop.

### Deep Mode (default for complex queries)
1. **Problem Decomposition + Assumption Statement** — mandatory list of key assumptions with self-verification (✅ holds / ❌ fails / ❓ pending)
2. **Effort Level** — `low` / `medium` / `high`, describing how far to expand (direct analysis / main dimensions / all dimensions with cross-validation), adjusted by complexity rules
3. **Socratic Questioning** — Clarify / Assumptions / Evidence / Counterexamples / Alternatives / Consequences
4. **Multi-Level Analysis** — compare multiple paths when warranted → Understand → Plan → Execute → Verify
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

## Example Outputs

Quick mode (`deepthink: 999 * 888 = ?`):

> 999 × 888 = 887,112. Quick mode (simple math): (1000 − 1) × 888 = 888,000 − 888 = 887,112.

Deep mode (excerpt from a database-index explanation):

> ### Key Assumptions
> - [x] The context is a relational database (MySQL InnoDB / PostgreSQL) — ✅ holds
>
> ### Conclusion
> An index is a **sorted auxiliary data structure** maintained per column... a B+ tree turns an O(N) page scan into O(log N)...
>
> ### Confidence: High

## Repository Layout

```
deepthink/
├── SKILL.md             # Skill entry (YAML frontmatter + usage)
├── core/                # Canonical protocol (loaded directly by SKILL.md)
│   ├── protocol.en.md   # English
│   └── protocol.zh.md   # Chinese
├── evals/
│   └── evals.json       # 16 test cases + trigger config + assertions
├── scripts/
│   ├── run_evals.py     # Run evals via claude CLI (--jobs, --only)
│   ├── grade_evals.py   # Grade outputs (--diff, --only)
│   ├── test_grade_evals.py
│   ├── check_consistency.py
│   └── deploy-site.sh   # Locked Cloudflare Pages deploy
├── site/
│   └── index.html       # Landing page
├── .github/workflows/   # check.yml (consistency) + deploy-site.yml
├── CLAUDE.md
├── CHANGELOG.md
├── LICENSE
├── package.json         # pinned wrangler devDependency
├── package-lock.json
└── wrangler.toml
```

## Evals

16 test cases across `quick` / `decision` / `debug` / `tradeoff` / `arch` / `concept` / `complex` types, including English prompts and all three trigger forms (`deepthink: `, `/deepthink `, `@deepthink `):

```bash
python scripts/run_evals.py --iter 1 --jobs 3      # run all cases (parallel, ~3x faster)
python scripts/run_evals.py --iter 2 --repeat 3    # run each case 3x for stability
python scripts/grade_evals.py --iter 1             # grade against assertions
python scripts/grade_evals.py --iter 1 --diff 0    # compare with iteration 0
python scripts/grade_evals.py --iter 2 --all-runs  # per-eval pass rate across repeats
```

Outputs go to `deepthink-workspace/iteration-N/eval-{id}-{type}/with_skill/run-{k}/outputs/output.txt` (the legacy `.../with_skill/outputs/` layout is still read). Assertions check both form and substance: `quick` prompts must answer directly (no DeepThink template), deeper modes must emit the template with key assumptions and confidence, plus case-specific content checks (the four requested dimensions, key architecture components, B+ tree mechanics, etc.). `results.json` and `grades.json` capture machine-readable run and grade data. `deepthink-workspace/` lives outside the repo — old `iteration-*` directories can be deleted freely.

## License

MIT

## Version

5.3.0 — published to skills.sh
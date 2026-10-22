# Changelog

## Unreleased

- **Evals**: substance assertions (requested dimensions, architecture
  components, B+ tree mechanics, JS `map()` semantics), regex and
  "at least N of" matching, `--repeat N` stability runs, `--all-runs`
  pass rates, machine-readable `results.json` / `grades.json`.
- **Isolation**: each eval now runs in a temporary working directory
  instead of `~/Documents`.
- **Supply chain**: `wrangler` pinned via `package.json` +
  `package-lock.json` (`npm ci` in CI); Actions pinned to commit SHAs.
- **Release**: repository tagged `v5.2.0`.

## 5.2.0 — 2026-10-22

- **Quick mode hardened**: answers no longer wrap in the DeepThink template.
  Baseline showed even `999 × 888` got the full `Key Assumptions` / `Confidence`
  block; `Output Format` is now explicitly deep-mode only.
- **Single-source protocol**: `SKILL.md` loads `core/protocol.{en,zh}.md`
  directly; the duplicated `references/` copies were removed.
- **Eval harness**: 16 cases (README examples, English prompts, all three
  trigger forms), structural assertions, automatic grading (`grade_evals.py`),
  parallel runs (`--jobs`), iteration diffing (`--diff`), per-eval `agent.log`.
- **CI**: zero-cost consistency check (version/路径/JSON/残留) + grader self-test;
  deploy switched from a non-existent Pages project to Workers static assets
  and now runs against Cloudflare Pages at `deepthinking.pages.dev`.
- **Housekeeping**: MIT `LICENSE` added, wrangler pinned to 4.151.3,
  Actions pinned to commit SHAs, python bytecode ignored.

## 5.1.0 — 2026-09-20

- Platform-agnostic protocol extracted to `core/`, prepared for skills.sh
  publishing (`npx skills add wxhou/deepthink`).

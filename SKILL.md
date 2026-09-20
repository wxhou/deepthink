---
name: deepthink
description: "Adaptive deep reasoning skill that automatically adjusts analysis depth based on question complexity. Uses sequential thinking, multi-path tree-of-thought exploration, Socratic questioning, first-principles verification, and iterative validation to produce high-confidence answers. Quick mode for simple queries, deep mode for complex problems. Bilingual: auto-detects Chinese vs English from prompt."
version: 5.1.0
---

# DeepThink

> **Trigger**: `/deepthink` (Claude Code / Claude.ai) or `deepthink: ` prefix (Cursor / Copilot) or always-on rule (per-platform).

## When to Use
- User invokes the skill
- Complex problem solving, research, step-by-step thinking
- User wants high-confidence, well-reasoned answers

## Language Detection

Read the user's prompt:
- Contains Chinese characters (CJK) → load `references/zh.md`
- Otherwise → load `references/en.md`

## Core Protocol

The full protocol lives in `references/`. Read the appropriate language version above and follow it. Key sections:

1. **Quick Mode Check** — if answerable in one sentence, stop after 1-3 sentences
2. **Problem Decomposition + Assumption Statement** — mandatory assumption list
3. **Socratic Questioning** — clarify, assumptions, evidence, counterexamples, alternatives, consequences
4. **Multi-Level Analysis** — Tree of Thoughts (mandatory for high effort) → Understand → Plan → Execute → Verify
5. **Verification** — Reflection / First Principles / Backward / Self-Consistency
6. **Iteration** — if confidence is Low/Medium or problem spans subsystems
7. **Completeness Check** — before output, confirm all steps done

## Output Format

```
---
## 🤔 DeepThink Analysis
### Core Problem
### Key Assumptions
### Conclusion
### One-Sentence Summary
### Confidence: [High/Medium/Low]
---
```

## Tool Notes

- **Claude Code**: Use `sequentialthinking` MCP if available; use `AskUserQuestion` for clarifications; `dispatch subagent` for parallel exploration
- **Cursor / Copilot / Others**: Use whatever search/clarification tools the platform provides; the protocol's "conditioned" wording handles graceful degradation

See `references/en.md` or `references/zh.md` for the canonical, platform-agnostic version.
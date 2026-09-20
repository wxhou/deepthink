# DeepThink Smart Deep Thinking

> **Platform note**: This is the canonical, platform-agnostic protocol. Tool-specific wrappers (Claude Code SKILL.md, Cursor .mdc, etc.) live under `adapters/`. When in doubt, edit **this file** and regenerate.

## When to Use
- User invokes the skill (`/deepthink`, `deepthink: ` prefix, `@deepthink`, or always-on rule depending on platform)
- Complex problem solving, research, step-by-step thinking
- User wants high-confidence, well-reasoned answers

---

## Quick Mode Check

**Ask first: Can this be answered in one sentence?**
- **Yes** → Answer in 1-3 sentences, stop. No protocol needed.
- **No** → Proceed to Core Protocol.

Simple examples: factual queries, yes/no questions, math calculations, explaining a code snippet, "What is X?"
Complex examples: trade-offs evaluation, multi-step analysis, architecture decisions, debugging, questions requiring research.

---

> **Tip**: If the current platform exposes a structured-thinking tool (e.g. `sequentialthinking`), prefer it to organize reasoning. Otherwise plain multi-pass reasoning is equally effective.

## Core Protocol

### 1. Problem Decomposition + Assumption Statement (mandatory)

> **Assumption statement (mandatory)**: Before any analysis, **must** list key assumptions and self-question "Are these assumptions valid?" — combat "initial assumption lock-in" bias.
>
> **Format**:
> ```
> ### Key Assumptions
> - [ ] Assumption 1
> - [ ] Assumption 2
> - [ ] ...
> ```
>
> For each: ✅ holds / ❌ fails / ❓ uncertain (uncertain ones MUST be checked first)

- Break into smallest logical sub-problems, ordered by dependency
- Define end goal and success criteria
- Set target confidence level (High/Medium/Low)

**Effort Level Assessment**:

| Effort | Problem Characteristics | Thinking Rounds |
|--------|------------------------|----------------|
| **low** | Single dimension, no search needed | 2-3 rounds |
| **medium** | Multi-angle analysis, may need search | 5-6 rounds |
| **high** | Complex reasoning, multi-system, deep argumentation | 7-9 rounds |

**Note**: Simple factual queries don't fall into any level — handled in Quick Mode.

**Complexity Rules**:
- Needs external info/search? → +1 level, **must search**
- Multiple sub-problems? → +1 level
- Moral/ethical/value judgment? → +1 level
- Pure logic/math? → -1 level (can simplify)

**Search & Question Rules**:
- **Confirm time**: Use system currentDate, don't guess
- **Search trigger**: Any information dependency = search, when in doubt, search
- **If unclear**: If the platform exposes a structured questioning tool (e.g. `AskUserQuestion`), use it; otherwise surface clarifying questions inline before continuing

### 2. Socratic Questioning
Select applicable follow-ups:

1. **Clarify** - Do I truly understand the problem? → If the platform offers a structured clarifying tool, use it; otherwise write a short list of unresolved questions
2. **Assumptions** - What assumptions am I making?
3. **Evidence** - What evidence is needed? What info is uncertain?
4. **Counterexamples** - Are there counterexamples?
5. **Alternatives** - Are there other approaches?
6. **Consequences** - What if I'm wrong?

**5 Whys** — only for root cause analysis

### 3. Multi-Level Analysis
For each sub-problem, loop:

- **ToT (mandatory for high effort)**: explore 2-3 reasoning paths first, compare, then deepen
- **Understand**: Restate in your own words, list assumptions and boundaries
- **Plan**: Brainstorm N strategies, evaluate pros/cons
- **Execute**: Step by step, need external info → search immediately
- **Verify (every round)**: Check logical consistency, find contradictions, test boundaries — verify while analyzing, not at the end

### 4. Verification
Choose appropriate verification methods:

- **Reflection**: Does the conclusion hold if premises are reversed? Acknowledge errors — don't double down.
- **First Principles**: Strip away appearance — what's the core physical/logical constraint?
- **Backward Verification**: Work backwards from the goal — what's the inevitable path?
- **Self-Consistency**: If analyzed with a completely different reasoning path, is the conclusion still the same?

**Dynamic Assessment**: During verification, check:
- Any important dimensions not fully explored?
- Any new discoveries requiring additional thinking?
- If needed, continue additional rounds

### 5. Iteration
Iterate if any condition is met:
- Problem spans multiple subsystems
- Conclusion depends on multiple assumptions
- Confidence is Low/Medium

Iterate: Redefine problem → Add evidence → Reanalyze → Verify

### 6. Completeness Check
Before output, confirm:
- ToT multi-path exploration completed?
- Verification (reflection/first principles/backward/self-consistency) completed?
- Arguments supported by evidence (source or reasoning)?
- Iteration completed (if needed)?
- If anything is missing, complete it before outputting
- **Concise over complete**: Don't pad structure — users want clear answers, not boilerplate

**Subagent Dispatch**: If the platform supports sub-task / sub-agent dispatch (e.g. Claude Code subagents), dispatch independent explorations and consolidate; otherwise simulate with `### Sub-exploration N` segments that reason in parallel before merging.

---

## Tool Usage

When encountering uncertain information, naturally think "I'm not sure, let me check."

**After each thinking round**: List information points you **assume are known** but haven't verified — for each:
- Verified → cite source
- Not verified → **search/verify immediately before continuing**

**ReAct Loop**:
- **Reason**: What do I need to search?
- **Act**: Call search/read tools
- **Observe**: Check results
- **Reason**: Re-reason based on results

- **Never guess**: Verify uncertain info before stating. Do not say "it needs a few rounds" or "roughly how long" — no time/step estimates.
- **After tool returns**: Re-verify based on new information.
- **Naturalness**: Avoid rigid formulas, stay flexible; use brief inner-monologue phrases when helpful ("Hmm... but what if...")
- **Anti-crawl fallback**: On access blocked → find available browser/MCP tools → try search cache/alternatives → inform user

---

## Output Format

```
---
## 🤔 DeepThink Analysis

### Core Problem
[1-sentence summary of the real question]

### Key Assumptions
[List key assumptions and self-verify: ✅ holds / ❌ fails / ❓ pending]

### Conclusion
[Final answer]

### One-Sentence Summary
[Core recommendation]

### Confidence: [High/Medium/Low]
---
```

---

## Flowchart

```
Question → Decomposition → Assumption Statement → ToT Paths → Socratic → Multi-Level Analysis
    ↓
Verification (Reflection/First Principles/Backward/Self-Consistency) ← Iterate (if needed)
    ↓
Completeness Check → Output + Confidence
```
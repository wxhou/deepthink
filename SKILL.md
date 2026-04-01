---
name: deepthink
description: "Use when user asks with /deepthink prefix, or wants deep analysis. For complex reasoning, multi-step analysis, architecture decisions, debugging, or research — NOT for simple factual questions (those get direct answers). Automatically adapts depth: simple → quick answer, complex → full structured reasoning. Supports both Chinese and English — detect from user's prompt language."
---

# /deepthink - Smart Deep Thinking Skill

<!-- LANGUAGE DETECTION: Read the user's prompt to detect language.
     If the prompt contains Chinese characters (CJK Unified Ideographs), use Chinese version.
     Otherwise use English version. -->

---

<!-- [ZH] Chinese Version Below -->

# 中文版 — DeepThink 智能深度思考

## 何时使用
- 用户输入 `/deepthink xxx`
- 复杂问题求解、研究、分步骤思考
- 用户需要高置信度、充分论证的回答

---

## 快速判断

**先用一句话问自己：能直接回答吗？**
- **能** → 1-3句话直接答，停止。不走任何协议。
- **不能** → 进入 Core Protocol。

简单例子：事实查询、yes/no、数计算、看代码片段解释其作用、"什么是X"。
复杂例子：trade-offs评估、多步分析、架构决策、调试推理、需要搜索的问题。

---

> **提示**: 使用 **sequentialthinking MCP** 工具来结构化推理过程。

## Core Protocol

### 1. 问题拆解

> **假设检查（强制）**: 第一轮思考后，必须列出关键假设，并自问"这些假设都对吗？"——对抗"初始假设锁定"偏差。

- 拆解为最小逻辑子问题，按依赖顺序排列
- 明确最终目标和成功标准
- 设定目标置信度 (High/Medium/Low)

**复杂度评估（Effort级别）**：

| Effort级别 | 问题特征 | 思考轮次 |
|-----------|---------|---------|
| **low** | 单一维度、无需搜索 | 2-3轮 |
| **medium** | 多角度分析、可能需要搜索 | 5-6轮 |
| **high** | 复杂推理、多系统交互、深度论证 | 7-9轮 |

**注意**：简单事实查询不属于以上任何级别——快速判断阶段已直接回答。

**复杂度判断规则**：
- 需要外部信息搜索？→ +1级，且**必须搜索验证**
- 涉及多个子问题？→ +1级
- 道德/伦理/价值判断？→ +1级
- 纯逻辑/数学问题？→ -1级（可简化）

**搜索和提问规则**：
- **确认时间**：以系统 currentDate 为准，不凭记忆
- **搜索触发**：涉及信息依赖即搜索，不确定则查
- **如有疑问**: 立即使用 AskUserQuestion 工具提问

### 2. 苏格拉底提问
选择适用的追问：

1. **Clarify** - 真正理解问题了吗？→ **有疑问必须用 AskUserQuestion**
2. **Assumptions** - 做了什么假设？
3. **Evidence** - 需要什么证据？不确定的信息有哪些？
4. **Counterexamples** - 有反例吗？
5. **Alternatives** - 有其他方案吗？
6. **Consequences** - 错了会怎样？

**5 Whys** - 仅在根因分析时使用

### 3. 多层次分析
对每个子问题循环执行：

- **ToT（强制）**: high effort 问题**必须**先探索2-3条推理路径，比较后再深入。
- **理解**: 用自己的话重述，列出假设和边界
- **规划**: 头脑风暴N个策略，评估优缺点
- **执行**: 需要外部信息→立即搜索验证
- **验证（每轮都要）**: 检查逻辑一致性，寻找矛盾，测试边界——边分析边验证

### 4. 验证
选择适用的验证方式：

- **反思**: 前提反转结论还成立吗？最弱假设是哪个？
- **第一性原理**: 剥离表象，最核心的物理/逻辑约束是什么？
- **逆向验证**: 从目标倒推，必经路径是什么？
- **自洽性检验**: 用完全不同的推理路径重新分析，结论是否一致？

**动态评估**：验证阶段检查：
- 是否还有重要维度未展开？
- 是否有新发现需要追加思考？
- 如需要，继续追加轮次

### 5. 迭代
满足任一条件则迭代：
- 问题涉及多个子系统
- 结论依赖多个假设
- 置信度为 Low/Medium

迭代：重新定义问题 → 补充证据 → 重新分析 → 验证

### 6. 流程完整性确认
输出结论前确认：
- ToT多路径探索是否完成？
- 验证（反思/第一性/逆向/自洽性）是否完成？
- 论证有证据支撑（信息源或推理依据）？
- 迭代是否完成（如果需要）？
- 如有遗漏，补充后再输出

**Subagent 调度**：满足任一条件，dispatch subagent 独立探索后汇总：
- 涉及代码编写/调试/执行验证
- 涉及数学推导或形式化证明
- 各分支需不同信息源或专业视角

---

## 工具使用

遇到不确定的信息时，自然地"我不确定，所以要查"。

**每轮思考后**：列出本轮推理中**"我认为已知"但未验证的信息点**，对每个点：
- 已验证 → 标注来源
- 未验证 → **立即搜索验证后再继续**

**ReAct 循环**：
- **Reason**: 需要查什么？
- **Act**: 调用搜索/读取工具
- **Observe**: 看工具返回
- **Reason**: 基于结果重新推理

- **禁止猜测**: 不确定先搜索验证
- **工具返回后**: 基于新信息重新验证

---

## 输出格式

```
---
## 🤔 DeepThink 分析

### 核心问题
[1句话概括真正问题]

### 关键假设
[列出关键假设并自验]

### 结论
[最终答案]

### 一句话总结
[核心建议]

### 置信度: [High/Medium/Low]
---
```

---

<!-- [EN] English Version Below -->

# English Version — DeepThink Smart Deep Thinking

## When to Use
- User writes `/deepthink xxx`
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

> **Tip**: Use **sequentialthinking MCP** to structure reasoning.

## Core Protocol

### 1. Problem Decomposition

> **Assumption Check (mandatory)**: After the first round of thinking, list key assumptions and ask "Are these assumptions valid?" — combat "initial assumption lock-in."

- Break into smallest logical sub-problems, ordered by dependency
- Define end goal and success criteria
- Set target confidence level (High/Medium/Low)

**Effort Level Assessment**:

| Effort | Problem Characteristics | Thinking Rounds |
|--------|------------------------|----------------|
| **low** | Single dimension, no search needed | 2-3 rounds |
| **medium** | Multi-angle analysis, may need search | 5-6 rounds |
| **high** | Complex reasoning, multi-system, deep论证 | 7-9 rounds |

**Note**: Simple factual queries don't fall into any level — handled in Quick Mode.

**Complexity Rules**:
- Needs external info/search? → +1 level, **must search**
- Multiple sub-problems? → +1 level
- Moral/ethical/value judgment? → +1 level
- Pure logic/math? → -1 level (can simplify)

**Search & Question Rules**:
- **Confirm time**: Use system currentDate, don't guess
- **Search trigger**: Any information dependency = search, when in doubt, search
- **If unclear**: Use AskUserQuestion tool immediately

### 2. Socratic Questioning
Select applicable follow-ups:

1. **Clarify** - Do I truly understand the problem? → **Must use AskUserQuestion if unclear**
2. **Assumptions** - What assumptions am I making?
3. **Evidence** - What evidence is needed? What info is uncertain?
4. **Counterexamples** - Are there counterexamples?
5. **Alternatives** - Are there other approaches?
6. **Consequences** - What if I'm wrong?

**5 Whys** — only for root cause analysis

### 3. Multi-Level Analysis
For each sub-problem, loop:

- **ToT (mandatory)**: High effort problems **must** explore 2-3 reasoning paths first, compare, then deepen.
- **Understand**: Restate in your own words, list assumptions and boundaries
- **Plan**: Brainstorm N strategies, evaluate pros/cons
- **Execute**: Step by step, need external info → search immediately
- **Verify (every round)**: Check logical consistency, find contradictions, test boundaries — verify while analyzing, not at the end

### 4. Verification
Choose appropriate verification methods:

- **Reflection**: Does the conclusion hold if premises are reversed? What's the weakest assumption?
- **First Principles**: Strip away appearance — what's the core physical/logical constraint?
- **Backward Verification**: Work backwards from the goal — what's the必经 path?
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

**Subagent Dispatch**: If any condition met, dispatch subagent for independent exploration then consolidate:
- Code writing/debugging/execution verification
- Mathematical derivation or formal proof
- Different branches need different information sources or expertise

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

- **Never guess**: Verify uncertain info before stating
- **After tool returns**: Re-verify based on new information

---

## Output Format

```
---
## 🤔 DeepThink Analysis

### Core Problem
[1-sentence summary of the real question]

### Key Assumptions
[List key assumptions and self-verify]

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
问题/Question → 问题拆解/Decomposition → ToT多路径/ToT Paths → 苏格拉底/Socratic → 多层次分析/Multi-Level
    ↓
验证(反思/第一性/逆向/自洽)/Verification ← 迭代/Iterate (if needed)
    ↓
流程完整性/Completeness → 总结输出/Output + 置信度/Confidence
```

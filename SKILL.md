---
name: deepthink
description: Use when user asks with /deepthink or /think prefix, or wants deep analysis - triggers advanced structured reasoning with automatic complexity detection. Activates for complex, analytical, reasoning-intensive queries.
---

# /deepthink - Smart Deep Thinking Skill

## When to Use

- User writes `/deepthink xxx` or `/think xxx` or `/深度思考 xxx`
- User explicitly asks to "think deeper" or "深度思考"
- Complex problem solving, research, step-by-step thinking
- User wants high-confidence, well-reasoned answers

## Quick Decision: Deep Mode vs Quick Mode

**Before following the full protocol, first assess the question complexity:**

### Quick Mode (Skip to Output)
For simple questions:
- Factual queries ("今天周几?")
- Confirmation ("这个文件存在吗?")
- Single-command tasks ("帮我运行 npm install")
- Yes/No questions

**Quick Mode Response:**
- Direct answer in 1-2 sentences
- Skip detailed analysis
- No structured format needed

### Deep Mode (Follow Full Protocol)
For complex questions:
- Multiple factors to consider
- Trade-offs to evaluate
- No clear "right answer"
- Requires research or evidence
- Decision-making or planning
- Technical architecture

---

## Core Protocol (For Deep Mode Only)

### 1. Problem Decomposition
- Break query into smallest logical sub-problems
- Number them in dependency order
- Identify final goal and success criteria
- Determine required confidence level (High/Medium/Low)

### 2. Multi-Layer Thinking Process
For each sub-problem, cycle through:

**Understand**:
- Rephrase the sub-problem in your own words
- List all assumptions being made
- Define boundaries and potential pitfalls

**Plan**:
- Brainstorm 2-4 strategies
- Evaluate pros/cons of each
- Select optimal approach

**Execute**:
- Step-by-step implementation
- If external info needed → use tools immediately
- Search/verify uncertain facts (never guess)

**Verify**:
- Check logic consistency
- Look for contradictions
- Test edge cases

### 3. Self-Questioning Loop (Smart Selection)
**NOT all questions need all 6 questions. Select relevant ones:**

#### Choose applicable Socratic Questions:
1. **Clarify** - Is my understanding correct? (If ambiguous → ask user)
2. **Challenge assumptions** - What assumptions am I making? (If many → list them)
3. **Find evidence** - What's the evidence? (If claims made → verify)
4. **Find counterexamples** - Any counterexamples? (If strong claim → seek)
5. **Consider alternatives** - Other solutions? (If decision → compare)
6. **Consequences** - What if wrong? (If risky → assess)

**5 Whys** - Only use when finding root cause is essential

### 4. Tool Integration
- **Never guess** uncertain facts: always search/verify first
- Use available tools: web_search → read files → code execution
- After tool results → re-verify with new information

### 5. Adaptive Output

**For Quick Questions:** Direct answer, 1-2 sentences

**For Complex Questions:**
```
---
## 🤔 DeepThink 分析

### 核心问题
[1句话概括真正问题]

### 关键分析
[根据问题选择相关分析，不是全写]

### 结论
[最终答案]

### 置信度: [High/Medium/Low]
---
```

**Keep it concise**: If 3 points cover it, don't list 10.

---

## Adaptive Response Rules

| Question Type | Response Style |
|--------------|---------------|
| Simple fact | Direct answer, skip format |
| How-to guide | Steps + key considerations |
| Decision | Pros/cons + recommendation |
| Analysis | Core insight + evidence |
| Research | Summary + sources |

---

## Important

- **Always start with complexity assessment**
- Quick questions → Quick Mode (skip full protocol)
- Complex questions → Deep Mode (follow protocol selectively)
- Not all steps always needed - be adaptive
- If information insufficient → ask user before guessing

## Examples

```
# Quick Mode
/deepthink 今天周几？
→ 直接回答: 今天是周五。

# Deep Mode
/deepthink 应该选择 PostgreSQL 还是 MongoDB？
→ Problem: 数据库选型
→ Analysis: 对比场景、性能、一致性
→ Conclusion: 根据场景推荐 + 置信度
```

---

## Flowchart

```
用户输入 /deepthink xxx
    ↓
判断复杂度（快速模式 vs 深度模式）
    ↓
├── 简单问题 → 直接回答，简洁
    ↓
└── 复杂问题 → 选择性执行步骤
        ├── 需要拆解？→ 问题拆解
        ├── 需要验证？→ 搜索验证
        ├── 需要质疑？→ 选择性自我追问
        └── 总结输出 + 置信度
```

---
name: deepthink
description: Use when user asks with /deepthink or /think prefix, or wants deep analysis - triggers advanced structured reasoning to ensure thorough, accurate answers. Activates for complex, analytical, reasoning-intensive queries.
---

# /deepthink - Advanced Deep Thinking Skill

## When to Use

- User writes `/deepthink xxx` or `/think xxx` or `/深度思考 xxx`
- User explicitly asks to "think deeper" or "深度思考"
- Question is ambiguous and needs careful analysis
- Complex problem solving, research, step-by-step thinking
- User wants high-confidence, well-reasoned answers
- Questions requiring multi-step logic, evidence, or verification

## Core Protocol (Strictly Follow)

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

### 3. Self-Questioning Loop (Mandatory)
Force at least 6 challenging questions:
- What is the weakest assumption? Provide counterexamples.
- Is there a simpler or more elegant solution?
- How would results change if a key condition varies?
- What risks or limitations does this conclusion have?
- Am I missing critical information? (If yes → search immediately)
- Can this conclusion be proven more rigorously?

### 4. Tool Integration
- **Never guess** uncertain facts: always search/verify first
- Use available tools: web_search → read files → code execution
- After tool results → re-verify with new information

### 5. Synthesis & Output
Combine all results:
- Check overall consistency
- Consider alternative interpretations (if ambiguous)
- Provide structured answer with:
  - Key conclusions (numbered/bulleted)
  - Confidence level
  - Limitations
  - Follow-up suggestions

## Required Output Format

```
---
## 🤔 DeepThink 深度分析

### 问题拆解
1. [子问题1]
2. [子问题2]
...

### 思考过程
[详细的推理链]

### 自我追问
- Q: 最弱的假设是什么? A: ...
- Q: 有更简单的方案吗? A: ...
...

### 结论
[最终答案]

### 置信度: [High/Medium/Low]
### 限制/注意事项: [如有]
---
```

## Important

- This skill is triggered by user intent, not automatically on every question
- Follow the full protocol: do not shortcut steps
- If information is insufficient, ask user before guessing
- Always assign confidence level to final answer

## Examples

```
/deepthink 如何设计一个高效的消息队列系统？
→ Decompose: 架构→持久化→高可用→性能优化
→ Plan: 对比 Kafka/RabbitMQ/Redis
→ Execute: 搜索最新方案
→ Self-question: 瓶颈在哪? 扩展性?
→ Output with confidence level

/deepthink 分析当前AI Agent的发展趋势
→ Search latest developments
→ Verify claims with sources
→ Structured timeline output
→ Confidence: High (based on recent data)
```

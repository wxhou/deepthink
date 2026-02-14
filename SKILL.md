---
name: deepthink
description: Use when user asks with /deepthink or /think prefix, or wants deep analysis - triggers advanced structured reasoning with automatic complexity detection. Activates for complex, analytical, reasoning-intensive queries.
---

# /deepthink - Smart Deep Thinking Skill

## When to Use
- User writes `/deepthink xxx` or `/think xxx` or `/深度思考 xxx`
- Complex problem solving, research, step-by-step thinking
- User wants high-confidence, well-reasoned answers

---

## Core Protocol

> **Note**: Use **sequentialthinking MCP** to structure the reasoning process.

### 1. 问题拆解
- 拆解为最小逻辑子问题，按依赖顺序排列
- 明确最终目标和成功标准
- 设定目标置信度 (High/Medium/Low)
- **如对问题有疑问 → 立即使用 AskUserQuestion 工具提问**

### 2. 苏格拉底提问
选择适用的追问：

1. **Clarify** - 我真正理解问题了吗？→ **如有疑问必须使用 AskUserQuestion 工具提问**
2. **Assumptions** - 我做了什么假设？
3. **Evidence** - 需要什么证据？不确定的信息有哪些？
4. **Counterexamples** - 有反例吗？
5. **Alternatives** - 有其他方案吗？
6. **Consequences** - 错了会怎样？

**5 Whys** - 仅在寻找根因时使用

### 3. 多层次分析
对每个子问题循环执行：

- **理解**: 用自己的话重述，列出假设和边界
- **规划**: 头脑风暴2-4个策略，评估优缺点
- **执行**: 步步为营，需要外部信息→立即搜索验证
- **验证**: 检查逻辑一致性，寻找矛盾，测试边界

### 4. 验证（选择性）
根据问题类型选择验证方式：

- **反思机制**: 前提反转结论还成立吗？最弱链是哪个假设？
- **第一性原理**: 剥离表象，最核心的物理/逻辑约束是什么？
- **逆向验证**: 从目标倒推，必经路径是什么？

### 5. 迭代
如满足任一条件则迭代：
- 问题涉及多个子系统
- 结论依赖多个假设
- 置信度为 Low/Medium

迭代流程：重新定义问题 → 补充证据 → 重新分析 → 验证

---

## 工具使用
- **Never guess**: 不确定的信息先搜索验证
- **工具返回后**: 基于新信息重新验证

---

## 输出格式

```
---
## 🤔 DeepThink 分析

### 核心问题
[1句话概括真正问题]

### 关键分析
[选择相关的分析阶段]

### 结论
[最终答案]

### 置信度: [High/Medium/Low]
---
```

**简洁原则**: 3点能说清就不列10点

---

## 注意事项
- 不是所有步骤都需要详细展开，选择与问题相关的阶段
- **信息不足时必须先问用户** → 使用 `AskUserQuestion` 工具获取澄清
- 永远不要猜测用户意图，有疑问先问

## 流程图

```
问题 → 问题拆解 → 苏格拉底提问 → 多层次分析
    ↓
验证（反思/第一性/逆向）←— 迭代（如需要）
    ↓
总结输出 + 置信度
```

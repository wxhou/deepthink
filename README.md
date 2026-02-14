# deepthink

Advanced deep thinking skill for Claude Code - enables rigorous, structured reasoning for complex problems.

## What is this?

This skill triggers advanced structured reasoning before answering questions. It follows a strict multi-layer protocol to:
- Minimize hallucinations
- Explore alternatives
- Achieve high-confidence answers

## Features

- **Problem Decomposition** - Break complex queries into logical sub-problems
- **Multi-Layer Thinking** - Understand → Plan → Execute → Verify cycle
- **Self-Questioning Loop** - Socratic Method + 5 Whys for deep analysis
- **Tool Integration** - Search/verify uncertain facts instead of guessing
- **Structured Output** - Clear conclusions with confidence levels

## Installation

### Method 1: Clone to skills directory

```bash
# Clone to your Claude Code skills directory
git clone https://github.com/wxhou/deepthink.git ~/.claude/skills/deepthink
```

### Method 2: Using Plugin (if available)

```bash
/plugin install deepthink-marketplace
```

## Usage

When you want deep analysis, use the `/deepthink` command:

```
/deepthink Your question here
```

Or alternatively:

```
/think Your question here
/depthink Your question here
```

## How it works

1. **Problem Decomposition** - Break query into sub-problems
2. **Multi-Layer Thinking** - Understand → Plan → Execute → Verify
3. **Self-Questioning** - Socratic Method (6 questions) + 5 Whys
4. **Tool Verification** - Search/verify uncertain facts
5. **Structured Output** - Conclusion + Confidence Level + Limitations

## Output Format

```
---
## 🤔 DeepThink 深度分析

### 问题拆解
1. [子问题1]
2. [子问题2]
...

### 思考过程
[详细推理链]

### 自我追问（苏格拉底式 + 5 Whys）
#### 苏格拉底提问：
- Q: 我的理解正确吗? A: ...
- Q: 最弱的假设是什么? A: ...
- Q: 有没有反例? A: ...
- Q: 有没有其他方案? A: ...
- Q: 如果错了会有什么后果? A: ...

#### 5 Whys（如需找根本原因）：
- 为什么? → 为什么? → 为什么? → 为什么? → 为什么?

### 结论
[最终答案]

### 置信度: [High/Medium/Low]
### 限制/注意事项: [如有]
---
```

## Requirements

- Claude Code CLI
- `sequentialthinking` MCP - **Built-in, no installation needed**

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
→ Confidence: High
```

## FAQ

### Q: Do I need to install sequentialthinking separately?
**A: No!** The `sequentialthinking` MCP is built into Claude Code. Just install this skill and it will work.

### Q: Does this run automatically on every question?
**A:** No. You must explicitly invoke with `/deepthink`. Claude Code doesn't support "pre-response hooks" yet.

---

**Version**: 2.0.0
**Author**: wxhou

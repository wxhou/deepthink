# deepthink

Smart deep thinking skill for Claude Code - automatically adapts depth based on question complexity.

## What is this?

This skill triggers intelligent, adaptive reasoning. It automatically detects question complexity and chooses the appropriate response depth - quick answers for simple questions, deep analysis for complex ones.

## Key Features

- **Automatic Complexity Detection** - Smart mode selection
- **Quick Mode** - Direct answers for simple questions
- **Deep Mode** - Full analysis for complex problems
- **Adaptive Output** - Not every question needs full protocol
- **Selective Self-Questioning** - Only relevant questions

## Prerequisites

This skill leverages the **sequentialthinking MCP** server (built into Claude Code) to structure the reasoning process. No additional installation is required for this dependency.

## Installation

### Method 1: Clone to skills directory

```bash
git clone https://github.com/wxhou/deepthink.git ~/.claude/skills/deepthink
```

### Method 2: Using Plugin

```bash
/plugin install deepthink-marketplace
```

## Usage

```bash
/deepthink Your question here
```

## How It Works

### Step 1: Complexity Assessment
First, assess whether the question needs deep analysis:

**Quick Mode (skip full protocol):**
- Simple facts ("What day is today?")
- Confirmations ("Does this file exist?")
- Single tasks ("Run npm install")
- Yes/No questions

**Deep Mode (follow protocol):**
- Multiple factors to consider
- Trade-offs to evaluate
- No clear "right answer"
- Requires research
- Decision-making

### Step 2: Adaptive Response

| Question Type | Response Style |
|--------------|---------------|
| Simple fact | Direct answer |
| How-to guide | Steps + key points |
| Decision | Pros/cons + recommendation |
| Analysis | Core insight + evidence |

## Output Examples

### Quick Mode
```
/deepthink 今天周几？
→ 今天是周五。
```

### Deep Mode
```
/deepthink 应该选择 PostgreSQL 还是 MongoDB？

## 分析

### 核心问题
数据库选型需要根据场景评估

### 关键分析
- PostgreSQL: 强一致性、复杂查询、JSON支持
- MongoDB: 灵活schema、高写入、文档存储

### 结论
根据场景选择：
- 金融/交易 → PostgreSQL
- 内容/日志 → MongoDB

### 置信度: Medium
```

## FAQ

### Q: Does every question need full analysis?
**A:** No! The skill automatically detects complexity. Simple questions get quick answers.

### Q: What if I'm not sure?
**A:** When uncertain, choose Deep Mode to be safe.

### Q: Do I need sequentialthinking?
**A:** It's built into Claude Code - no installation needed.

---

**Version**: 3.0.0
**Author**: wxhou

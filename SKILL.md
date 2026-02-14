---
name: deepthink
description: Use when user asks with /deepthink or /think prefix, or wants deep analysis - triggers sequential thinking to ensure understanding before answering
---

# /deepthink - Deep Thinking Skill

## When to Use

- User writes `/deepthink xxx` or `/think xxx` or `/深度思考 xxx`
- User explicitly asks to "think deeper" or "深度思考"
- Question is ambiguous and needs careful analysis when prompted by user
- User wants to ensure understanding before proceeding

## Workflow

1. **Load sequentialthinking MCP tool**
2. **Run multi-round thinking** - let the MCP decide how many iterations are needed based on complexity
   - Use `needsMoreThoughts: true/false` to control continuation
   - Analyze: What is the user really asking? Any ambiguities? What assumptions am I making?
3. **Confirm understanding** with user if unclear
4. **Then proceed to answer**

## Example Response Format

```
---
## 🤔 思考分析

[Thought 1: Initial analysis]
[Thought 2: Verification/challenge]

结论：[你的理解]
---
```

## Important

- This skill is triggered by user intent, not automatically on every question
- Only use when user explicitly requests deep thinking

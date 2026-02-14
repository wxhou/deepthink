# deepthink

A Claude Code skill for deep thinking using sequentialthinking MCP.

## What is this?

This skill triggers deep, multi-round thinking before answering questions - helps avoid superficial answers by analyzing the problem thoroughly first.

## Features

- Uses `sequentialthinking` MCP for structured deep analysis
- Automatically determines how many thinking rounds are needed
- Confirms understanding before answering
- Helps avoid mistakes like answering without understanding the full context

## Installation

### Method 1: Clone to skills directory

```bash
# Clone to your Claude Code skills directory
git clone https://github.com/wxhou/deepthink.git ~/.claude/skills/deepthink
```

### Method 2: Using Skill tool (if available)

In Claude Code, you can install skills via the skill marketplace or by placing the skill in your skills directory.

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

1. Loads the `sequentialthinking` MCP tool
2. Runs multi-round thinking - MCP decides the number of iterations
3. Analyzes: What is the user really asking? Any ambiguities? What assumptions am I making?
4. Confirms understanding with user if unclear
5. Then proceeds to answer

## Requirements

- Claude Code CLI
- `sequentialthinking` MCP - **Built-in, no installation needed** (comes with Claude Code by default)

## FAQ

### Q: Do I need to install sequentialthinking separately?
**A: No!** The `sequentialthinking` MCP is built into Claude Code. Just install this skill and it will work.

## Example

```
/deepthink Why did my previous answer about going to the car wash fail?
```

The skill will think through:
- What was the actual question context?
- What assumptions were made?
- What information was missing?
- Then provide a more thoughtful answer

---

**Note**: This skill needs to be explicitly invoked with `/deepthink` - it won't automatically run on every question (Claude Code doesn't support "pre-response hooks" yet).

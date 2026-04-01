---
name: deepthink
description: "Use when user asks with /deepthink prefix, or wants deep analysis. For complex reasoning, multi-step analysis, architecture decisions, debugging, or research — NOT for simple factual questions (those get direct answers). Automatically adapts depth: simple → quick answer, complex → full structured reasoning. Bilingual: auto-detects Chinese vs English from prompt and loads references/zh.md or references/en.md."
---

# /deepthink - Smart Deep Thinking Skill

<!-- Language Detection:
     Read the user's prompt to detect language.
     If the prompt contains Chinese characters (CJK) → load references/zh.md
     Otherwise → load references/en.md

     After loading, follow the localized version's instructions.
-->

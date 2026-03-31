---
description: Explica el código en detalle con contexto y razonamiento.
---
# Explain Workflow

Explain code in detail with context and reasoning.

The argument `$ARGUMENTS` contains the path to the file, function, or concept to explain.

## When to use this workflow

| Phase | When to invoke |
|---|---|
| **Fase 2 — Análisis** | Before designing any change, use `/explain` on the target model or view to understand current behavior and dependencies. |
| **Fase 4 — Desarrollo** | When editing unfamiliar code, use `/explain` first to avoid breaking existing logic. |
| **Debugging** | When diagnosing a bug in a complex method, explain the code path before proposing a fix. |

> Lean principle: invest 2 minutes in understanding before 2 hours in wrong implementation.

Steps:
1. Read the target code and the surrounding context.
2. Identify the general purpose of the code.
3. Explain in this order:

## Explanation Structure

### What it does (1-2 line summary)
Concise description of the purpose.

### How it works (step-by-step)
Walk through the execution flow, explaining each logical block.
Use analogies when they genuinely help.

### Why it is written this way
- Design decisions (why this pattern instead of another?)
- Known trade-offs
- Framework/library context that influences style

### Dependencies and connections
- Which other files/modules use it
- What this code depends on
- How it fits the broader architecture

### Possible improvements (only if relevant)
- Mention only if there are clear issues
- Avoid unnecessary refactors

Principles:
- Match depth to code complexity
- Don’t explain the obvious (e.g., don’t describe that `i++` increments `i`)
- Focus on intent, not syntax
- If there’s a design pattern, name it

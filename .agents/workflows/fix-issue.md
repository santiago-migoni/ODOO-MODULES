---
description: Corrige un issue o bug siguiendo las convenciones del repositorio.
---
Diagnose and fix a bug in the code.


The argument `$ARGUMENTS` contains the description of the issue/bug to resolve.

Steps:
1. Analyze the provided problem description.
2. Search the codebase for relevant files using Grep and Glob.
3. Identify the root cause of the bug.
4. Propose a solution explaining:
   - What causes the bug
   - Which files need changes
   - The proposed fix (what to change and why)
5. Apply the fix with the minimum necessary edits.
6. Verify the fix does not introduce regressions by checking related usages.
7. If tests exist, run them to validate the fix.

Principles:
- Minimal change: do not refactor code that is not broken.
- Explain the “why” of the bug, not only the “what”.
- If the bug cannot be reproduced with the given info, request more context.

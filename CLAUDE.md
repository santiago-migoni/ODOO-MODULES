# Odoo 19 Custom Module Development — Dipleg

This repository contains custom Odoo 19.0 Community modules for Dipleg, deployed on Odoo.sh.

## Language

- Reply and propose in Spanish.
- Code comments: minimal, English, only when helpful.

## Workflow

1. Understand the requirement (ask clarifying questions if needed).
2. Propose a plan and options — **always before coding**.
3. Wait for approval before making edits.
4. Implement with minimal, targeted edits.
5. Add/adjust tests and run a quick sanity check when possible.
6. Final review: correctness, security, performance, Odoo 19 conventions.

### Propose-first rule

Do NOT directly edit files or generate large code changes until you present:
- The intended approach
- The affected files
- The test strategy (at least what to add/check)

Proceed only after approval. If the user has not approved, stop at the proposal stage.

### Proposal format

When proposing changes, use this structure:
- **Goal**: what you're solving
- **Plan**: steps to implement
- **Files**: create/update list
- **Tests/checks**: what to add and verify
- **Risks/assumptions**: any uncertainty

Provide 2-3 alternatives if the user asks for options.

### Missing context

If critical context is missing (model name, XML IDs, view structure, security groups):
- Ask targeted questions first.
- Otherwise propose a safe default and clearly mark assumptions.
- Never invent identifiers without evidence from the codebase.

## Odoo 19 Conventions (mandatory)

All custom modules must follow these patterns:

- Use `<list>` (not `<tree>`).
- Use direct UI attributes (`invisible="..."`) instead of legacy `attrs="..."`.
- Use `@api.ondelete(at_uninstall=False)` for delete prevention (not `unlink()` overrides).
- Use `aggregator=` for grouped fields (not `group_operator=`).
- Prefer batch operations (`create([{...}, {...}])`) over `create()` inside loops.
- Avoid N+1: never `search()` inside loops; use batched domains, `read_group()`, or aggregated queries.
- Use `models.Constraint` instead of `_sql_constraints` for SQL constraints.

## Quality Gates (non-negotiable)

Before marking any task as done:

- **Tests**: Add/adjust `TransactionCase` / `HttpCase` for behavior changes (computed fields, constraints, state transitions, wizard actions, access rules).
- **Security**: Ensure ACL/record rules, auth for controllers, no secret leakage.
- **Performance**: No N+1 queries, no expensive loops; use batching and ORM-friendly patterns.
- **Consistency**: Follow the coding style already present in the repository.

## Module Structure & Naming

- Technical name: `dipl_<module_name>` (always with prefix).
- Version: `19.0.x.y.z`
- License: `LGPL-3`
- Author: `Dipleg`
- Website: `https://dipleg.com`
- XML IDs: namespaced with module prefix, must be stable.
- Security files under `security/` (`ir.model.access.csv` + rules XML when applicable).
- Consider `company_id` and multi-company from the start when relevant.

## Translation Standard

- Base msgid/source strings are **English** (the strings you write in code).
- Translation output: `i18n/es.po`.
- Do NOT generate `i18n/en.po`.
- If more languages are requested, generate additional `i18n/<lang>.po` files.

## Debugging Approach

When diagnosing errors:
1. Capture the error message and stack trace.
2. Identify reproduction steps (or the most likely trigger path).
3. Isolate the failure location by searching the codebase.
4. Implement a minimal fix consistent with existing style and Odoo 19 best practices.
5. Verify the solution (tests, lint, or runtime check).
6. Provide: root cause, evidence, fix, test approach, and prevention recommendations.

## Reference Guides

For Odoo 19 API patterns, consult the skill at `.claude/skills/odoo-19/` which contains 18 specialized guides covering actions, controllers, data files, decorators, development, fields, manifest, migration, mixins, models, OWL, performance, reports, security, testing, transactions, translations, and views.

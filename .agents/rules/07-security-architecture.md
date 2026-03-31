---
trigger:
globs: "**/*.py", "**/*.xml", "**/security/**", "**/ir.model.access.csv"
phase: f4-f5
description: Security architecture — ACL, record rules, AND/OR logic
---

# security-architecture

Security is foundational. It must be designed, documented, and stress-tested from the first iteration — never as a post-launch patch.

## Layered Security Model

1. **User Groups** (`res.groups`): Logical roles (e.g., "Sales Manager", "Warehouse Operator"). Define hierarchy and category.
2. **Access Rights** (`ir.model.access`): Binary CRUD permissions per model, imported via CSV. Additive: total access = union of all groups the user belongs to. If no matching ACL exists, access is **denied by default** (Strict Access).
3. **Record Rules** (`ir.rule`): Row-level security using domain expressions (`domain_force`). Inject invisible SQL filters evaluated against dynamic variables (`user.id`, `company_id`).

## Critical: AND vs OR Logic

| Rule Type | Assigned Group | Logic | Effect |
|---|---|---|---|
| Global Rules | None (applies to all users) | **AND** (intersection) | Each global rule RESTRICTS access. User must satisfy ALL global rules. |
| Group Rules | Tied to a `res.groups` | **OR** (union) | Each group rule EXPANDS access. User needs to satisfy at least ONE. |

**Superposition**: Group rules operate ONLY within the perimeter defined by global rules. A group rule cannot override a global restriction.

## Mandatory Practices

- Every new model MUST have an entry in `ir.model.access.csv` before the first test.
- Models with financial/inventory impact MUST have `company_id` + a multi-company record rule from day one.
- `sudo()` usage MUST be justified in the proposal and reviewed in `/security-audit`.
- No hardcoded credentials, tokens, or secrets in code.
- Controllers MUST declare the correct `auth` type (`user`, `public`, `none`).
- Portal/external users MUST be isolated via dedicated record rules — never share internal group rules.

## Common Pitfalls

- Missing ACL → `AccessError` blocking all users on install.
- Global rule too restrictive → locks out admin users.
- Group rules without matching global → false sense of security (no baseline restriction).
- `sudo()` bypassing record rules without re-validating business logic.

---
description: Realiza una auditoría de seguridad en un módulo de Odoo.
---
# Security Audit Workflow (Odoo 19)

Process to audit code for security risks in Odoo 19 custom modules.

The argument `$ARGUMENTS` contains the target module path or name.

## 1. Access Control (ACL)

1. Verify every model has an entry in `security/ir.model.access.csv`. No model should be unprotected.
2. Check that `base.group_user` does not have blanket `1,1,1,1` permissions on sensitive models. Restrict to the minimum necessary.
3. Ensure custom groups are defined and used when the module handles sensitive business data.

## 2. Record Rules

1. Verify models with `company_id` have a multi-company record rule in `security/security.xml`.
2. Check "Global" rules for unintended side effects on standard Odoo behavior.
3. Verify portal users (`base.group_portal`) are explicitly excluded from internal rules when needed.

## 3. Python Security

1. **Sudo escalation**: Grep for `.sudo()` — each instance must be justified. Never use `sudo()` in methods that are callable by standard or portal users without an explicit privilege check before the call.
2. **Raw SQL**: Every `env.cr.execute()` must use `%s` placeholders (never string interpolation). Flag any f-string or `.format()` in SQL queries.
3. **Hardcoded credentials**: Scan for API keys, passwords, or tokens in Python files and XML data.
4. **`eval()` / `exec()`**: Flag any usage. Odoo domain fields using `safe_eval()` are acceptable — bare `eval()` is not.

## 4. Odoo Framework Best Practices

- `@api.private` must be applied to methods that should never be called from RPC.
- `@api.ondelete(at_uninstall=False)` for delete prevention logic.
- **`t-raw` is unsafe** (deprecated in Odoo 17+, removed in 19): flag any remaining usage in QWeb templates. `t-out` is the safe replacement — it auto-escapes HTML output.
- JSON-RPC endpoints (`/web/dataset/call_kw`): verify they don't expose unintended model methods to unauthenticated users.

## 5. Portal & External API Security

1. Check `http.route` for any `auth="public"` or `auth="none"` routes — verify they serve only non-sensitive data.
2. For portal-accessible views, ensure `groups` attribute or `invisible` conditions prevent internal data exposure.
3. If the module exposes a REST API or webhooks, verify CSRF/token validation.

## 6. Report Findings

Severity scale for the final report:
- 🔴 **High**: Missing ACL, SQL injection risk, unguarded `sudo()`, exposed private method via RPC.
- 🟠 **Medium**: Incomplete record rules, weak auth in routes, missing `@api.private`.
- 🟡 **Low**: Missing `help=` strings on sensitive fields, non-explicit `groups=` on confidential fields.

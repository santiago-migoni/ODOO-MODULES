---
description: Protocolo acelerado de fix para bugs críticos en producción (Fase 7).
---
# Hotfix Workflow (Fase 7 — Mantenimiento)

Accelerated fix protocol for production-critical bugs that cannot wait for the normal release cycle.

The argument `$ARGUMENTS` contains the bug description and affected module.

---

## When to use this workflow vs `/fix-issue`

| Scenario | Workflow |
|---|---|
| Bug in development or staging, no user impact | `/fix-issue` |
| Bug in production, users affected, needs same-day fix | `/hotfix` (this workflow) |

> Six Sigma: a production bug is a DPMO (defect per million opportunities) event. Fix fast, but fix correctly — never apply a patch that creates a second defect.

---

## Step 1 — Triage (5 minutes max)

Answer immediately:
1. Is production currently **down** or just degraded? (Down = highest urgency)
2. How many users are affected?
3. Is there a workaround users can apply while the fix is being developed?
4. What is the exact error message and which module/action triggers it?

If production is fully down, notify stakeholders before writing any code.

## Step 2 — Create the hotfix branch

Branch **from production** (not from staging or a feature branch):

```bash
git checkout production
git pull origin production
git checkout -b fix/dipl_{module_name}_{short_description}
```

Example: `fix/dipl_sale_extra_compute_total_crash`

> Never branch from master/staging for a hotfix — you may include unreleased changes.

## Step 3 — Diagnose the root cause

Apply the 6-step process from `/fix-issue` but accelerated:

1. Get full stack trace from Odoo.sh logs.
2. Identify trigger path (model method, cron, controller, XML load).
3. Search codebase for the failure point.
4. **Propose the minimal fix** — present to user for approval even in hotfix mode.
5. Apply fix — single, surgical change, no refactors.
6. Verify no regressions with targeted search.

Consult `odoo-maintenance` skill for Odoo-specific edge cases.

**Propose-First rule still applies**, even under time pressure. A 2-minute review prevents a second production incident.

## Step 4 — Minimal QA (scoped to the fix only)

Do NOT run the full QA pipeline. Run only:
- [ ] **Targeted test**: add or update ONE test that covers the exact bug scenario.
- [ ] **Security check**: if the fix touches `sudo()`, ACLs, or controllers — run `/security-audit` on that file only.
- [ ] **Regression check**: grep for all usages of the changed method/field and verify none break.

Full `/perf-check` and `/security-audit` on the whole module are **deferred to the next normal release**.

## Step 5 — Deploy to staging first

```bash
git push origin fix/dipl_{module_name}_{short_description}
```

Merge to staging in Odoo.sh → wait for 🟢 build → run the specific failing scenario manually.

**Do not skip staging** — even for hotfixes. A 10-minute staging validation is always worth it.

## Step 6 — Deploy to production

1. Merge the `fix/` branch into production (via PR or direct merge).
2. Monitor the production build until 🟢.
3. Verify the specific scenario that was broken now works.
4. Monitor server logs for 30 minutes post-deploy.

If the build fails or introduces a new error: **revert immediately** (see rollback below).

## Step 7 — Post-hotfix actions

After production is stable:
1. Run `/changelog` → add entry under `Fixed` with patch version bump.
2. Document in `CHANGELOG.md`: root cause, fix, test added.
3. Merge the `fix/` branch back into the development/staging branches to keep them in sync.
4. Open a follow-up task for full QA (`/perf-check`, `/security-audit`) in the next sprint.

---

## Emergency Rollback Protocol

If the hotfix itself causes a new production failure:

```bash
# Revert the merge commit immediately
git revert -m 1 <merge-commit-sha>
git push origin production
```

Odoo.sh will rebuild from the reverted state. Monitor until 🟢.

If the database was corrupted: restore from the last Odoo.sh snapshot (Backups section).

**Never attempt a second fix on a broken production** — revert first, diagnose after.

---

## Principles

- **Minimal change**: one surgical fix only. No refactors, no improvements bundled in.
- **Speed with correctness**: fast is not the same as reckless — always propose before applying.
- **Document everything**: the root cause must be written down so it never recurs.
- **Adaptability**: if the fix is more complex than expected, escalate to a maintenance window instead of forcing an incomplete hotfix.

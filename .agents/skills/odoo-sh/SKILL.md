---
name: odoo-sh
description: >-
  Knowledge base for Odoo.sh ecosystem: deployment, monitoring, logs, staging
  vs production, submodules, and troubleshooting build failures. Use when
  deploying, configuring environments, or analyzing CI/CD issues in Odoo.sh.
---

# Odoo.sh Skill - Reference Guide

Guide for managing Dipleg's custom modules on the Odoo.sh platform.

## 1. Environment Architecture

Odoo.sh maps Git branches to environments:
- **Production**: The live database. Only merge after staging validation.
- **Staging**: Clone of production data. Use for final validation before production.
- **Development**: Transient environments per feature branch. Database is a dump of staging.

One branch = One environment. Never commit directly to the production branch.

## 2. Build Process

Every `git push` triggers an automated build:
- 🟢 **Success**: All modules installed/updated, tests passed.
- 🟡 **Warning**: Build completed with non-critical errors (e.g., deprecated API usage).
- 🔴 **Failure**: Module install failed, tests failed, or dependency missing.

## 3. Logs & Monitoring

Access via the Odoo.sh dashboard project page:
- **Install Logs**: Module-by-module install output. First place to check on failure.
- **Odoo Server Logs**: Runtime logs (`logging.info`, errors, tracebacks).
- **HTTP Logs**: Web request history.
- **Backups**: Daily automatic snapshots + manual on-demand snapshots.

## 4. Troubleshooting Build Failures (Red Build)

Systematic diagnosis — check in this order:
1. **Install Logs → look for**: `ImportError`, `SyntaxError`, `ValueError` in XML, missing `_inherit` target.
2. **Missing Odoo dependency**: Module name in `depends` doesn't match any installed or submodule module.
3. **External Python package missing**: Not listed in `requirements.txt` or `external_dependencies`.
4. **Data constraint error**: `UniqueViolation` or missing XML ID during `noupdate` data load.
5. **Test failure**: Check which test class/method failed and reproduce locally.

## 5. Staging → Production Workflow

1. Push to feature branch → development build.
2. Validate in development.
3. Merge to staging branch → build with production data clone.
4. Run full smoke test in staging.
5. Merge staging → production branch.
6. Monitor production build and server logs for 30 minutes post-deploy.

## 6. Emergency Rollback Protocol

If the production build fails after merge:
1. **Immediately revert** the merge commit: `git revert -m 1 <merge-commit-sha>` and push.
2. Odoo.sh will trigger a new build from the reverted state.
3. While the rollback builds, check "Backups" in the dashboard — restore the last snapshot if the DB was corrupted.
4. After rollback is green, diagnose the failure in a development branch before re-attempting.

## 7. Submodules (External Module Dependencies)

To include a module from an external repo (e.g., OCA):
1. Add as a Git submodule inside the repo:
   ```bash
   git submodule add -b 19.0 https://github.com/OCA/partner-contact.git .src/partner-contact
   ```
2. Add the needed module name to `depends` in `__manifest__.py`.
3. Odoo.sh detects submodules automatically — no extra config needed.
4. Keep submodule branch pinned to the same Odoo version (`19.0`).

## 8. Shell Access (Odoo.sh Editor Terminal)

The Odoo.sh web editor includes a terminal. Verified commands:
- `python odoo-bin shell -d <db>` — interactive Odoo shell.
- `python odoo-bin -u <module> -d <db> --stop-after-init` — update a module.
- `tail -f /var/log/odoo/odoo-server.log` — stream live logs.
- Standard `git`, `pip`, `psql` commands are available.

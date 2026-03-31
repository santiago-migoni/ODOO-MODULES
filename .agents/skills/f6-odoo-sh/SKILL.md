---
name: odoo-sh
description: >-
  Knowledge base for Odoo.sh ecosystem: deployment, monitoring, logs, staging
  vs production, submodules, and troubleshooting build failures. Use when
  deploying, configuring environments, or analyzing CI/CD issues in Odoo.sh.
---

> **Fase**: F6 — Deploy
> **Dónde estamos**: QA ha validado el código. Ahora lo movemos a través de los entornos de Odoo.sh hasta producción.
> **Qué hacer**: Validar en staging con datos reales, ejecutar migración, desplegar a producción, capacitar usuarios.
> **Cómo hacerlo**: Skill f6-odoo-sh + workflows /translate, /review-pr, /changelog, /deploy.
> **Por qué así**: Sin un proceso de staging con datos clonados de producción, los scripts de migración podrían fallar ante volúmenes reales de datos, causando downtime en Go-Live.

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

## Estrategia de 3 Ramas — Detalle Arquitectónico

### Development Branches (Ramas de Desarrollo)
- Cada requerimiento/bugfix/refactor se desarrolla en su propia rama aislada.
- Odoo.sh despliega un servidor Linux virtual + PostgreSQL **desde cero** con datos de demo.
- **Mail catchers**: Interceptores de correo electrónico y DNS simulados — no se envían correos reales.
- **Autodestrucción**: Las bases efímeras se eliminan tras un período de inactividad.
- Aquí se ejecutan pruebas destructivas sin impacto en operaciones.

### Staging Branches (Pre-producción)
- Las bases de datos son **clones bit-a-bit de producción** (con anonimización opcional).
- Epicentro del QA: UAT, validación de migración con datos históricos reales, pruebas de carga.
- Si se detecta una regresión, el código se intercepta antes del impacto comercial.
- Diferencia clave vs Development: datos reales en volúmenes reales.

### Production Branch
- Merge desde Staging solo tras evidencia concluyente de QA + validación del Project Leader.
- Odoo.sh ejecuta: detener servicio → instalar dependencias → actualizar ORM → re-enrutar tráfico HTTP.
- **Tiempo de inactividad prácticamente imperceptible**.

### Salvaguardas
- **Imposible** mover Production a Staging por drag-and-drop.
- **Imposible** mover Staging a Production sin git merge explícito.
- Gobernanza rigurosa impuesta por diseño arquitectónico de la plataforma.

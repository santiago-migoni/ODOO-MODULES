---
description: Checklist de deploy a Odoo.sh (staging -> prod).
---

> **Fase**: F6 — Deploy
> **Dónde estamos**: QA aprobado. Movemos código a producción a través de Odoo.sh.
> **Por qué esta fase**: Sin un proceso formal de deploy con staging, migración y validación, los defectos llegan directamente a la operación corporativa.
> **Habilita**: Fase 7 (Mantenimiento) — un deploy limpio minimiza hotfixes y establece la base para el siguiente ciclo iterativo.

# Deploy Workflow

Standardized process for deploying Dipleg custom modules to Odoo.sh.

The argument `$ARGUMENTS` contains the branch name to promote to production.

## 1. Staging validation gate

Before touching production, confirm all of the following:
- [ ] Staging build is 🟢 Green (no errors in Install Logs).
- [ ] Changes validated with real (cloned) production data in staging.
- [ ] All module tests passed — run via: `Settings → Technical → Automation → Run Tests` or by checking the Odoo.sh test report in the build detail page.
- [ ] `/perf-check` was executed and no Critical/High findings remain.
- [ ] `/security-audit` was executed and no High findings remain.

## 2. Pre-production checklist

- [ ] All `depends` modules are available in production.
- [ ] No `demo=True` data exists in the module.
- [ ] Migration scripts (`migrations/`) are present and tested if version changed.
- [ ] `i18n/es.po` is up-to-date.
- [ ] `CHANGELOG.md` reflects this release.

## 3. Deployment action

1. Merge the staging branch into the production branch (via GitHub PR or `git merge`).
2. Push triggers the Odoo.sh production build automatically.
3. Monitor the build in the Odoo.sh dashboard — do not leave until it turns 🟢.
4. Check Odoo Server Logs in the dashboard for the first 15 minutes post-deploy.

## 4. Post-deployment smoke test

Manually verify the core user flow affected by these changes in production. Confirm the feature works end-to-end with real data.

## 5. Emergency rollback protocol

If the production build fails or the feature causes critical errors after deploy:

1. **Revert the merge immediately**:
   ```bash
   git revert -m 1 <merge-commit-sha>
   git push origin production
   ```
2. Odoo.sh will rebuild from the reverted state — monitor until 🟢.
3. If the DB was corrupted (rare), restore from the last snapshot in Odoo.sh → Backups.
4. Open a fix branch from the reverted state. Do not re-merge until the root cause is resolved and validated in staging.

## Proceso de Migración Pre/Post

Si la versión del módulo ha cambiado y hay scripts de migración:

1. **Pre-migration**: Ejecuta ANTES de que el ORM actualice el schema.
   - Remapear claves, alterar constraints, transferir datos legacy.
   - Solo acceso a cursor SQL (`cr`), ORM no completamente disponible.
2. **Post-migration**: Ejecuta DESPUÉS de que el ORM ha aplicado el nuevo schema.
   - Computar valores de campos stored nuevos, normalizar datos, limpiar temporales.
   - ORM completo disponible vía `api.Environment(cr, SUPERUSER_ID, {})`.

Verificar en staging con datos clonados de producción ANTES de merge a producción.

## Gestión del Cambio — Go-Live

El Go-Live no es solo técnico — el factor humano es crítico:

- **Capacitación**: Usuarios finales deben operar sin soporte constante.
- **Monitoreo**: Primeros 30 minutos, 24 horas, 1 semana — con alertas activas.
- **Fricción esperada**: Hallazgos de UI, integraciones no previstas, nuevos ángulos de análisis.
- **Cierre de ciclo**: Todos los descubrimientos retroalimentan el backlog de la Fase 1.

## Cierre de Iteración

Al completar el deploy:
1. Documentar en CHANGELOG.md.
2. Registrar hallazgos post-deploy como tarjetas en el backlog.
3. Evaluar velocidad real del sprint vs estimada.
4. Preparar inputs para el siguiente ciclo de GAP Analysis.

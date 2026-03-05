# Migracion de Infraestructura ODOO al Modelo Odoo.sh

Este documento detalla como migrar el repositorio ODOO (infraestructura) para soportar el modelo de branches dinamicos de Odoo.sh, reemplazando los worktrees fijos actuales.

---

## 1. Estado actual de la infraestructura ODOO

### Worktrees fijos

El repositorio ODOO monta ODOO-MODULES mediante 3 worktrees fijos, cada uno vinculado a una rama:

| Worktree | Rama | Entorno |
|----------|------|---------|
| `modules/prod` | `main` | Produccion |
| `modules/stag` | `staging` | Staging |
| `modules/dev` | `development` | Desarrollo |

### Docker Compose

```yaml
# Cada servicio monta su worktree como addons
volumes:
  - ./modules/prod:/mnt/extra-addons   # web-prod-odoo
  - ./modules/stag:/mnt/extra-addons   # web-stag-odoo
  - ./modules/dev:/mnt/extra-addons    # web-dev-odoo
```

### Odoo config

```ini
# config/prod/odoo.conf (y equivalentes stag/dev)
addons_path = /mnt/extra-addons
```

### Makefile targets actuales

```makefile
mod-promote-dev    # feature -> development
mod-promote-stag   # development -> staging + deploy
mod-promote-main   # staging -> main + deploy
```

---

## 2. Modelo objetivo (Odoo.sh)

### Principios

- **`main` es la unica rama fija** (produccion)
- Feature branches son **efimeras** y se mueven entre etapas (Dev -> Staging -> Prod)
- **No existen ramas fijas** `staging` ni `development`
- Cada branch puede tener su propio entorno (container + base de datos)
- El merge a `main` via PR es el unico camino a produccion

### Flujo Odoo.sh

```
Feature branch  -->  Dev stage (entorno efimero)
                -->  Staging stage (copia de prod DB)
                -->  PR merge a main --> Produccion
```

---

## 3. Que debe cambiar en ODOO

### 3.1 docker-compose.yml

**Mantener**: `web-prod-odoo` fijo con `modules/prod` (worktree de `main`).

**Cambiar**: Los demas entornos se crean dinamicamente. No mas servicios fijos `web-stag-odoo` ni `web-dev-odoo`.

```yaml
# Fijo (no cambia)
web-prod-odoo:
  volumes:
    - ./modules/prod:/mnt/extra-addons

# Los entornos dev/staging se crean dinamicamente via PaaS dashboard
# o scripts de deploy, no como servicios fijos en docker-compose
```

### 3.2 Worktrees

**Eliminar**: Worktrees fijos `modules/stag` y `modules/dev`.

**Reemplazar con**: Worktrees dinamicos creados por el PaaS dashboard o scripts, similar al sistema de entornos efimeros que ya existe.

```bash
# Ejemplo: crear entorno efimero para branch feature/dipl_sale
git worktree add modules/feature-dipl_sale origin/feature/dipl_sale
# Se destruye cuando el branch se mergea o se abandona
```

### 3.3 Makefile

**Eliminar targets**:
- `mod-promote-dev`
- `mod-promote-stag`
- `mod-promote-main`

**Nuevo flujo**: No hay promocion manual. El camino es:
```
Push -> CI -> PR -> Review -> Merge a main -> Deploy prod automatico
```

### 3.4 PaaS Dashboard

Extender el sistema de entornos efimeros existente para soportar etapas como **labels** (Development, Staging), no como ramas fijas.

Funcionalidades necesarias:
- Crear entorno efimero desde cualquier branch
- Asignar etapa (Dev/Staging) al entorno
- Staging copia la base de datos de produccion
- Destruccion automatica al mergear/cerrar el branch

### 3.5 Webhook handler

Cambiar triggers de deploy:
- **Actual**: Detecta push a ramas fijas (`staging`, `development`)
- **Nuevo**: Detecta push a cualquier branch y crea/actualiza entorno efimero correspondiente
- Push a `main` -> deploy produccion (sin cambios)

### 3.6 Config files

- **Mantener**: `config/prod/odoo.conf` fijo
- **Cambiar**: Los demas configs se generan dinamicamente desde un template

```ini
# config/template/odoo.conf.tmpl
[options]
addons_path = /mnt/extra-addons
db_name = ${DB_NAME}
# ... resto de config parametrizada
```

---

## 4. Diagrama de flujo post-migracion

```
Developer
  |
  v
git push feature/dipl_xxx
  |
  v
Webhook detecta push
  |
  v
PaaS crea entorno efimero (etapa: Development)
  - git worktree add modules/<branch-slug> origin/<branch>
  - docker-compose up (servicio dinamico)
  - DB nueva o copiada segun etapa
  |
  v
QA mueve branch a etapa Staging
  - PaaS recrea entorno con copia de prod DB
  - Pruebas con datos reales
  |
  v
Aprobado -> PR merge a main
  |
  v
Webhook detecta push a main
  - Deploy produccion automatico
  - modules/prod se actualiza (git pull)
  - Odoo restart/update
  |
  v
Entorno efimero se destruye automaticamente
```

---

## 5. Plan de migracion paso a paso

### Fase 1: ODOO-MODULES adopta modelo Odoo.sh (este PR)

- [x] Eliminar archivos duplicados
- [x] README enfocado en desarrollo de modulos
- [x] Makefile sin targets de promocion
- [x] CI triggers en feature branches + PRs a main
- [ ] No eliminar ramas `staging`/`development` todavia

### Fase 2: ODOO adapta scripts de deploy

- [ ] Webhook handler soporta branches dinamicos
- [ ] PaaS dashboard soporta etapas como labels
- [ ] Template de config para entornos efimeros
- [ ] Scripts de creacion/destruccion de worktrees dinamicos

### Fase 3: Eliminar worktrees fijos de ODOO

- [ ] Remover `modules/stag` y `modules/dev` como worktrees fijos
- [ ] Remover servicios `web-stag-odoo` y `web-dev-odoo` de docker-compose
- [ ] Remover configs fijos de staging/dev

### Fase 4: Eliminar ramas legacy de ODOO-MODULES

- [ ] Eliminar rama `staging`
- [ ] Eliminar rama `development`
- [ ] Actualizar protecciones de rama en GitHub

---

## 6. Riesgos y consideraciones

### No romper produccion

- `main` y `modules/prod` **no cambian** en ninguna fase
- El deploy a produccion sigue igual (push a main -> deploy)
- El riesgo es cero para el entorno productivo

### Orden de migracion es critico

- **No eliminar** ramas `staging`/`development` de ODOO-MODULES hasta que ODOO tenga branches dinamicos funcionando (Fase 2 completa)
- Durante la transicion, ambos modelos coexisten

### Base existente

- El PaaS dashboard ya tiene la infraestructura para entornos efimeros
- Esta migracion extiende esa funcionalidad, no la reemplaza

### Rollback

- Si algo falla, revertir es simple: recrear worktrees fijos y restaurar targets del Makefile
- Las ramas `staging`/`development` siguen existiendo como respaldo hasta Fase 4

# CLAUDE.md — ODOO-MODULES

Repositorio de modulos Odoo custom de Dipleg. Compatible con Odoo.sh.

## Estructura

- Los modulos van en la **raiz** del repo (requerido por Odoo.sh)
- Cada directorio con `__manifest__.py` es un modulo instalable
- Archivos de soporte en carpetas dot-prefix: `.docs/`, `.config/`, `.github/`

## Convenciones de modulos

- Naming: `dipl_[nombre]` para modulos propios
- Version: `19.0.x.y.z` (Odoo 19)
- Licencia: `LGPL-3`
- Autor: `Dipleg`
- Dependencias Python extra en `requirements.txt`

## Branching

- `main` = produccion (unica rama fija)
- Feature branches: `feature/dipl_xxx`, `fix/dipl_xxx`, `hotfix/dipl_xxx`
- Flujo: branch desde main -> desarrollar -> PR a main

## Comandos

```bash
make mod-scaffold   # Crear modulo nuevo
make mod-branch     # Crear rama feature desde main
make lint           # flake8 (errores criticos)
make mod-format     # black (formateo)
make commit         # Add + commit interactivo
make push           # Push rama actual
```

## CI/CD

GitHub Actions ejecuta lint + tests en push a feature branches y PRs a `main`.

## Reglas para Claude

- No modificar `__manifest__.py` sin leer el archivo primero
- Respetar naming `dipl_*` para modulos nuevos
- No crear archivos de documentacion extra salvo que se pida
- Los modulos siempre van en la raiz, nunca en subdirectorios
- Usar Odoo 19 API (fields, models, controllers)
- Seguir OCA coding standards para Python en Odoo

---
description: Workflows interactivos y automáticos para Git y Commits
---

# Workflows de Git Commit

Procedimientos unificados para integrar cambios limpiamente en el repositorio.

## 1. Análisis de Contexto previo a Commit

Entender los cambios que están ocurriendo es siempre el primer paso:

```bash
# Opción 1: Validar únicamente lo que está Staged (listo para commit)
git diff --staged

# Opción 2: Validar todos los cambios locales desde el último commit (sin preparar)
git diff

# Listar el status a nivel general
git status --porcelain
```

## 2. Staging Estructurado e Inteligente

No uses un `git add .` a la ligera; agrupa los archivos por concepto:

```bash
# Por nombre o componente
git add src/components/Header.vue

# Por extensión relacionada a la capa técnica:
git add *.py

# Modo interactivo (seleccionar patch por patch)
git add -p
```

## 3. Formulación y Ejecución del Commit Convencional

Cuando ya están los archivos en área de _Staging_ (verificados sin secretos):

**Para cambios simples de una línea (One-liners):**

```bash
git commit -m "feat[core]: implementar login JWT para usuarios externos"
```

**Para cambios complejos que requieren cuerpo/nota:**

```bash
git commit -m "$(cat <<'EOF'
fix[billing]: resolver doble pago por race condition

El job cron no detectaba la transición de estado del procesador si la IP del webhook demoraba más de 300ms.

Closes #1234
EOF
)"
```

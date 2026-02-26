---
name: git-commit
description: 'Ejecuta git commit con análisis de mensajes de commit convencionales, staging inteligente y generación de mensajes. Úsalo cuando el usuario pida confirmar cambios, crear un commit de git o mencione "/commit". Soporta: (1) Autodetección de tipo y ámbito a partir de los cambios, (2) Generación de mensajes de commit convencionales desde el diff, (3) Commit interactivo con anulación opcional de tipo/ámbito/descripción, (4) Staging de archivos inteligente para agrupación lógica'
license: MIT
allowed-tools: Bash
---

# Git Commit con Commits Convencionales

## Resumen

Crea commits de git estandarizados y semánticos utilizando la especificación de Commits Convencionales (Conventional Commits). Analiza el diff real para determinar el tipo, ámbito y mensaje apropiados.

## Formato de Commit Convencional

```bash
<tipo>[ámbito opcional]: <descripción>

[cuerpo opcional]

[nota(s) al pie opcional(es)]
```

## Tipos de Commit

| Tipo       | Propósito                               |
| ---------- | --------------------------------------  |
| `feat`     | Nueva característica                    |
| `fix`      | Corrección de errores                   |
| `docs`     | Solo documentación                      |
| `style`    | Formato/estilo (sin lógica)             |
| `refactor` | Refactorización de código (sin feat/fix)|
| `perf`     | Mejora de rendimiento                   |
| `test`     | Añadir/actualizar pruebas               |
| `build`    | Sistema de construcción/dependencias    |
| `ci`       | Cambios en CI/configuración             |
| `chore`    | Mantenimiento/varios                    |
| `revert`   | Revertir commit                         |

## Cambios Importantes (Breaking Changes)

```bash
# Signo de exclamación después del tipo/ámbito
feat!: eliminar endpoint obsoleto

# Nota al pie BREAKING CHANGE
feat: permitir que la configuración extienda otras
 
BREAKING CHANGE: cambió el comportamiento de la clave `extends`
```

## Flujo de Trabajo

### 1. Analizar el Diff

```bash
# Si los archivos están en el área de preparación (staged), usa el diff de staged
git diff --staged

# Si no hay nada preparado, usa el diff del árbol de trabajo
git diff

# También comprueba el estado
git status --porcelain
```

### 2. Preparar Archivos (si es necesario)

Si no hay nada preparado o quieres agrupar los cambios de forma diferente:

```bash
# Preparar archivos específicos
git add ruta/al/archivo1 ruta/al/archivo2

# Preparar por patrón
git add *.test.*
git add src/components/*

# Preparación interactiva
git add -p
```

**Nunca hagas commit de secretos** (.env, credentials.json, claves privadas).

### 3. Generar Mensaje de Commit

Analiza el diff para determinar:

- **Tipo**: ¿Qué tipo de cambio es este?
- **Ámbito**: ¿Qué área/módulo se ve afectado?
- **Descripción**: Resumen de una línea de lo que cambió (tiempo presente, modo imperativo, <72 caracteres)

### 4. Ejecutar el Commit

```bash
# Una sola línea
git commit -m "<tipo>[ámbito]: <descripción>"

# Multilínea con cuerpo/nota al pie
git commit -m "$(cat <<'EOF'
<tipo>[ámbito]: <descripción>

<cuerpo opcional>

<nota al pie opcional>
EOF
)"
```

## Buenas Prácticas

- Un cambio lógico por commit
- Tiempo presente: "add" no "added" (añadir, no añadió)
- Modo imperativo: "fix bug" no "fixes bug" (corregir error, no corrige error)
- Referencia a problemas: `Closes #123`, `Refs #456`
- Mantener la descripción por debajo de los 72 caracteres

## Protocolo de Seguridad de Git

- NUNCA actualices la configuración de git
- NUNCA ejecutes comandos destructivos (--force, hard reset) sin una petición explícita
- NUNCA omitas los hooks (--no-verify) a menos que el usuario lo pida
- NUNCA fuerces el push a main/master
- Si el commit falla debido a los hooks, corrígelo y crea un NUEVO commit (no uses amend)

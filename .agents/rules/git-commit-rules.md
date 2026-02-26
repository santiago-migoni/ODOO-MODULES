---
trigger: always_on
glob: 
description: Reglas y restricciones de seguridad para las operaciones de Git Commit
---

# Reglas de Git Commit

Basado en la skill `git-commit` y el uso de **Conventional Commits**.

## 1. Formato Strict "Conventional Commits"

Todos los mensajes de commit deben seguir exactamente este formato:
`<tipo>[ámbito opcional]: <descripción>`

### Tipos Permitidos

- `feat`: Nueva característica.
- `fix`: Corrección de un error.
- `docs`: Modificaciones exclusivas de documentación.
- `style`: Estilo de código (espacios, comas, formateo de código).
- `refactor`: Refactorización que no añade funcionalidad ni arregla bugs.
- `perf`: Mejoras de rendimiento.
- `test`: Añadido interno o arreglos de pruebas (unit/integration tests).
- `build` / `ci`: Cambios a dependencias o scripts de despliegue.
- `chore`: Mantenimiento y tareas rutinas diversas.

### Reglas de Estilo de la Descripción

- Máximo de **72 caracteres**.
- Debe escribirse en **tiempo presente y modo imperativo** (ej. "add config file" o "añadir archivo de config"). No usar pasado (added, fix).
- Rompimientos de retrocompatibilidad deben expresarse con un `!` antes de los dos puntos o un pie de página `BREAKING CHANGE: ...`.

## 2. Reglas de Inclusión (Staging)

- **Compromiso Único**: Agrupar los cambios de manera que cada commit refleje un cambio lógico único.
- **Protección de Datos Sensibles**: **NUNCA** hacer commit de secretos, credenciales (ej. `credentials.json`, claves privadas) o archivos como `.env`.

## 3. Restricciones de Seguridad de Git

- **NUNCA** alterar configuraciones subyacentes de git del entorno local a menos que se instruya directamente.
- **NUNCA** ejecutar comandos destructivos como `git reset --hard` o `git push --force` proactivamente.
- **NUNCA** saltar las barreras de pre-commit con `--no-verify`.
- **NUNCA** forzar pushes a las ramas principales (`main` o `master`).
- Si un hook de commit rechaza el cambio, no forzar un amend ciego; resolver el problema de código y crear un nuevo intento limpio.

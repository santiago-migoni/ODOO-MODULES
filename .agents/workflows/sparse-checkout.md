---
description: Configura sparse-checkout para trabajar solo con los módulos necesarios.
---
# Sparse Checkout — Seleccionar módulos para desarrollo local

Configura git sparse-checkout para mostrar solo los módulos que necesitás, reduciendo el ruido visual en el editor.

## Steps

1. **Verificar estado**: Comprobar si sparse-checkout ya está configurado:
   `git sparse-checkout list`
   Si ya está activo, mostrar los paths actuales y preguntar si se quiere reconfigurar.

2. **Detectar módulos disponibles**: Listar todos los módulos en el repo (directorios con `__manifest__.py`):
   `find . -maxdepth 2 -name '__manifest__.py' -not -path './.src/*' | sed 's|/.__manifest__.py||' | sed 's|^\./||' | sort`

3. **Preguntar al usuario**: Presentar las opciones:
   - **Nuevo módulo**: No necesita módulos existentes, solo crear el directorio.
   - **Módulos específicos**: El usuario indica cuáles necesita (uno o varios).
   - **Todos**: Desactivar sparse-checkout y mostrar todo.

4. **Ejecutar sparse-checkout**:
   - Si el usuario elige **nuevo módulo** o **módulos específicos**:
     ```bash
     git sparse-checkout init --cone
     git sparse-checkout set .agents docs src {módulos seleccionados}
     ```
     `.agents`, `docs` y `src` siempre se incluyen — son esenciales para el desarrollo.
   - Si el usuario elige **todos**:
     ```bash
     git sparse-checkout disable
     ```

5. **Verificar resultado**: Ejecutar `ls` y confirmar que solo se ven los módulos seleccionados más las carpetas de soporte.

## Agregar módulos después

Si el usuario necesita agregar más módulos sin perder los actuales:
```bash
git sparse-checkout add {nuevo_módulo}
```

## Notas
- Sparse-checkout solo controla qué se **muestra** localmente. Todos los módulos siguen existiendo en git.
- Los commits, push y pull funcionan normalmente — no afecta el flujo de git.
- Para volver a ver todo: `git sparse-checkout disable`.

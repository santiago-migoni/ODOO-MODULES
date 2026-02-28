# Guía de Comandos de Desarrollo (ODOO-MODULES Repo)

Esta guía detalla los comandos disponibles en el repositorio `ODOO-MODULES`.
**Este repositorio es tu "Fábrica de Código". Aquí se construyen los módulos, se crean ramas y se gestiona el versionado.**

---

## 🏭 Terminal 2: ODOO-MODULES (Desarrollo)

Usa estos comandos mientras programas tus módulos.

### 1. Iniciar un Nuevo Trabajo y Preparar Entorno

| Comando | Acción |
| :--- | :--- |
| **`make help`**      | Muestra la lista de todos los comandos disponibles con una breve descripción. |
| **`make init`**      | Instala hooks de git (pre-commit) y dependencias necesarias para desarrollo local. |
| **`make scaffold`**  | **Tu primer paso**: Crea la estructura básica de un nuevo módulo. <br>Genera: `models/`, `views/`, `__manifest__.py`, etc. Te pedirá el nombre técnico. |
| **`make branch`**    | Crea una nueva rama `feature/` sincronizada con `development`.<br>Úsalo siempre antes de empezar una nueva tarea para mantener el orden. |

### 2. Guardar y Compartir

| Comando | Acción |
| :--- | :--- |
| **`make commit`**    | Asistente interactivo para hacer commits convencionales (ej: `feat(ventas): agrega descuento`).<br>Te preguntará tipo, ámbito y descripción. ¡Mantiene el historial limpio! |
| **`make push`**      | Sube tu rama actual a GitHub (simplifica el `git push -u origin...`). |
| **`make pr`**        | Si tienes la CLI de GitHub (`gh`) instalada, te abre la URL para crear un Pull Request. |

### 3. Calidad de Código

| Comando | Acción |
| :--- | :--- |
| **`make lint`**      | Revisa tu código Python en busca de errores de sintaxis y asegura que cumples el estándar PEP8 (usando `flake8`). |
| **`make format`**    | Formatea tu código automáticamente usando `black` (si está instalado). |

---

## Flujo de Trabajo Recomendado

1. **Crear Módulo**: `make scaffold` -> `dipl_sales_custom`
2. **Crear Rama**: `make branch` -> `sales-custom-logic`
3. **Programar**: Editar archivos `.py` y `.xml`.
4. **Verificar**: `make lint`
5. **Guardar**: `make commit` -> `feat(sales): add custom logic`
6. **Subir**: `make push`
7. **Desplegar**: Ir a la **Terminal 1 (ODOO)** y ejecutar `make deploy-dev`.

---

**Última actualización**: 19 de febrero de 2026

# ODOO-MODULES

Repositorio de módulos Odoo 19 custom de **Dipleg**. Compatible con Odoo.sh sin modificaciones.

---

## Estructura del repositorio

```
ODOO-MODULES/
├── dipl_{nombre}/              # Módulos custom Dipleg (en la raíz del repo)
├── .agents/                    # Ecosistema de desarrollo con IA (skills + workflows)
│   ├── skills/                 # Conocimiento especializado del agente
│   └── workflows/              # Comandos /slash automatizados
├── src/                        # Código fuente de Odoo Community (solo referencia, NO módulos)
├── docs/                       # Documentación interna
├── .gitignore
├── GEMINI.md                   # Constitución y reglas del repositorio
├── README.md
└── requirements.txt
```

Los módulos custom van directamente en la **raíz del repositorio**. Cada directorio con `__manifest__.py` es un módulo Odoo instalable. La carpeta `src/` contiene el código fuente de Odoo Community clonado para referencia — no se monta en el servidor. Los directorios dot-prefix (`.agents/`) son de soporte.

---

## Ecosistema de desarrollo con IA

El directorio `.agents/` contiene un sistema completo de asistencia para el ciclo de vida del desarrollo. Sigue filosofía **Lean** y **Six Sigma**: sin desperdicios, cero defectos y protocolos de recuperación ante fallos.

### GEMINI.md — Constitución del repositorio

El archivo [`GEMINI.md`](./GEMINI.md) es el documento central que gobierna todo el desarrollo. Define:

- **Estrategia Propose-First**: El agente nunca edita código sin presentar primero un plan técnico aprobado.
- **Formato de propuesta estándar**: Goal → Plan → Files → Tests/Checks → Risks.
- **Quality Gates**: Checklist no negociable antes de cerrar cualquier tarea (Tests, Seguridad, Performance, Traducciones).
- **Guía de activación de skills**: Qué skill consultar automáticamente según la situación.
- **Convenciones Odoo 19**: Reglas técnicas obligatorias (`<list>`, `invisible=`, N+1, etc.).
- **Git Flow**: Naming de ramas y commits convencionales.
- **Debugging Approach**: 6 pasos sistemáticos para diagnosticar bugs de raíz.
- **Missing Context Protocol**: Qué preguntar antes de asumir modelo, XML IDs o grupos de seguridad.

---

### Skills disponibles

Las skills son las guías de referencia especializadas del agente.

| Skill | Propósito | Cuándo se activa |
|---|---|---|
| `odoo-19` | API completa de Odoo 19 (18 guías: modelos, vistas, OWL, etc.) | Siempre que se escribe o revisa código Odoo |
| `odoo-sh` | Plataforma Odoo.sh: builds, logs, staging, rollback de emergencia | Al desplegar o diagnosticar fallos de build |
| `odoo-module-patterns` | Arquitectura: herencia, patrones de UI, modelos de datos, performance | Al diseñar una feature o módulo nuevo |
| `python-pro` | Python 3.11+ avanzado: tipado, async, testing con pytest | Lógica compleja fuera del framework Odoo |
| `scrum-master` | Gestión ágil: user stories, story points, sprints | Planificación y estimación |

#### `odoo-module-patterns` — Guías de referencia

| Guía | Contenido |
|---|---|
| `extend-vs-create.md` | Cuándo usar `_inherit`, `_inherits`, mixin o modelo nuevo |
| `module-dependencies.md` | Dependencias locales, Python, OS y resolución de dependencias circulares |
| `data-model-patterns.md` | State machines, relaciones parent-child, campos multi-compañía |
| `ui-patterns.md` | Snippets completos: Wizard, Smart Button, Status Bar, Chatter |
| `performance-patterns.md` | Prevención N+1, `read_group()`, decisión `store=True`, migraciones masivas |

**Code Templates** (copiar y adaptar):

| Template | Contenido |
|---|---|
| `model-pattern.md` | Modelo completo con fields, compute, constraints y actions |
| `inherit-pattern.md` | Extensión de modelos estándar de Odoo (`res.partner`, etc.) |
| `wizard-pattern.md` | TransientModel + vista XML + entrada de ACL |
| `view-pattern.md` | Form, list, search, action y menuitem |
| `test-pattern.md` | TransactionCase con setUpClass y prioridades de cobertura |
| `controller-pattern.md` | Endpoints HTTP/JSON y rutas de descarga de archivos |


---

### Comandos disponibles (`/slash-command`)

| Comando | Qué hace |
|---|---|
| `/scaffold-module` | Crea un módulo nuevo con estructura completa. Soporta multi-compañía y OWL. |
| `/new-feature` | Guía para agregar funcionalidad a un módulo existente con análisis técnico, propuesta y verificación. |
| `/add-field` | Agrega campos a modelos: Python + XML + script de migración si el módulo ya está en producción. |
| `/add-wizard` | Crea un `TransientModel` con vista de formulario, botones y binding al modelo origen. |
| `/add-report` | Genera un reporte QWeb (PDF con `external_layout` o HTML) con acción de impresión. |
| `/generate-tests` | Genera `TransactionCase` o `HttpCase` para cubrir campos computados, constraints y flujos de estado. |
| `/translate` | Escanea el código y actualiza `i18n/es.po` con todos los strings traducibles. |
| `/security-audit` | Audita ACLs, Record Rules, uso de `sudo()`, rutas HTTP y seguridad de usuarios portal. |
| `/perf-check` | Detecta consultas N+1, `@api.depends` sobreactivados e índices faltantes. |
| `/deploy` | Checklist de deploy a Odoo.sh (staging → producción) con protocolo de rollback de emergencia. |
| `/fix-issue` | Diagnóstico y reparación de bugs con análisis de causa raíz en 6 pasos. |
| `/review-pr` | Revisión de Pull Requests con checklist específico de Odoo 19. |
| `/explain` | Explica código en detalle: qué hace, cómo funciona y por qué está escrito así. |
| `/clone-odoo` | Clona el repositorio oficial de Odoo Community 19.0 como referencia. |

---

## Estructura de un módulo

### Convenciones de naming

| Concepto | Convención |
|---|---|
| Nombre técnico | `dipl_<nombre>` (siempre con prefijo) |
| Versión | `19.0.x.y.z` |
| Licencia | `LGPL-3` |
| Autor | `Dipleg` |
| Ramas Git | `feature/`, `fix/`, `release/` |
| Commits | `feat:`, `fix:`, `docs:`, `test:`, `refactor:` |

### `__manifest__.py`

```python
{
    "name": "Dipleg - Sale Extra",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Descripción breve del módulo",
    "author": "Dipleg",
    "website": "https://dipleg.com",
    "license": "LGPL-3",
    "depends": ["base", "mail"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
```

### Estructura base generada por `/scaffold-module`

```
dipl_{name}/
├── __init__.py
├── __manifest__.py
├── CHANGELOG.md
├── models/
│   ├── __init__.py
│   └── {name}.py
├── views/
│   ├── {name}_views.xml
│   └── menus.xml
├── security/
│   ├── ir.model.access.csv
│   └── security.xml
├── tests/
│   ├── __init__.py
│   └── test_{name}.py
└── i18n/
    └── es.po
```

Directorios opcionales según necesidad: `wizards/`, `report/`, `static/src/` (OWL).

---

## Flujo de trabajo estándar

```
1. git checkout -b feature/dipl_xxx
2. Usar /scaffold-module o /new-feature para planificar
3. Esperar aprobación del plan técnico (Propose-First)
4. Implementar en orden: models → security → views → tests → i18n
5. Validar Quality Gates (tests, seguridad, performance, traducciones)
6. Push y crear PR → usar /review-pr para auditar antes del merge
7. Merge a staging en Odoo.sh → validar con datos reales
8. Merge a producción usando /deploy con checklist completo
```

---

## Dependencias Python

Agregar en [`requirements.txt`](./requirements.txt). Odoo.sh las instala automáticamente.

Declarar también en `__manifest__.py`:

```python
"external_dependencies": {
    "python": ["nombre_paquete"],
},
```

---

## Compatibilidad Odoo.sh

Este repositorio funciona directamente como repositorio de módulos en Odoo.sh:

- Módulos custom en la **raíz del repo** con `__manifest__.py` y `installable: True`.
- `requirements.txt` en la raíz para dependencias Python.
- `packages.txt` en la raíz para dependencias de SO (si aplica).
- Submodules Git para dependencias de repos externos (ej. OCA).
- La carpeta `src/` **no se monta** — es solo referencia del código fuente de Odoo.
- Sin configuración adicional necesaria.

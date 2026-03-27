# ODOO-MODULES

Repositorio de modulos Odoo 19 custom de **Dipleg**. Compatible con Odoo.sh sin modificaciones.

## Estructura del repositorio

```
ODOO-MODULES/
|-- dipl_web_ui_enhanced/       # Modulo custom Dipleg
|-- ica_web_responsive/         # Modulo forkeado
|-- .agents/                    # Antigravity agent
|-- .claude/                    # Claude Code settings
|-- .docs/                      # Documentacion interna
|-- .src/                       # Community/Enterprise/Upstream (referencia, NO en Docker)
|-- .gitignore
|-- CLAUDE.md
|-- Makefile
|-- README.md
|-- requirements.txt
```

Cada directorio en la raiz con `__manifest__.py` es un modulo Odoo instalable. Los directorios dot-prefix (`.agents/`, `.src/`, etc.) son de soporte y no se montan en el servidor.

## Crear un modulo nuevo

```bash
make scaffold
```

Pide nombre tecnico y categoria, genera la estructura completa:

```
dipl_sale_extra/
|-- __init__.py
|-- __manifest__.py
|-- models/
|   |-- __init__.py
|-- views/
|   |-- views.xml
|-- security/
|   |-- ir.model.access.csv
|-- data/
|-- static/
    |-- description/
```

Directorios adicionales segun necesidad: `controllers/`, `tests/`, `i18n/`, `wizards/`, `reports/`.

## Estructura de un modulo

### `__manifest__.py`

```python
{
    'name': 'Dipleg Sale Extra',
    'version': '19.0.1.0.0',
    'category': 'Sales',
    'summary': 'Descripcion breve del modulo',
    'author': 'Dipleg',
    'website': 'https://dipleg.com',
    'license': 'LGPL-3',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'dipl_sale_extra/static/src/**/*',
        ],
    },
    'installable': True,
    'application': False,
}
```

### `__init__.py`

```python
from . import models
from . import controllers  # si aplica
```

## Flujo de trabajo

```
1. git checkout main && git pull
2. git checkout -b feature/dipl_xxx
3. Desarrollar + probar localmente
4. make lint
5. make check
6. make commit
7. make push
8. Crear PR hacia main → Review → Merge
```

## Comandos

```bash
make help       # Muestra todos los comandos
make scaffold   # Crea modulo nuevo con estructura estandar
make commit     # Add + commit interactivo
make push       # Push rama actual a origin
make pull       # Pull rama actual desde origin
make lint       # black (formateo) + flake8 (errores criticos)
make list       # Lista modulos del repo con version y summary
make check      # Valida manifests contra convenciones Dipleg
```

## Convenciones

| Concepto | Convencion |
|----------|-----------|
| Nombre de modulo | `dipl_[nombre]` para propios, nombre original para forks |
| Version | `19.0.x.y.z` (version Odoo . major . minor . patch) |
| Licencia | `LGPL-3` |
| Autor | `Dipleg` |
| Ramas | `feature/dipl_xxx`, `fix/dipl_xxx`, `hotfix/dipl_xxx` |

## Dependencias Python

Agregar dependencias extra en [`requirements.txt`](./requirements.txt). Odoo.sh las instala automaticamente.

## Compatibilidad Odoo.sh

Este repositorio funciona directamente como repositorio de modulos en Odoo.sh:

- Modulos en la raiz del repo (sin subdirectorios extra)
- `requirements.txt` en la raiz para dependencias Python
- `__manifest__.py` estandar con `installable: True`
- Sin configuracion adicional necesaria

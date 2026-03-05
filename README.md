# ODOO-MODULES

Repositorio de modulos Odoo custom de **Dipleg**. Compatible con Odoo.sh sin modificaciones.

## Estructura del repositorio

```
ODOO-MODULES/
|-- dipl_modulo_a/          # Modulo custom
|-- dipl_modulo_b/          # Otro modulo custom
|-- ica_web_responsive/     # Modulo forkeado
|-- requirements.txt        # Dependencias Python adicionales
|-- Makefile                # Comandos de desarrollo
|-- .github/workflows/      # CI/CD (lint + tests)
```

Cada directorio en la raiz con `__manifest__.py` es un modulo Odoo instalable.

## Crear un modulo nuevo

```bash
make mod-scaffold
```

Esto genera la estructura base con el nombre que indiques (ej: `dipl_sale_extra`):

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
5. git add + git commit
6. git push -u origin feature/dipl_xxx
7. Crear PR hacia main
8. Review + merge
```

O usa el atajo:

```bash
make mod-branch    # Crea rama feature desde main
make commit        # Add + commit interactivo
make push          # Push de la rama actual
```

## Convenciones

| Concepto | Convencion |
|----------|-----------|
| Nombre de modulo | `dipl_[nombre]` para propios, nombre original para forks |
| Version | `19.0.x.y.z` (mayor Odoo . major . minor . patch) |
| Licencia | `LGPL-3` |
| Autor | `Dipleg` |
| Ramas | `feature/dipl_xxx`, `fix/dipl_xxx`, `hotfix/dipl_xxx` |

## Dependencias Python

Agregar dependencias extra en [`requirements.txt`](./requirements.txt). Odoo.sh las instala automaticamente.

## Calidad de codigo

```bash
make lint          # flake8 (errores criticos)
make mod-format    # black (formateo automatico)
```

## CI/CD

El workflow de GitHub Actions ejecuta automaticamente en cada push a ramas feature y PRs a `main`:

1. **Lint** (flake8) -- errores criticos
2. **Tests** (Odoo) -- modulos que tengan directorio `tests/`
3. **Notificacion** al webhook handler con el resultado

## Compatibilidad Odoo.sh

Este repositorio funciona directamente como repositorio de modulos en Odoo.sh:

- Modulos en la raiz del repo (sin subdirectorios extra)
- `requirements.txt` en la raiz para dependencias Python
- `__manifest__.py` estandar con `installable: True`
- Sin configuracion adicional necesaria

# ODOO-MODULES

Repositorio de módulos Odoo custom de **Dipleg**.

## Estructura de Branches

| Branch | Entorno | Descripción |
|---|---|---|
| `main` | Producción | Código estable aprobado |
| `staging` | Staging | En validación con datos reales |
| `development` | Dev | Integración de features |
| `feature/dipl_xxx` | Dev | Desarrollo activo de un módulo |

## Flujo de Promoción

```
feature/dipl_xxx → development → staging → main
```

## Módulos

### Custom (100% Dipleg)

- `dipl_ui_app_interface` — Interfaz de la app

### Forks (upstream customizados)

- _Agregar módulos forkeados aquí_

## Convenciones de Naming

- Módulos propios: `dipl_[nombre]`
- Forks customizados: mantener nombre original o renombrar a `dipl_[nombre]` si se refactoriza completamente

## Dependencias Python

Ver [`requirements.txt`](./requirements.txt)

---
trigger:
globs: "modules/**/*"
description: Module structure and naming conventions (dipl_ prefix)
phase: f3-f4
---

# structure-and-naming

Module structure & naming are mandatory:

- Module technical name must follow: `dipl_<module_name>`.
- Versioning conventions follow the repository/scaffold rules.
- XML IDs must be namespaced (include the module technical prefix) and must be stable.
- Security files belong under `security/` (`ir.model.access.csv` and rules XML when applicable).
- `company_id` and multi-company considerations must be considered from the start when the model is multi-company.

## Standard Directory Structure

| Directory | Technical Function |
| --- | --- |
| `models/` | Python source files defining business object classes, business logic, and ORM database interactions. |
| `views/` | XML files structuring UI (forms, lists, kanban, pivot, graphs) and rendering model data to the web client. |
| `controllers/` | Python HTTP controllers handling custom web routing, external requests, and portal/API integration logic. |
| `static/` | Static web assets organized in subdirectories: `css/`, `js/`, `src/`, `components/`, `img/`. Home of OWL frontend logic. |
| `data/` | XML/CSV files for initializing essential parametrizations and default settings. |
| `demo/` | XML/CSV files providing fake records exclusively for test/development environments. |
| `security/` | Access control definitions: `ir.model.access.csv` for CRUD permissions, XML for user groups and record rules (`ir.rule`). |
| `wizards/` | Transient models (`models.TransientModel`) and their views for interactive modal interfaces and batch processing. |
| `report/` | SQL-based report models and QWeb printable templates (PDFs) for invoicing, management analysis, and accounting. |
| `i18n/` | Translation files (`.po`). Base strings in English, output in `es.po`. |

## File Naming Convention

- Python files: `snake_case.py` (e.g., `plant_nursery.py`).
- XML files: model name + resource suffix (e.g., `plant_nursery_views.xml`, `plant_nursery_demo.xml`).
- This separation of Backend (models/) / Frontend (views/, static/) / Security (security/) enables parallel development across team members.

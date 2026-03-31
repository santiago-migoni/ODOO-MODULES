# ODOO-MODULES

Custom Odoo 19 module repository for **Dipleg**. Compatible with Odoo.sh out of the box.

---

## Repository Structure

```
ODOO-MODULES/
├── dipl_{name}/                # Dipleg custom modules (at repo root)
├── .agents/                    # AI-powered development ecosystem (skills + workflows + rules)
│   ├── rules/                  # Mandatory rules (10 rules: 00-09)
│   ├── skills/                 # Phase-coded specialized knowledge (8 skills)
│   └── workflows/              # Automated /slash commands (18 workflows)
├── .src/                       # Odoo Community source code (reference only, NOT mounted)
├── .docs/                      # Internal documentation
├── .gitignore
├── GEMINI.md                   # Repository constitution and rules
├── README.md
└── requirements.txt
```

Custom modules go directly at the **repository root**. Each directory with `__manifest__.py` is an installable Odoo module. The `src/` folder contains the Odoo Community source code cloned for reference — it is not mounted on the server. Dot-prefixed directories (`.agents/`) are support infrastructure.

---

## AI-Powered Development Ecosystem

The `.agents/` directory contains a complete development lifecycle assistance system, organized by iterative SDLC phases. Follows **Lean** and **Six Sigma** philosophy: zero waste, zero defects, and failure recovery protocols.

### GEMINI.md — Repository Constitution

The [`GEMINI.md`](./GEMINI.md) file is the central document governing all development. It defines:

- **8-Phase Iterative SDLC** (F0-F7): Each phase documents where we are, what to do, how to do it, and why it enables the next phase.
- **Propose-First Strategy**: The agent never edits code without presenting an approved technical plan first.
- **Quality Gates**: Non-negotiable checklist before closing any task.
- **Odoo 19 Conventions**: Mandatory technical rules (`<list>`, `invisible=`, `models.Constraint`, etc.).
- **Git Flow**: Branch naming and conventional commits.

---

### Available Skills (by phase)

Skills are the agent's specialized reference guides, phase-coded within the SDLC.

| Skill | Phase | Purpose | Activation Trigger |
|---|---|---|---|
| `f0-enterprise-sdlc` | F0 | SDLC foundational framework, GAP Analysis, change management | Project kickoff, initial planning |
| `f1-scrum-master` | F1 | Sprint planning, story points, backlog, cross-functional teams | Planning and estimation |
| `f2-odoo-analysis` | F2 | Existing code mapping, impact analysis, dependencies | Before designing changes |
| `f3-module-patterns` | F3 | Module architecture, inheritance, data model, UI patterns | Designing features or new modules |
| `g-odoo-19` | Global | Complete Odoo 19 API (22 references: ORM, views, OWL, themes, etc.) | Whenever writing or reviewing Odoo code |
| `f5-odoo-qa` | F5 | 5-level QA pyramid, Form helper, HOOT, E2E Tours | Testing and pre-deploy validation |
| `f6-odoo-sh` | F6 | Odoo.sh platform: 3-branch strategy, builds, staging, rollback | Deploy and build diagnostics |
| `f7-odoo-maintenance` | F7 | Hotfixes, semantic versioning, pre/post migration, cyclic closure | Post-deploy and maintenance |

#### `g-odoo-19` — 22 Specialized References

| Category | References |
|---|---|
| **Constraints** (MUST DO / MUST NOT DO) | Backend (ORM/Python), Views (XML/UI), OWL (JS/Frontend), Theme (SCSS/Bootstrap/Reports) |
| **API Guides** (18 guides) | Actions, Controllers, Data, Decorators, Development, Fields, Manifest, Migration, Mixins, Models, OWL, Performance, Reports, Security, Testing, Transactions, Translation, Views |

#### `f3-module-patterns` — Reference Guides

| Guide | Content |
|---|---|
| `extend-vs-create.md` | When to use `_inherit`, `_inherits`, mixin, or new model |
| `module-dependencies.md` | Local, Python, OS dependencies and circular dependency resolution |
| `data-model-patterns.md` | State machines, parent-child relations, multi-company fields |
| `ui-patterns.md` | Complete snippets: Wizard, Smart Button, Status Bar, Chatter |
| `performance-patterns.md` | N+1 prevention, `read_group()`, `store=True` decisions, bulk migrations |

**Code Templates** (copy and adapt):

| Template | Content |
|---|---|
| `model-pattern.md` | Complete model with fields, compute, constraints, and actions |
| `inherit-pattern.md` | Standard model extension (`res.partner`, etc.) |
| `wizard-pattern.md` | TransientModel + XML view + ACL entry |
| `view-pattern.md` | Form, list, search, action, and menuitem |
| `test-pattern.md` | TransactionCase with setUpClass and coverage priorities |
| `controller-pattern.md` | HTTP/JSON endpoints and file download routes |

---

### Rules (mandatory)

| Rule | Phase | Purpose |
|---|---|---|
| `00-global-config` | Global | Base configuration: Odoo 19, LGPL-3, Dipleg, languages |
| `01-propose-first` | Global | Always propose before editing |
| `02-odoo-19-conventions` | F4 | ORM conventions, computed fields, batch ops |
| `03-quality-gates` | F5 | Tests, security, performance, translations |
| `04-translation-standard` | Global | i18n/es.po, no en.po |
| `05-structure-and-naming` | F3-F4 | `dipl_` prefix, standard directories, XML IDs |
| `06-inheritance-strategy` | F3 | 3 inheritance paradigms with DB implications |
| `07-security-architecture` | F4-F5 | ACL, record rules, AND/OR logic |
| `08-migration-protocol` | F6-F7 | Pre/post scripts, manifest hooks |
| `09-owl-frontend` | F4 | 4 OWL pillars, asset bundles, registry |

---

### Available Commands (`/slash-command`)

| Command | Phase | Description |
|---|---|---|
| `/clone-odoo` | F0 | Clone official Odoo Community 19.0 repository as reference. |
| `/sparse-checkout` | F0 | Filter VS Code workspace to show only relevant modules. |
| `/plan-module` | F1 | Capture requirements with GAP Analysis and generate prioritized backlog. |
| `/explain` | F2 | Analyze and explain existing code with full context. |
| `/scaffold-module` | F3 | Create a new module with complete structure. Supports multi-company and OWL. |
| `/new-feature` | F3 | Guide for adding functionality with impact analysis and technical proposal. |
| `/add-field` | F4 | Add fields to models: Python + XML + migration script. |
| `/add-wizard` | F4 | Create a `TransientModel` with view, buttons, and model binding. |
| `/add-report` | F4 | Generate a QWeb report (PDF/HTML) with print action. |
| `/fix-issue` | F4 | Diagnosis and repair with 6-step root cause analysis. |
| `/generate-tests` | F5 | Generate `TransactionCase` or `HttpCase` with Form helper, HOOT, and Tours. |
| `/perf-check` | F5 | Detect N+1, over-triggered `@api.depends`, and missing indexes. |
| `/security-audit` | F5 | Audit ACLs, record rules, AND/OR logic, `sudo()`, and portal security. |
| `/translate` | F6 | Scan code and update `i18n/es.po` with all translatable strings. |
| `/review-pr` | F6 | Pull Request review with Odoo 19-specific checklist. |
| `/changelog` | F6 | Generate or update `CHANGELOG.md` with semantic versioning. |
| `/deploy` | F6 | Odoo.sh deployment checklist with pre/post migration and change management. |
| `/hotfix` | F7 | Accelerated protocol for production-critical bugs. |

---

## Module Structure

### Naming Conventions

| Concept | Convention |
|---|---|
| Technical name | `dipl_<name>` (always with prefix) |
| Version | `19.0.x.y.z` |
| License | `LGPL-3` |
| Author | `Dipleg` |
| Git branches | `feature/`, `fix/`, `release/` |
| Commits | `feat:`, `fix:`, `docs:`, `test:`, `refactor:` |

### `__manifest__.py`

```python
{
    "name": "Dipleg - Sale Extra",
    "version": "19.0.1.0.0",
    "category": "Sales",
    "summary": "Short module description",
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

### Base Structure Generated by `/scaffold-module`

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

Optional directories as needed: `wizards/`, `report/`, `static/src/` (OWL).

---

## Standard Workflow (Iterative SDLC)

```
F0. Infrastructure: /clone-odoo, /sparse-checkout
F1. Planning: /plan-module (GAP Analysis → prioritized backlog)
F2. Analysis: /explain (existing code mapping)
F3. Design: /scaffold-module or /new-feature (mandatory inheritance decision)
F4. Implementation: models → security → views → tests → i18n
F5. QA: /generate-tests, /perf-check, /security-audit (5-level pyramid)
F6. Deploy: /translate, /review-pr, /changelog, /deploy (staging → production)
F7. Maintenance: /hotfix, post-deploy monitoring, cyclic closure → F1
```

---

## Python Dependencies

Add to [`requirements.txt`](./requirements.txt). Odoo.sh installs them automatically.

Also declare in `__manifest__.py`:

```python
"external_dependencies": {
    "python": ["package_name"],
},
```

---

## Odoo.sh Compatibility

This repository works directly as a module repository on Odoo.sh:

- Custom modules at the **repo root** with `__manifest__.py` and `installable: True`.
- `requirements.txt` at root for Python dependencies.
- `packages.txt` at root for OS dependencies (if applicable).
- Git submodules for external repo dependencies (e.g., OCA).
- The `src/` folder is **NOT mounted** — it is reference only.
- No additional configuration needed.

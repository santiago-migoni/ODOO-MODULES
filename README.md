# ODOO-MODULES

Custom Odoo 19 module repository for Dipleg. Compatible with Odoo.sh.

## Codex-first structure

```text
ODOO-MODULES/
├── dipl_<name>/                 # Installable custom modules at repo root
├── .codex/                      # Official agent ecosystem
│   ├── config.toml              # Runtime baseline (approval/sandbox/profile)
│   ├── skills/                  # Reusable Codex skills (SKILL.md + references)
│   ├── docs/
│   │   ├── workflows/           # SDLC playbooks (human readable)
│   │   ├── rules/               # Governance/quality docs
│   └── rules/                   # Executable Codex rule files (*.rules)
├── .src/                        # Odoo Community source (reference only)
├── AGENTS.md                    # Primary governance entrypoint for agents
├── README.md
└── requirements.txt
```

Authoritative order for agent guidance:
1. `AGENTS.md`
2. `.codex/`

## How to operate with Codex

- Activate capabilities via `$skill`.
- Skills are autonomous and must contain their own execution contract.
- Runtime behavior is governed by `.codex/config.toml` + `.codex/rules/*.rules`.
- Use phase skills and operational skills from `.codex/skills/`.
- Use `.codex/docs/workflows/` for detailed SDLC procedures.
- Use `.codex/docs/rules/` for Odoo conventions and quality gates.

## Core skills

Domain skills:
- `f0-enterprise-sdlc`
- `f1-scrum-master`
- `f2-odoo-analysis`
- `f3-module-patterns`
- `g-odoo-19`
- `f5-odoo-qa`
- `f6-odoo-sh`
- `f7-odoo-maintenance`

Operational skills (replacing command-centric flow):
- `odoo-plan`
- `odoo-analysis`
- `odoo-scaffold`
- `odoo-add-field`
- `odoo-tests`
- `odoo-deploy`
- `odoo-hotfix`

## Odoo module conventions

- Technical module name: `dipl_<name>`
- Versioning: `19.0.x.y.z`
- License: `LGPL-3`
- Default translation target: `i18n/es.po`

Each installable module should follow standard Odoo layout:
- `models/`
- `views/`
- `security/`
- `tests/`
- `i18n/`
- `static/src/` (only if needed)

## Dependencies

Add Python dependencies to `requirements.txt`, and declare them in module manifests:

```python
"external_dependencies": {
    "python": ["package_name"],
},
```

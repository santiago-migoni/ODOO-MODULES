# ODOO-MODULES

Custom Odoo 19 module repository for Dipleg. Compatible with Odoo.sh.

## Codex-first structure

```text
ODOO-MODULES/
├── dipl_<name>/                 # Installable custom modules at repo root
├── .codex/                      # Official agent ecosystem
│   ├── config.toml              # Runtime baseline (approval/sandbox/profile)
│   ├── agents/                  # Project subagents (*.toml)
│   ├── skills/                  # Reusable Codex skills (SKILL.md + references)
│   └── rules/                   # Executable Codex rule files (*.rules)
├── .docs/                       # Local developer records (ignored from VCS)
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
- Delegate project subagents from `.codex/agents/*.toml` when specialization helps.
- Skills are autonomous and must contain their own execution contract.
- Runtime behavior is governed by `.codex/config.toml` + `.codex/rules/*.rules`.
- Use phase skills and operational skills from `.codex/skills/`.

## Core skills

Global technical skill:
- `odoo-19`

Lifecycle skills:
- `odoo-stage-orchestrator`
- `odoo-stage-01-discovery`
- `odoo-stage-02-functional-definition`
- `odoo-stage-03-technical-design`
- `odoo-stage-04-planning`
- `odoo-stage-05-module-scaffolding`
- `odoo-stage-06-implementation`
- `odoo-stage-07-validation-qa`
- `odoo-stage-08-uat`
- `odoo-stage-09-deployment`
- `odoo-stage-10-maintenance`

Governance skill:
- `odoo-dashboard-branch-governance`

Project subagents:
- `code-mapper`
- `frontend-developer`
- `javascript-pro`
- `python-pro`
- `xml-pro`
- `owl-pro`
- `scss-pro`

Branch and environment model:
- `master` is production only.
- All non-master branches are ephemeral and dashboard-managed.
- Delivery flow is `dev-env -> test-env -> master`.
- A branch can move from dev to test without renaming.
- Test environments clone production data while disabling production services like outbound email and similar integrations.

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

`requirements.txt` is the repository-level source of truth for Python dependencies.

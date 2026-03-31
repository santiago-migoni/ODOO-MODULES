---
trigger:
globs: "**/migrations/**", "**/__manifest__.py"
phase: f6-f7
description: Migration scripts (pre/post) and manifest hooks protocol
---

# migration-protocol

Schema changes, data transformations, and cleanup operations that cannot be handled declaratively by XML require imperative migration scripts.

## Migration Scripts

Located in `migrations/` directory, classified by target version:

```
dipl_module/
└── migrations/
    └── 19.0.X.Y.0/
        ├── pre-update.py    # Runs BEFORE ORM applies new schema
        └── post-update.py   # Runs AFTER ORM has applied new schema
```

### Pre-migration (`pre-update.py`)

Executes **before** the server applies updated database definitions from the new code iteration. Use for:

- Remapping historical keys or renaming columns before they're dropped.
- Altering PostgreSQL constraints that would block the schema update.
- Transferring legacy data to temporary columns before new columns manifest.
- Dropping indexes that conflict with new field definitions.

```python
def migrate(cr, version):
    if not version:
        return
    # Direct SQL — ORM not fully available yet
    cr.execute("ALTER TABLE dipl_example RENAME COLUMN old_field TO old_field_backup")
```

### Post-migration (`post-update.py`)

Executes **after** the ORM and table architectures have assimilated the new iteration. Use for:

- Computing values for newly added stored fields.
- Data normalization that depends on the new schema being in place.
- Parameterization of business processes dependent on new columns.
- Cleanup of temporary/backup columns.

```python
def migrate(cr, version):
    if not version:
        return
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    # ORM fully available here
    records = env['dipl.example'].search([('new_field', '=', False)])
    records.write({'new_field': 'default_value'})
```

## Manifest Hooks

Declared in `__manifest__.py`, these execute during first installation (not upgrades):

| Hook | When | Access | Use Case |
|---|---|---|---|
| `pre_init_hook` | Before module install | Direct cursor (`cr`) | Create infrastructure before ORM initializes (sequences, extensions). |
| `post_init_hook` | After module install | Direct cursor (`cr`) | Populate initial data, set defaults that need SQL-level operations. |
| `uninstall_hook` | On module uninstall | Direct cursor (`cr`) | Clean up database artifacts, remove scheduled actions, drop custom sequences. |

Hooks receive the database cursor (`cr`) directly, **bypassing the ORM**. Use with extreme care — no access rights, no computed field triggers, no record rules.

## Rules

- **Always bump version** in `__manifest__.py` when adding migration scripts.
- **Always test migrations** on a staging clone of production data before deploying.
- **Pre scripts**: minimal, surgical — only what's needed before schema changes.
- **Post scripts**: can use full ORM via `api.Environment(cr, SUPERUSER_ID, {})`.
- **Never skip migration scripts** when changing stored field types, renaming fields, or removing models.
- **Document migrations** in CHANGELOG.md with the version and what the script does.

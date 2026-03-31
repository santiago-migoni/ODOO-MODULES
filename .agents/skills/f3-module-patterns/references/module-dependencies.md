# Module Dependencies Guide

Managing relations between custom and standard Odoo 19 modules.

## 1. Local Dependencies (`depends`)

In `__manifest__.py`, declare all required Odoo or custom modules:
- **Core**: `base`, `web`, `mail`.
- **Apps**: `sale`, `purchase`, `stock`, `account`.
- **Custom**: `dipl_base_module` (always use the technical name).

Declare the **minimum necessary** — each dependency increases install time and potential conflicts.

## 2. Python Dependencies (`requirements.txt`)

For external libraries (e.g., `requests`, `pandas`):
1. Add to `requirements.txt` in the repo root.
2. Declare in `__manifest__.py` so Odoo validates them at install:

```python
"external_dependencies": {
    "python": ["pandas", "requests"],
},
```

## 3. OS Dependencies (`packages.txt`)

For system-level libraries (e.g., `libxslt1-dev`, `wkhtmltopdf`):
- List them in `packages.txt` (Odoo.sh reads this automatically during build).
- Overlap with `requirements.txt` at the Python level is expected — both may be needed.

## 4. Circular Dependencies — Detection & Resolution

Circular dependencies (A depends on B, B depends on A) cause install failures.

**Detection**: Odoo raises `odoo.exceptions.ValidationError: Module ... is already installed` or a topological sort error in the log.

**Resolution strategies** (in order of preference):
1. **Extract shared logic** into a new `dipl_base_*` module that both A and B depend on.
2. **Use `_inherit` without `depends`**: If A only needs a field from B's model, inherit the model in A's code and add B to `depends`. Avoid making B depend on A.
3. **Late binding**: Use `self.env['b.model']` at runtime instead of a static import — breaks the manifest-level cycle.

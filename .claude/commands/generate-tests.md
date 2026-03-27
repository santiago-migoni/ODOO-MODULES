---
description: Genera tests para un módulo de Odoo 19.
---
Generate tests for Odoo 19 code following the native testing framework.


The argument `$ARGUMENTS` contains the path to the file or module to generate tests for.

## Steps
1. Read the target file/module.
2. Identify the code type:
   - **Model** -> `TransactionCase`
   - **HTTP Controller** -> `HttpCase`
   - **Wizard** -> `TransactionCase`
   - **JS/OWL** -> `HttpCase` with a tour
3. Consult the testing guide: `.claude/skills/odoo-19/references/odoo-19-testing-guide.md`
4. Analyze the code to identify:
   - Public methods/actions
   - Computed fields and constraints
   - State flows (draft -> confirmed -> done)
   - Permissions and security (sudo vs user)
   - Edge cases (empty records, boundary values)
5. Generate tests in `tests/test_{model}.py`
6. Run the tests if the environment allows it

## Odoo test structure

```python
# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError


@tagged("post_install", "-at_install")
class TestDiplExample(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        # Create shared test data
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.record = cls.env["dipl.example"].create({
            "name": "Test Record",
            "partner_id": cls.partner.id,
        })

    def test_compute_total(self):
        """Computed total field is correct."""
        self.record.line_ids = [(0, 0, {"amount": 100}), (0, 0, {"amount": 200})]
        self.assertEqual(self.record.total, 300)

    def test_constraint_name_min_length(self):
        """Min length constraint is enforced."""
        with self.assertRaises(ValidationError):
            self.record.write({"name": "AB"})

    def test_action_confirm(self):
        """State flow: draft -> confirmed."""
        self.assertEqual(self.record.state, "draft")
        self.record.action_confirm()
        self.assertEqual(self.record.state, "confirmed")

    def test_action_confirm_idempotent(self):
        """Confirming an already confirmed record does not fail."""
        self.record.action_confirm()
        self.record.action_confirm()
        self.assertEqual(self.record.state, "confirmed")

    def test_access_rights_user(self):
        """Basic user can read but cannot delete/unlink (if applicable)."""
        user = self.env["res.users"].create({
            "name": "Test User",
            "login": "test_user",
            "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
        })
        record_as_user = self.record.with_user(user)
        record_as_user.read(["name"])
```

## Conventions
- **File**: `tests/test_{model}.py` (e.g. `tests/test_dipl_example.py`)
- **Class**: `TestDipl{Model}(TransactionCase)`
- **Methods**: `test_{what_is_being_tested}` -- descriptive
- **Tags**: `@tagged("post_install", "-at_install")` for tests that need installed data
- **setUpClass**: create shared data; use `tracking_disable=True` to avoid mail chatter
- **Don't forget**: add `from . import test_{model}` in `tests/__init__.py`

## What to test (priority)
1. **Computed fields** -- correct computation with different inputs
2. **Constraints** -- ensure `ValidationError` is raised when it should
3. **State flows** -- valid and invalid transitions
4. **CRUD overrides** -- custom `create`, `write`, `unlink` (if any)
5. **Permissions** -- access with different users/groups
6. **Wizards** -- `action_apply` (or equivalent) processes records correctly
7. **Controllers** -- only when logic is complex (use `HttpCase`)

## What NOT to test
- Trivial getters/setters
- Odoo ORM internal logic (already tested upstream)
- XML views (use tours for complex UI flows)

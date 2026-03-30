# Test Pattern — Dipleg Odoo 19

Complete template for `TransactionCase` tests. Copy and adapt for each module.

## Test File (`tests/test_{name}.py`)

```python
# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDiplExample(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """Create shared data for all tests in this class."""
        super().setUpClass()
        # Disable mail tracking to avoid sending emails during tests
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))

        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.record = cls.env["dipl.example"].create(
            {
                "name": "Test Record",
                "partner_id": cls.partner.id,
            }
        )

    # === COMPUTED FIELDS ===
    def test_compute_total_with_lines(self):
        """Total is correctly computed with lines."""
        self.record.line_ids = [
            (0, 0, {"amount": 100.0}),
            (0, 0, {"amount": 200.0}),
        ]
        self.assertEqual(self.record.total, 300.0)

    def test_compute_total_without_lines(self):
        """Total is 0 when no lines exist."""
        self.assertEqual(self.record.total, 0.0)

    # === CONSTRAINTS ===
    def test_constraint_name_too_short(self):
        """ValidationError raised when name < 3 chars."""
        with self.assertRaises(ValidationError):
            self.record.write({"name": "AB"})

    def test_constraint_name_valid(self):
        """Name with 3+ chars does not raise an error."""
        self.record.write({"name": "ABC"})
        self.assertEqual(self.record.name, "ABC")

    # === STATE TRANSITIONS ===
    def test_action_confirm_from_draft(self):
        """Confirming a draft record moves it to confirmed."""
        self.assertEqual(self.record.state, "draft")
        self.record.action_confirm()
        self.assertEqual(self.record.state, "confirmed")

    def test_action_confirm_idempotent(self):
        """Confirming an already confirmed record does not fail."""
        self.record.action_confirm()
        self.record.action_confirm()
        self.assertEqual(self.record.state, "confirmed")

    def test_action_cancel(self):
        """Cancelling a record changes state to cancelled."""
        self.record.action_cancel()
        self.assertEqual(self.record.state, "cancelled")

    # === CRUD ===
    def test_create_batch(self):
        """Batch create works correctly."""
        records = self.env["dipl.example"].create(
            [{"name": "Record 1"}, {"name": "Record 2"}]
        )
        self.assertEqual(len(records), 2)

    # === ACCESS RIGHTS ===
    def test_user_can_read(self):
        """Basic user can read records without AccessError."""
        user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_user_dipl",
                "groups_id": [(6, 0, [self.env.ref("base.group_user").id])],
            }
        )
        self.record.with_user(user).read(["name"])
```

## `tests/__init__.py`

```python
from . import test_{name}
```

## Key conventions

- **`@tagged("post_install", "-at_install")`**: runs after all modules are installed, ensuring XML IDs are available.
- **`setUpClass`**: creates shared data once per test class — faster than `setUp` (per-test).
- **`tracking_disable=True`**: prevents mail chatter from triggering during tests — avoids side effects.
- **Test naming**: `test_{what_is_being_tested}` — descriptive, one assertion per test.
- **Coverage priority**: (1) Computed fields, (2) Constraints, (3) State transitions, (4) CRUD overrides, (5) Access rights.
- **Do NOT test**: trivial getters/setters, Odoo ORM internals, or XML view structure.

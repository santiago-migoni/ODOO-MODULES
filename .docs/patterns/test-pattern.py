# -*- coding: utf-8 -*-
"""Plantilla de tests Odoo estándar Dipleg.

Uso: copiar y adaptar para tests en módulos dipl_*.
Usa TransactionCase (rollback automático por test).
"""
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestDiplExample(TransactionCase):

    @classmethod
    def setUpClass(cls):
        """Crear datos compartidos para todos los tests."""
        super().setUpClass()
        # Desactivar tracking para evitar envío de mails en tests
        cls.env = cls.env(
            context=dict(cls.env.context, tracking_disable=True)
        )

        # Datos de test
        cls.partner = cls.env["res.partner"].create(
            {"name": "Test Partner"}
        )
        cls.record = cls.env["dipl.example"].create(
            {
                "name": "Test Record",
                "partner_id": cls.partner.id,
            }
        )

    # === COMPUTED FIELDS ===#
    def test_compute_total_with_lines(self):
        """Total se calcula correctamente con líneas."""
        self.record.line_ids = [
            (0, 0, {"amount": 100.0}),
            (0, 0, {"amount": 200.0}),
        ]
        self.assertEqual(self.record.total, 300.0)

    def test_compute_total_without_lines(self):
        """Total es 0 cuando no hay líneas."""
        self.assertEqual(self.record.total, 0.0)

    # === CONSTRAINTS ===#
    def test_constraint_name_too_short(self):
        """ValidationError si nombre tiene menos de 3 caracteres."""
        with self.assertRaises(ValidationError):
            self.record.write({"name": "AB"})

    def test_constraint_name_valid(self):
        """Nombre de 3+ caracteres no lanza error."""
        self.record.write({"name": "ABC"})
        self.assertEqual(self.record.name, "ABC")

    # === STATE TRANSITIONS ===#
    def test_action_confirm_from_draft(self):
        """Confirmar un registro en draft cambia a confirmed."""
        self.assertEqual(self.record.state, "draft")
        self.record.action_confirm()
        self.assertEqual(self.record.state, "confirmed")

    def test_action_confirm_idempotent(self):
        """Confirmar un registro ya confirmado no falla."""
        self.record.action_confirm()
        self.record.action_confirm()
        self.assertEqual(self.record.state, "confirmed")

    def test_action_cancel(self):
        """Cancelar un registro cambia a cancelled."""
        self.record.action_cancel()
        self.assertEqual(self.record.state, "cancelled")

    # === CRUD OVERRIDES ===#
    def test_create_batch(self):
        """Batch create funciona correctamente."""
        records = self.env["dipl.example"].create(
            [
                {"name": "Record 1"},
                {"name": "Record 2"},
            ]
        )
        self.assertEqual(len(records), 2)

    # === ACCESS RIGHTS ===#
    def test_user_can_read(self):
        """Usuario básico puede leer registros."""
        user = self.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_user_dipl",
                "groups_id": [
                    (6, 0, [self.env.ref("base.group_user").id])
                ],
            }
        )
        # No debe lanzar AccessError
        self.record.with_user(user).read(["name"])

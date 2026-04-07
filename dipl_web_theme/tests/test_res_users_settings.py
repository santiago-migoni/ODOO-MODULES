# -*- coding: utf-8 -*-

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestResUsersSettings(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = cls.env["res.users"].create(
            {
                "name": "Theme Test User",
                "login": "theme_test_user",
                "password": "theme_test_user",
            }
        )
        cls.settings = cls.env["res.users.settings"]._find_or_create_for_user(cls.user)

    def test_custom_fields_exist(self):
        self.assertIn("color_scheme", self.env["res.users.settings"]._fields)
        self.assertIn("homemenu_config", self.env["res.users.settings"]._fields)
        self.assertEqual(self.settings.color_scheme, "system")

    def test_color_scheme_persists_allowed_values(self):
        for scheme in ("system", "light", "dark"):
            self.settings.write({"color_scheme": scheme})
            self.assertEqual(self.settings.color_scheme, scheme)

    def test_homemenu_config_persists_native_json(self):
        config = [
            {"xmlid": "sale.sale_menu_root", "sequence": 1},
            {"xmlid": "website.menu_website_configuration", "sequence": 2},
        ]
        self.settings.write({"homemenu_config": config})
        self.assertEqual(self.settings.homemenu_config, config)

    def test_homemenu_config_accepts_legacy_string_and_remains_writable(self):
        legacy_config = '[{"xmlid":"sale.sale_menu_root","sequence":1}]'
        native_config = [{"xmlid": "base.menu_administration", "sequence": 1}]

        self.settings.write({"homemenu_config": legacy_config})
        self.assertEqual(self.settings.homemenu_config, legacy_config)

        self.settings.write({"homemenu_config": native_config})
        self.assertEqual(self.settings.homemenu_config, native_config)

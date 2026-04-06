# -*- coding: utf-8 -*-

from types import SimpleNamespace
from unittest.mock import patch

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestWebThemeHttp(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.internal_user = cls.env["res.users"].create(
            {
                "name": "Theme Internal User",
                "login": "theme_internal_user",
                "password": "theme_internal_user",
            }
        )
        cls.internal_settings = cls.env["res.users.settings"]._find_or_create_for_user(
            cls.internal_user
        )
        cls.public_user = cls.env.ref("base.public_user")

    def _fake_request(self, user, cookies=None):
        cookie_calls = []

        def set_cookie(*args, **kwargs):
            cookie_calls.append((args, kwargs))

        fake_request = SimpleNamespace(
            httprequest=SimpleNamespace(cookies=cookies or {}),
            env=SimpleNamespace(user=user),
            future_response=SimpleNamespace(set_cookie=set_cookie),
        )
        return fake_request, cookie_calls

    def test_color_scheme_prefers_user_setting_for_internal_user(self):
        self.internal_settings.write({"color_scheme": "dark"})
        fake_request, _cookie_calls = self._fake_request(
            self.internal_user, cookies={"color_scheme": "light"}
        )

        with patch("odoo.addons.dipl_web_theme.models.ir_http.request", fake_request):
            self.assertEqual(self.env["ir.http"].color_scheme(), "dark")

    def test_color_scheme_falls_back_to_cookie_for_system_mode(self):
        self.internal_settings.write({"color_scheme": "system"})
        fake_request, _cookie_calls = self._fake_request(
            self.internal_user, cookies={"color_scheme": "dark"}
        )

        with patch("odoo.addons.dipl_web_theme.models.ir_http.request", fake_request):
            self.assertEqual(self.env["ir.http"].color_scheme(), "dark")

    def test_color_scheme_ignores_cookie_for_public_user(self):
        fake_request, _cookie_calls = self._fake_request(
            self.public_user, cookies={"color_scheme": "dark"}
        )

        with patch("odoo.addons.dipl_web_theme.models.ir_http.request", fake_request):
            self.assertEqual(self.env["ir.http"].color_scheme(), "light")

    def test_post_logout_clears_color_scheme_cookie(self):
        fake_request, cookie_calls = self._fake_request(self.public_user)

        with patch("odoo.addons.dipl_web_theme.models.ir_http.request", fake_request):
            self.env["ir.http"]._post_logout()

        self.assertIn((("color_scheme",), {"max_age": 0}), cookie_calls)

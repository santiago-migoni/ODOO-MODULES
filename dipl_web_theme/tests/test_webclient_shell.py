# -*- coding: utf-8 -*-

from odoo.tests import HttpCase, tagged
from odoo.tests.common import new_test_user


@tagged("post_install", "-at_install")
class TestWebclientShell(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user_password = "theme_http_case"
        cls.user = new_test_user(
            cls.env,
            login="theme_http_case",
            password=cls.user_password,
            groups="base.group_user",
        )
        settings = cls.env["res.users.settings"]._find_or_create_for_user(cls.user)
        settings.write({"color_scheme": "dark"})

    def test_odoo_route_sets_color_scheme_cookie(self):
        self.authenticate(self.user.login, self.user_password)
        response = self.url_open("/odoo")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.cookies.get("color_scheme"), "dark")

    def test_shell_smoke_loads_home_menu(self):
        self.browser_js(
            "/odoo",
            """
                const waitFor = async (predicate, timeout = 15000) => {
                    const start = Date.now();
                    while (!predicate()) {
                        if (Date.now() - start > timeout) {
                            throw new Error("Timed out waiting for shell state");
                        }
                        await new Promise((resolve) => setTimeout(resolve, 100));
                    }
                };

                (async () => {
                    await waitFor(() => document.querySelector("header nav.o_main_navbar"));
                    await waitFor(() => document.querySelector(".o_home_menu"));
                    if (!document.querySelector(".o_menu_toggle")) {
                        throw new Error("Missing theme navbar toggle");
                    }
                    console.log("dipl_web_theme shell smoke succeeded");
                })();
            """,
            "odoo.isReady === true",
            login=self.user.login,
            timeout=180,
            success_signal="dipl_web_theme shell smoke succeeded",
        )

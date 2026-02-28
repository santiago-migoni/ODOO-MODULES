from odoo.tests import HttpCase, tagged

@tagged('post_install', '-at_install')
class TestHomeControllers(HttpCase):

    def test_01_web_client_color_scheme(self):
        # We need to test the /web endpoint to ensure it renders correctly
        # and doesn't crash after our template overrides.
        res = self.url_open('/web')
        self.assertEqual(res.status_code, 200, "The /web endpoint must return a 200 OK.")
        # Ensure that our injected class is present in the rendered HTML
        self.assertIn(b'o_web_client', res.content, "Webclient body classes missing.")

    def test_02_web_login_color_scheme(self):
        # Ensure the login layout is properly padded and hasn't broken
        res = self.url_open('/web/login')
        self.assertEqual(res.status_code, 200, "The /web/login endpoint must return a 200 OK.")
        # Make sure our custom background class is being injected by x-path
        self.assertIn(b'o_home_menu_background', res.content, "Login background class missing.")

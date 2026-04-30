# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.addons.web.controllers import home as web_home
from odoo.http import request, route


class Home(web_home.Home):

    @route('/odoo/home', type='http', auth='user')
    def dipl_home(self, **kw):
        return request.redirect('/odoo/action-dipl_web_theme.home_menu')

    @route()
    def web_client(self, s_action=None, **kw):
        if (
            request.httprequest.path == '/odoo'
            and not s_action
            and request.env.user.has_group('base.group_user')
        ):
            return request.redirect('/odoo/home')
        response = super().web_client(s_action, **kw)
        if response.status_code == 200:
            response.set_cookie('color_scheme', request.env['ir.http'].color_scheme())
        return response

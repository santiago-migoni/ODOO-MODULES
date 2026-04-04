import { NavBar } from "@web/webclient/navbar/navbar";
import { useService, useBus } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";
import { useEffect, useRef } from "@odoo/owl";

patch(NavBar.prototype, {
    setup() {
        super.setup(...arguments);
        this.diplHomeMenu = useService("dipl_home_menu");
        this.menuAppsRef = useRef("menuApps");
        this.navRef = useRef("nav");
        useBus(this.env.bus, "DIPL_HOME_MENU:TOGGLED", () => this._updateMenuAppsIcon());
        useEffect(() => this._updateMenuAppsIcon());
    },
    get hasBackgroundAction() {
        return this.diplHomeMenu.hasBackgroundAction;
    },
    get isInApp() {
        return !this.diplHomeMenu.hasHomeMenu;
    },

    _openAppMenuSidebar() {
        if (this.diplHomeMenu.hasHomeMenu) {
            this.diplHomeMenu.toggle(false);
        } else {
            this.state.isAppMenuSidebarOpened = true;
        }
    },
    _updateMenuAppsIcon() {
        const menuAppsEl = this.menuAppsRef.el;
        const navEl = this.navRef.el;
        if (!menuAppsEl || !navEl) {
            return;
        }
        menuAppsEl.classList.toggle("o_hidden", !this.isInApp && !this.hasBackgroundAction);
        menuAppsEl.classList.toggle(
            "o_menu_toggle_back",
            !this.isInApp && this.hasBackgroundAction
        );
        if (!this.isScopedApp) {
            const title =
                !this.isInApp && this.hasBackgroundAction ? _t("Previous view") : _t("Home menu");
            menuAppsEl.title = title;
            menuAppsEl.ariaLabel = title;
        }

        const menuBrand = navEl.querySelector(".o_menu_brand");
        if (menuBrand) {
            menuBrand.classList.toggle("o_hidden", !this.isInApp);
        }

        const menuBrandIcon = navEl.querySelector(".o_menu_brand_icon");
        if (menuBrandIcon) {
            menuBrandIcon.classList.toggle("o_hidden", !this.isInApp);
        }

        const appSubMenus = this.appSubMenus.el;
        if (appSubMenus) {
            appSubMenus.classList.toggle("o_hidden", !this.isInApp);
        }

        const breadcrumb = navEl.querySelector(".o_navbar_breadcrumbs");
        if (breadcrumb) {
            breadcrumb.classList.toggle("o_hidden", !this.isInApp);
        }
    },

    /**
     * @override
     */
    onAllAppsBtnClick() {
        super.onAllAppsBtnClick();
        this.diplHomeMenu.toggle(true);
        this._closeAppMenuSidebar();
    },
});

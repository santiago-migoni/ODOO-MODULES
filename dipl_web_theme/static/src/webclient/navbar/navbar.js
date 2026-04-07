import { NavBar } from "@web/webclient/navbar/navbar";
import { useService } from "@web/core/utils/hooks";
import { _t } from "@web/core/l10n/translation";
import { patch } from "@web/core/utils/patch";

patch(NavBar.prototype, {
    setup() {
        super.setup(...arguments);
        this.diplHomeMenu = useService("dipl_home_menu");
    },
    get hasBackgroundAction() {
        return Boolean(this.diplHomeMenu?.hasBackgroundAction);
    },
    get hasHomeMenu() {
        return Boolean(this.diplHomeMenu?.hasHomeMenu);
    },
    get isInApp() {
        return !this.hasHomeMenu;
    },
    get showMenuToggle() {
        return this.isInApp || this.hasBackgroundAction || this.isScopedApp;
    },
    get menuToggleClasses() {
        return {
            hasImage: Boolean(this.currentApp?.webIconData),
            o_hidden: !this.isScopedApp && !this.showMenuToggle,
            o_menu_toggle_back: !this.isScopedApp && !this.isInApp && this.hasBackgroundAction,
        };
    },
    get menuToggleTitle() {
        if (this.isScopedApp) {
            return undefined;
        }
        return !this.isInApp && this.hasBackgroundAction ? _t("Previous view") : _t("Home menu");
    },
    get showAppBrand() {
        return this.isInApp;
    },
    get showBreadcrumbs() {
        return this.isInApp;
    },
    get showSectionsMenu() {
        return this.isInApp;
    },
    _openAppMenuSidebar() {
        if (this.hasHomeMenu) {
            this.diplHomeMenu.toggle(false);
            return;
        }
        this.state.isAppMenuSidebarOpened = true;
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

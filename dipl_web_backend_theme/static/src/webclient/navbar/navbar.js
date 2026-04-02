import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { NavBar } from "@web/webclient/navbar/navbar";

patch(NavBar.prototype, {
    setup() {
        super.setup(...arguments);
        this.homeMenu = useService("home_menu");
    },

    get hasHomeMenu() {
        return this.homeMenu.hasHomeMenu;
    },

    toggleHomeMenu() {
        this.homeMenu.toggle(true);
        this._closeAppMenuSidebar();
    },

    _openAppMenuSidebar() {
        if (this.homeMenu.hasHomeMenu) {
            this.homeMenu.toggle(false);
            return;
        }
        return super._openAppMenuSidebar(...arguments);
    },

    onAllAppsBtnClick() {
        if (this.env.isSmall) {
            this.toggleHomeMenu();
            return;
        }
        return super.onAllAppsBtnClick(...arguments);
    },
});

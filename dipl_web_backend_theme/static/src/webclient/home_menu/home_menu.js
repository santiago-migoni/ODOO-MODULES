import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class DiplegHomeMenu extends Component {
    static template = "dipl_web_backend_theme.HomeMenu";
    static props = {
        apps: {
            type: Array,
            element: {
                type: Object,
            },
        },
    };

    setup() {
        this.menuService = useService("menu");
        this.homeMenu = useService("home_menu");
    }

    get hasResults() {
        return this.props.apps.length > 0;
    }

    async onSelectApp(app) {
        await this.menuService.selectMenu(this.menuService.getMenu(app.id));
    }

    closeHomeMenu() {
        this.homeMenu.toggle(false);
    }
}

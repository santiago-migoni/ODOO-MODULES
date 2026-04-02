import { Component, useRef, useState } from "@odoo/owl";
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
        this.searchRef = useRef("search");
        this.state = useState({
            query: "",
        });
    }

    get displayedApps() {
        const query = this.state.query.trim().toLowerCase();
        if (!query) {
            return this.props.apps;
        }
        return this.props.apps.filter((app) => {
            const haystack = [app.label, app.parents, app.xmlid].filter(Boolean).join(" ").toLowerCase();
            return haystack.includes(query);
        });
    }

    get hasResults() {
        return this.displayedApps.length > 0;
    }

    onInputSearch(ev) {
        this.state.query = ev.target.value;
    }

    async onSelectApp(app) {
        await this.menuService.selectMenu(this.menuService.getMenu(app.id));
    }

    clearSearch() {
        this.state.query = "";
        if (this.searchRef.el) {
            this.searchRef.el.focus();
        }
    }

    closeHomeMenu() {
        this.homeMenu.toggle(false);
    }
}

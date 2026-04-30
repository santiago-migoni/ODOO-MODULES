import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { user } from "@web/core/user";
import { Mutex } from "@web/core/utils/concurrency";
import { useBus, useService } from "@web/core/utils/hooks";
import { computeAppsAndMenuItems, reorderApps } from "@web/webclient/menus/menu_helpers";
import { HomeMenu } from "./home_menu";

import { Component, onMounted, onWillUnmount, reactive } from "@odoo/owl";

export const readHomeMenuConfig = () => {
    const storedConfig = user.settings?.homemenu_config;
    if (Array.isArray(storedConfig)) {
        return storedConfig;
    }
    if (typeof storedConfig === "string") {
        try {
            return JSON.parse(storedConfig);
        } catch {
            return null;
        }
    }
    return null;
};

export const homeMenuService = {
    dependencies: ["action"],
    start(env) {
        const state = reactive({
            hasHomeMenu: false, // true iff the HomeMenu is currently displayed
            hasBackgroundAction: false, // true iff there is an action behind the HomeMenu
            toggle,
        });
        const mutex = new Mutex(); // used to protect against concurrent toggling requests

        env.bus.addEventListener("DIPL_HOME_MENU:TOGGLED", () => {
            document.body.classList.toggle("o_home_menu_background", state.hasHomeMenu);
        });

        const forceHomeMenuCleanUrl = () => {
            const { pathname, search } = browser.location;
            if (!pathname.includes("/odoo/action-")) {
                return;
            }
            browser.history.replaceState(browser.history.state, "", `/odoo${search || ""}`);
        };

        async function toggle(show) {
            return mutex.exec(async () => {
                show = show === undefined ? !state.hasHomeMenu : Boolean(show);
                if (show !== state.hasHomeMenu) {
                    if (show) {
                        state.hasBackgroundAction = Boolean(
                            env.services.action?.currentController
                        );
                        state.hasHomeMenu = true;
                        forceHomeMenuCleanUrl();
                        env.bus.trigger("DIPL_HOME_MENU:TOGGLED");
                        return true;
                    } else {
                        state.hasHomeMenu = false;
                        state.hasBackgroundAction = false;
                        env.bus.trigger("DIPL_HOME_MENU:TOGGLED");
                        forceHomeMenuCleanUrl();
                        return true;
                    }
                }
                return true;
            });
        }

        return state;
    },
};

class HomeMenuRoot extends Component {
    static template = "dipl_web_theme.HomeMenuRoot";
    static components = { HomeMenu };

    setup() {
        this.menus = useService("menu");
        this.homeMenuService = useService("dipl_home_menu");
        onMounted(() => this.env.bus.trigger("DIPL_HOME_MENU:TOGGLED"));
        onWillUnmount(() => this.env.bus.trigger("DIPL_HOME_MENU:TOGGLED"));
        useBus(this.env.bus, "MENUS:APP-CHANGED", () => this.render());
    }

    get homeMenuProps() {
        const homemenuConfig = readHomeMenuConfig();
        const apps = reactive(computeAppsAndMenuItems(this.menus.getMenuAsTree("root")).apps);
        if (homemenuConfig) {
            reorderApps(apps, homemenuConfig);
        }
        return {
            apps,
            reorderApps: (order) => reorderApps(apps, order),
        };
    }
}

registry.category("services").add("dipl_home_menu", homeMenuService);
registry.category("main_components").add("dipl_home_menu.root", {
    Component: HomeMenuRoot,
}, { force: true });

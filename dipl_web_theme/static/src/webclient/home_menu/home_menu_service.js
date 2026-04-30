import { browser } from "@web/core/browser/browser";
import { router, routerBus } from "@web/core/browser/router";
import { registry } from "@web/core/registry";
import { user } from "@web/core/user";
import { Mutex } from "@web/core/utils/concurrency";
import { useBus, useService } from "@web/core/utils/hooks";
import { computeAppsAndMenuItems, reorderApps } from "@web/webclient/menus/menu_helpers";
import { HomeMenu } from "./home_menu";

import { Component, onMounted, onWillUnmount, reactive } from "@odoo/owl";

const HOME_PATH = "/odoo/home";
const HOME_FLAG = "dipl_home";
let homeRoutePatched = false;

function stripHomeFlag(state = {}) {
    const nextState = { ...state };
    delete nextState[HOME_FLAG];
    return nextState;
}

function isHomePath(pathname) {
    return pathname === HOME_PATH;
}

function currentUrl() {
    const { pathname, search, hash } = browser.location;
    return `${pathname}${search || ""}${hash || ""}`;
}

function patchHomeRouteSerialization() {
    if (homeRoutePatched) {
        return;
    }
    homeRoutePatched = true;
    const nativeStateToUrl = router.stateToUrl.bind(router);
    const nativeUrlToState = router.urlToState.bind(router);

    router.stateToUrl = (state) => {
        if (!state?.[HOME_FLAG]) {
            return nativeStateToUrl(state);
        }
        const baseUrl = nativeStateToUrl(stripHomeFlag(state));
        if (baseUrl === "/odoo") {
            return HOME_PATH;
        }
        if (baseUrl.startsWith("/odoo?")) {
            return `${HOME_PATH}${baseUrl.slice("/odoo".length)}`;
        }
        return HOME_PATH;
    };

    router.urlToState = (urlObject) => {
        const parsedState = nativeUrlToState(urlObject);
        if (!isHomePath(urlObject.pathname)) {
            return stripHomeFlag(parsedState);
        }
        const nextState = stripHomeFlag(parsedState);
        delete nextState.action;
        delete nextState.actionStack;
        delete nextState.model;
        delete nextState.resId;
        delete nextState.active_id;
        nextState[HOME_FLAG] = true;
        return nextState;
    };
}

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
        patchHomeRouteSerialization();

        const state = reactive({
            hasHomeMenu: false,
            hasBackgroundAction: false,
            isRouteHome: false,
            lastAppUrl: null,
            toggle,
        });
        const mutex = new Mutex(); // used to protect against concurrent toggling requests

        const syncFromRoute = () => {
            state.isRouteHome = Boolean(router.current?.[HOME_FLAG]) || isHomePath(browser.location.pathname);
            state.hasHomeMenu = state.isRouteHome;
            state.hasBackgroundAction = Boolean(state.isRouteHome && state.lastAppUrl);
            if (!state.isRouteHome && !isHomePath(browser.location.pathname)) {
                state.lastAppUrl = currentUrl();
            }
        };

        env.bus.addEventListener("DIPL_HOME_MENU:TOGGLED", () => {
            document.body.classList.toggle("o_home_menu_background", state.hasHomeMenu);
        });

        routerBus.addEventListener("ROUTE_CHANGE", syncFromRoute);

        async function toggle(show) {
            return mutex.exec(async () => {
                show = show === undefined ? !state.hasHomeMenu : Boolean(show);
                syncFromRoute();
                if (show === state.hasHomeMenu) {
                    return true;
                }

                if (show) {
                    if (!state.isRouteHome && !isHomePath(browser.location.pathname)) {
                        state.lastAppUrl = currentUrl();
                    }
                    router.pushState({ [HOME_FLAG]: true }, { replace: false, sync: true });
                    syncFromRoute();
                    env.bus.trigger("DIPL_HOME_MENU:TOGGLED");
                    return true;
                }

                const targetState = state.lastAppUrl
                    ? stripHomeFlag(router.urlToState(new URL(state.lastAppUrl, browser.location.origin)))
                    : {};
                router.pushState(targetState, { replace: false, sync: true });
                syncFromRoute();
                env.bus.trigger("DIPL_HOME_MENU:TOGGLED");
                return true;
            });
        }

        syncFromRoute();

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

import { describe, expect, test } from "@odoo/hoot";
import { EventBus } from "@odoo/owl";

import { patchWithCleanup } from "@web/../tests/web_test_helpers";
import { router, routerBus } from "@web/core/browser/router";
import { _makeUser, user } from "@web/core/user";
import { browser } from "@web/core/browser/browser";

import {
    homeMenuService,
    readHomeMenuConfig,
} from "../../src/webclient/home_menu/home_menu_service";

describe.current.tags("headless");

function makeEnv(actionService) {
    return {
        bus: new EventBus(),
        config: {},
        services: {
            action: actionService,
        },
    };
}

test("service is registered in the services registry", () => {
    expect(typeof homeMenuService.start).toBe("function");
});

test("readHomeMenuConfig reads native JSON config", () => {
    const config = [{ xmlid: "sale.sale_menu_root", sequence: 1 }];
    patchWithCleanup(user, _makeUser({ user_settings: { homemenu_config: config } }));

    expect(readHomeMenuConfig()).toEqual(config);
});

test("readHomeMenuConfig reads legacy stringified config", () => {
    const config = '[{"xmlid":"sale.sale_menu_root","sequence":1}]';
    patchWithCleanup(user, _makeUser({ user_settings: { homemenu_config: config } }));

    expect(readHomeMenuConfig()).toEqual([{ xmlid: "sale.sale_menu_root", sequence: 1 }]);
});

test("toggle opens and closes the custom home menu state", async () => {
    const state = homeMenuService.start(makeEnv({ currentController: {} }));
    expect(state.hasHomeMenu).toBe(false);
    expect(await state.toggle(true)).toBe(true);
    expect(state.hasHomeMenu).toBe(true);
    expect(await state.toggle(false)).toBe(true);
    expect(state.hasHomeMenu).toBe(false);
});

test("toggle navigates between /odoo/home and the previous app route", async () => {
    const location = {
        pathname: "/odoo/sales",
        search: "",
        hash: "",
    };
    let routeState = {};

    patchWithCleanup(browser, {
        location,
    });
    patchWithCleanup(router, {
        get current() {
            return routeState;
        },
        stateToUrl(state) {
            if (state.action === "sales") {
                return "/odoo/sales";
            }
            return "/odoo";
        },
        urlToState(urlObject) {
            if (urlObject.pathname === "/odoo/sales") {
                return { action: "sales" };
            }
            return {};
        },
        pushState(nextState) {
            routeState = { ...nextState };
            if (nextState.dipl_home) {
                location.pathname = "/odoo/home";
            } else if (nextState.action === "sales") {
                location.pathname = "/odoo/sales";
            } else {
                location.pathname = "/odoo/";
            }
            routerBus.trigger("ROUTE_CHANGE");
        },
    });

    const state = homeMenuService.start(makeEnv({ currentController: {} }));
    await state.toggle(true);
    expect(location.pathname).toBe("/odoo/home");
    expect(state.lastAppUrl).toBe("/odoo/sales");
    expect(state.hasHomeMenu).toBe(true);
    await state.toggle(false);
    expect(location.pathname).toBe("/odoo/sales");
    expect(state.hasHomeMenu).toBe(false);
});

test("home flag never keeps home menu visible after navigating to an app route", async () => {
    const location = {
        pathname: "/odoo/home",
        search: "",
        hash: "",
    };
    let routeState = { dipl_home: true };

    patchWithCleanup(browser, {
        location,
    });
    patchWithCleanup(router, {
        get current() {
            return routeState;
        },
        stateToUrl(state) {
            if (state.action === "base_setup.action_general_configuration") {
                return "/odoo/settings";
            }
            return state.dipl_home ? "/odoo/home" : "/odoo";
        },
        urlToState(urlObject) {
            if (urlObject.pathname === "/odoo/settings") {
                return { action: "base_setup.action_general_configuration" };
            }
            return {};
        },
        pushState(nextState) {
            routeState = { ...nextState };
            location.pathname =
                nextState.action === "base_setup.action_general_configuration"
                    ? "/odoo/settings"
                    : nextState.dipl_home
                      ? "/odoo/home"
                      : "/odoo/";
            routerBus.trigger("ROUTE_CHANGE");
        },
    });

    const state = homeMenuService.start(makeEnv({ currentController: {} }));
    expect(state.hasHomeMenu).toBe(true);

    routeState = { dipl_home: true, action: "base_setup.action_general_configuration" };
    location.pathname = "/odoo/settings";
    routerBus.trigger("ROUTE_CHANGE");

    expect(state.hasHomeMenu).toBe(false);
    expect(state.isRouteHome).toBe(false);
});

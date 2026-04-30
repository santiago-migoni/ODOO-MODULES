import { describe, expect, test } from "@odoo/hoot";
import { EventBus } from "@odoo/owl";

import { patchWithCleanup } from "@web/../tests/web_test_helpers";
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

test("toggle cleans action url when opening/closing the home menu", async () => {
    patchWithCleanup(browser, {
        location: {
            pathname: "/odoo/action-dipl_web_theme.home_menu",
            search: "?debug=1",
        },
        history: {
            state: {},
            replaceState: (...args) => expect.step(args[2]),
        },
    });

    const state = homeMenuService.start(makeEnv({ currentController: {} }));
    await state.toggle(true);
    await state.toggle(false);

    expect.verifySteps(["/odoo?debug=1", "/odoo?debug=1"]);
});

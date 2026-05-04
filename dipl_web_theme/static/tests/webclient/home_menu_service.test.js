import { describe, expect, test } from "@odoo/hoot";
import { EventBus } from "@odoo/owl";

import { patchWithCleanup } from "@web/../tests/web_test_helpers";
import { registry } from "@web/core/registry";
import { _makeUser, user } from "@web/core/user";

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
    const actionService = {
        async doAction(action) {
            expect.step(`doAction:${action}`);
        },
        async restore() {
            expect.step("restore");
        },
    };
    const state = homeMenuService.start(makeEnv(actionService));
    expect(state.hasHomeMenu).toBe(false);
    expect(await state.toggle(true)).toBe(true);
    expect.verifySteps(["doAction:dipl_web_theme.home_menu"]);
    state.hasHomeMenu = true;
    expect(await state.toggle(false)).toBe(true);
    expect.verifySteps(["restore"]);
});

test("toggle returns false when the action service is unavailable", async () => {
    const state = homeMenuService.start(makeEnv(null));

    expect(await state.toggle(true)).toBe(false);
});

test("toggle uses the registered action instead of router-only state", async () => {
    const actionService = {
        currentController: {},
        async doAction(action) {
            expect.step(`doAction:${action}`);
        },
        async restore() {
            expect.step("restore");
        },
    };

    const state = homeMenuService.start(makeEnv(actionService));
    await state.toggle(true);
    state.hasHomeMenu = true;
    await state.toggle(false);

    expect.verifySteps(["doAction:dipl_web_theme.home_menu", "restore"]);
});

test("registered home action exposes the canonical /odoo/home path", async () => {
    const state = homeMenuService.start(makeEnv({ async doAction() {} }));
    const HomeMenuAction = registry.category("actions").get("dipl_web_theme.home_menu");

    expect(HomeMenuAction.path).toBe("home");
    expect(await state.toggle(true)).toBe(true);
});

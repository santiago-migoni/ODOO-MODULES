import { describe, expect, test } from "@odoo/hoot";
import { EventBus } from "@odoo/owl";

import { patchWithCleanup } from "@web/../tests/web_test_helpers";
import { _makeUser, user } from "@web/core/user";
import { registry } from "@web/core/registry";
import { ControllerNotFoundError } from "@web/webclient/actions/action_service";

import {
    homeMenuService,
    readHomeMenuConfig,
} from "../../src/webclient/home_menu/home_menu_service";

describe.current.tags("headless");

const HOME_MENU_ACTION = "dipl_web_theme.home_menu";

function makeEnv(actionService) {
    return {
        bus: new EventBus(),
        config: {},
        services: {
            action: actionService,
        },
    };
}

function cleanupHomeMenuAction() {
    const actions = registry.category("actions");
    if (actions.contains(HOME_MENU_ACTION)) {
        actions.remove(HOME_MENU_ACTION);
    }
}

test("service is registered in the services registry", () => {
    expect(registry.category("services").get("dipl_home_menu")).toBe(homeMenuService);
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

test("toggle opens the custom home menu action", async () => {
    cleanupHomeMenuAction();
    const actionService = {
        async doAction(action) {
            expect.step(action);
        },
        async restore() {
            expect.step("restore");
        },
    };

    const state = homeMenuService.start(makeEnv(actionService));

    const didOpenHomeMenu = await state.toggle(true);

    expect(didOpenHomeMenu).toBe(true);
    expect.verifySteps([HOME_MENU_ACTION]);
});

test("toggle returns false when the action service is unavailable", async () => {
    cleanupHomeMenuAction();
    const state = homeMenuService.start(makeEnv(undefined));

    expect(await state.toggle(true)).toBe(false);
});

test("toggle safely handles legacy restore errors", async () => {
    cleanupHomeMenuAction();
    const state = homeMenuService.start(
        makeEnv({
            async doAction() {
                expect.step("doAction");
            },
            async restore() {
                throw new ControllerNotFoundError();
            },
        })
    );
    state.hasHomeMenu = true;

    expect(await state.toggle(false)).toBe(false);
});

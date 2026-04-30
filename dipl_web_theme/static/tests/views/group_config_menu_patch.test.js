import { describe, expect, test } from "@odoo/hoot";
import { patchWithCleanup } from "@web/../tests/web_test_helpers";
import { user } from "@web/core/user";
import { GroupConfigMenu } from "@web/views/view_components/group_config_menu";

import "../../src/views/view_components/group_config_menu_patch";

describe.current.tags("headless");

function makeMenu(overrides = {}) {
    const menu = Object.create(GroupConfigMenu.prototype);
    menu.props = {
        activeActions: {},
        configItems: [],
        deleteGroup: () => {},
        dialogClose: [],
        group: {
            groupByField: {},
            value: false,
        },
        list: {},
    };
    Object.assign(menu, overrides);
    return menu;
}

test("automations is hidden when handler is missing", () => {
    patchWithCleanup(user, { isAdmin: true });
    const menu = makeMenu();
    expect(menu.permissions.canEditAutomations).toBe(false);
});

test("automations is shown only when handler exists", () => {
    patchWithCleanup(user, { isAdmin: true });
    const menu = makeMenu({
        _openAutomations: () => {},
    });
    expect(menu.permissions.canEditAutomations).toBe(true);
});

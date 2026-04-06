import { describe, expect, test } from "@odoo/hoot";

import { isTopLevelBackendActionList } from "../../src/views/list/list_renderer_desktop";

describe.current.tags("headless");

function makeRenderer(overrides = {}) {
    const rootList = {};
    const model = { root: rootList };
    rootList.model = model;

    return {
        env: {
            config: {
                actionId: 7,
                actionType: "ir.actions.act_window",
            },
            inDialog: false,
        },
        props: {
            list: rootList,
        },
        ...overrides,
    };
}

test("the list patch only targets top-level backend action lists", () => {
    expect(
        isTopLevelBackendActionList(makeRenderer(), {
            isMobile: () => false,
            isSystem: true,
        })
    ).toBe(true);
});

test("the list patch does not apply to embedded x2many lists", () => {
    const rootList = {};
    const childList = {};
    const model = { root: rootList };
    rootList.model = model;
    childList.model = model;

    expect(
        isTopLevelBackendActionList(
            makeRenderer({
                props: {
                    list: childList,
                },
            }),
            {
                isMobile: () => false,
                isSystem: true,
            }
        )
    ).toBe(false);
});

test("the list patch does not apply in dialogs", () => {
    expect(
        isTopLevelBackendActionList(
            makeRenderer({
                env: {
                    config: {
                        actionId: 7,
                        actionType: "ir.actions.act_window",
                    },
                    inDialog: true,
                },
            }),
            {
                isMobile: () => false,
                isSystem: true,
            }
        )
    ).toBe(false);
});

test("the list patch does not apply on mobile or for non-system users", () => {
    expect(
        isTopLevelBackendActionList(makeRenderer(), {
            isMobile: () => true,
            isSystem: true,
        })
    ).toBe(false);

    expect(
        isTopLevelBackendActionList(makeRenderer(), {
            isMobile: () => false,
            isSystem: false,
        })
    ).toBe(false);
});

test("the list patch requires a full act_window action context", () => {
    expect(
        isTopLevelBackendActionList(
            makeRenderer({
                env: {
                    config: {
                        actionId: false,
                        actionType: "ir.actions.act_window",
                    },
                    inDialog: false,
                },
            }),
            {
                isMobile: () => false,
                isSystem: true,
            }
        )
    ).toBe(false);

    expect(
        isTopLevelBackendActionList(
            makeRenderer({
                env: {
                    config: {
                        actionId: 7,
                        actionType: "ir.actions.server",
                    },
                    inDialog: false,
                },
            }),
            {
                isMobile: () => false,
                isSystem: true,
            }
        )
    ).toBe(false);
});

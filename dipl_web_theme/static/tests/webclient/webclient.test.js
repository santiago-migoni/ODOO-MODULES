import { describe, expect, test } from "@odoo/hoot";

import { patchWithCleanup } from "@web/../tests/web_test_helpers";
import { _makeUser, user } from "@web/core/user";

import { loadDefaultAppWithDiplHomeMenu } from "../../src/webclient/webclient";

describe.current.tags("headless");

test("internal users load the custom home menu before the native app", async () => {
    patchWithCleanup(user, _makeUser({ is_internal_user: true }));

    const webClient = {
        env: {
            services: {
                dipl_home_menu: {
                    async toggle(show) {
                        expect.step(`toggle:${show}`);
                        return true;
                    },
                },
            },
        },
    };

    const result = await loadDefaultAppWithDiplHomeMenu(webClient, async () => {
        expect.step("native");
        return "native";
    });

    expect(result).toBe(true);
    expect.verifySteps(["toggle:true"]);
});

test("the webclient falls back to the native default app when the custom shell returns false", async () => {
    patchWithCleanup(user, _makeUser({ is_internal_user: true }));

    const webClient = {
        env: {
            services: {
                dipl_home_menu: {
                    async toggle() {
                        expect.step("toggle");
                        return false;
                    },
                },
            },
        },
    };

    const result = await loadDefaultAppWithDiplHomeMenu(webClient, async () => {
        expect.step("native");
        return "native";
    });

    expect(result).toBe("native");
    expect.verifySteps(["toggle", "native"]);
});

test("the webclient falls back to the native default app when the custom shell errors", async () => {
    patchWithCleanup(user, _makeUser({ is_internal_user: true }));

    const webClient = {
        env: {
            services: {
                dipl_home_menu: {
                    async toggle() {
                        throw new Error("boom");
                    },
                },
            },
        },
    };

    const result = await loadDefaultAppWithDiplHomeMenu(webClient, async () => "native");

    expect(result).toBe("native");
});

test("public users skip the custom shell and keep the native default app", async () => {
    patchWithCleanup(user, _makeUser({ is_internal_user: false }));

    const webClient = {
        env: {
            services: {
                dipl_home_menu: {
                    async toggle() {
                        expect.step("toggle");
                        return true;
                    },
                },
            },
        },
    };

    const result = await loadDefaultAppWithDiplHomeMenu(webClient, async () => {
        expect.step("native");
        return "native";
    });

    expect(result).toBe("native");
    expect.verifySteps(["native"]);
});

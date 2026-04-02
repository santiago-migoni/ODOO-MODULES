import { registry } from "@web/core/registry";
import { browser } from "@web/core/browser/browser";
import { cookie } from "@web/core/browser/cookie";
import { user } from "@web/core/user";

import { switchColorSchemeItem } from "./color_scheme_menu_items";

const serviceRegistry = registry.category("services");
const userMenuRegistry = registry.category("user_menuitems");

function systemColorScheme() {
    return browser.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
}

function currentColorScheme() {
    return cookie.get("color_scheme");
}

export const colorSchemeService = {
    dependencies: ["ui"],

    start(env, { ui }) {
        userMenuRegistry.add("dipl_web_backend_theme.color_scheme.switch", switchColorSchemeItem);

        const setCurrentColorScheme = (scheme) => {
            let nextScheme = systemColorScheme();
            if (["light", "dark"].includes(scheme)) {
                nextScheme = scheme;
            }
            const currentScheme = currentColorScheme();
            if (!currentScheme) {
                cookie.set("color_scheme", nextScheme);
                if (nextScheme === "dark") {
                    ui.block();
                    browser.location.reload();
                }
                return;
            }
            if (currentScheme !== nextScheme) {
                cookie.set("color_scheme", nextScheme);
                ui.block();
                browser.location.reload();
            }
        };

        setCurrentColorScheme(user.settings.color_scheme);

        return {
            get currentColorScheme() {
                return currentColorScheme();
            },
            get systemColorScheme() {
                return systemColorScheme();
            },
            get userColorScheme() {
                return user.settings.color_scheme;
            },
            async setUserColorScheme(colorScheme) {
                await user.setUserSettings("color_scheme", colorScheme);
                setCurrentColorScheme(colorScheme);
            },
        };
    },
};

serviceRegistry.add("color_scheme", colorSchemeService);

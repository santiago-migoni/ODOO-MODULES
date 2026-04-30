import { describe, expect, test } from "@odoo/hoot";

import { patchWithCleanup } from "@web/../tests/web_test_helpers";
import { browser } from "@web/core/browser/browser";
import { NavBar } from "@web/webclient/navbar/navbar";

import "../../src/webclient/navbar/navbar";

describe.current.tags("headless");

function makeNavBar(overrides = {}) {
    const currentApp =
        overrides.currentApp ||
        {
            name: "Sales",
            webIconData: "data:image/png;base64,AA==",
        };
    const diplHomeMenu =
        overrides.diplHomeMenu ||
        {
            hasBackgroundAction: false,
            hasHomeMenu: false,
            toggle() {},
        };
    const isScopedApp = overrides.isScopedApp || false;
    const state = overrides.state || {
        isAppMenuSidebarOpened: false,
    };

    const navbar = Object.create(NavBar.prototype);
    navbar.diplHomeMenu = diplHomeMenu;
    navbar.state = state;
    navbar.env = { _t: (s) => s };

    Object.defineProperties(navbar, {
        currentApp: {
            configurable: true,
            get: () => currentApp,
        },
        isScopedApp: {
            configurable: true,
            get: () => isScopedApp,
        },
    });

    return navbar;
}

test("navbar keeps web.NavBar as its template base", () => {
    expect(NavBar.template).toBe("web.NavBar");
});

test("navbar exposes in-app flags when the custom home menu is closed", () => {
    const navbar = makeNavBar();

    expect(navbar.showMenuToggle).toBe(true);
    expect(navbar.showAppBrand).toBe(true);
    expect(navbar.showBreadcrumbs).toBe(true);
    expect(navbar.showSectionsMenu).toBe(true);
    expect(navbar.menuToggleClasses.o_hidden).toBe(false);
});

test("navbar exposes previous-view state when the home menu overlays a background action", () => {
    const navbar = makeNavBar({
        diplHomeMenu: {
            hasBackgroundAction: true,
            hasHomeMenu: true,
            toggle() {},
        },
    });

    expect(navbar.hasBackgroundAction).toBe(true);
    expect(navbar.hasHomeMenu).toBe(true);
    expect(navbar.isInApp).toBe(false);
    expect(navbar.menuToggleClasses.o_menu_toggle_back).toBe(true);
});

test("opening the sidebar from the home menu closes the custom shell instead", () => {
    let toggleArg;
    const navbar = makeNavBar({
        diplHomeMenu: {
            hasBackgroundAction: false,
            hasHomeMenu: true,
            toggle(show) {
                toggleArg = show;
            },
        },
    });

    navbar._openAppMenuSidebar();

    expect(toggleArg).toBe(false);
    expect(navbar.state.isAppMenuSidebarOpened).toBe(false);
});

test("all apps button redirects to /odoo/home", () => {
    let redirectedTo;
    patchWithCleanup(browser, {
        location: {
            assign(url) {
                redirectedTo = url;
            },
        },
    });
    const navbar = makeNavBar();
    navbar._closeAppMenuSidebar = () => {
        navbar.state.isAppMenuSidebarOpened = false;
    };

    navbar.onAllAppsBtnClick();

    expect(redirectedTo).toBe("/odoo/home");
});

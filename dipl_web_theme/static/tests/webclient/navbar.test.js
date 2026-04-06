import { describe, expect, test } from "@odoo/hoot";

import { NavBar } from "@web/webclient/navbar/navbar";

import "../../src/webclient/navbar/navbar";

describe.current.tags("headless");

function makeNavBar(overrides = {}) {
    return Object.assign(Object.create(NavBar.prototype), {
        currentApp: {
            name: "Sales",
            webIconData: "data:image/png;base64,AA==",
        },
        diplHomeMenu: {
            hasBackgroundAction: false,
            hasHomeMenu: false,
            toggle() {},
        },
        isScopedApp: false,
        state: {
            isAppMenuSidebarOpened: false,
        },
        ...overrides,
    });
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

    expect(navbar.showAppBrand).toBe(false);
    expect(navbar.showBreadcrumbs).toBe(false);
    expect(navbar.showSectionsMenu).toBe(false);
    expect(navbar.menuToggleClasses.o_menu_toggle_back).toBe(true);
    expect(navbar.menuToggleTitle).toBe("Previous view");
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

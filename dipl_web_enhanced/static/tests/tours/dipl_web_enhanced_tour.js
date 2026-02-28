/** @odoo-module **/

import { registry } from "@web/core/registry";
import { stepUtils } from "@web_tour/tour_service/tour_utils";

registry.category("web_tour.tours").add('dipl_web_enhanced_tour', {
    test: true,
    url: '/web',
    steps: () => [
        // 1. Wait for the Home Menu to be present which validates our `home_menu` service injection
        {
            content: "Check if the Home Menu background is visible",
            trigger: 'body.o_home_menu_background',
            run: () => {}, // Just verifying it exists
        },
        // 2. Click on the first visible app icon
        {
            content: "Click on the first app in the Home Menu",
            trigger: '.o_app:first',
            run: 'click',
        },
        // 3. Ensure we are inside an app and the Home Menu background is gone
        {
            content: "Verify we entered an app and background changed",
            trigger: 'body:not(.o_home_menu_background)',
            run: () => {},
        },
        // 4. Click the app switcher icon in the navbar (this uses our patched NavBar)
        {
            content: "Click the home menu / app switcher toggle in the navbar",
            trigger: '.o_navbar_apps_menu button',
            run: 'click',
        },
        // 5. Verify the Home Menu returns
        {
            content: "Check if the Home Menu returned",
            trigger: 'body.o_home_menu_background',
            run: () => {}, // Just verifying it arrived
        }
    ]
});

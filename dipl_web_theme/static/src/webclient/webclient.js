import { user } from "@web/core/user";
import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";

patch(WebClient.prototype, {
    async _loadDefaultApp() {
        const diplHomeMenu = this.env.services.dipl_home_menu;
        if (diplHomeMenu && user.isInternalUser) {
            try {
                const didOpenHomeMenu = await diplHomeMenu.toggle(true);
                if (didOpenHomeMenu !== false) {
                    return didOpenHomeMenu;
                }
            } catch {
                // Fall back to the native webclient behavior when the custom shell
                // cannot open its home menu safely.
            }
        }
        return super._loadDefaultApp(...arguments);
    },
});

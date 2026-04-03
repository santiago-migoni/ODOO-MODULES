import { user } from "@web/core/user";
import { patch } from "@web/core/utils/patch";
import { WebClient } from "@web/webclient/webclient";

patch(WebClient.prototype, {
    _loadDefaultApp() {
        const diplHomeMenu = this.env.services.dipl_home_menu;
        if (diplHomeMenu && user.isInternalUser) {
            return diplHomeMenu.toggle(true);
        }
        return super._loadDefaultApp(...arguments);
    },
});

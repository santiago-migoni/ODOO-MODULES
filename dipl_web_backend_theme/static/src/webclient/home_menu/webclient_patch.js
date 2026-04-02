import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { WebClient } from "@web/webclient/webclient";

patch(WebClient.prototype, {
    setup() {
        super.setup(...arguments);
        this.homeMenu = useService("home_menu");
    },

    _loadDefaultApp() {
        return this.homeMenu.toggle(true);
    },
});

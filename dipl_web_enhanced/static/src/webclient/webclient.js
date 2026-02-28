import { WebClient } from "@web/webclient/webclient";
import { useService } from "@web/core/utils/hooks";
import { patch } from "@web/core/utils/patch";

patch(WebClient.prototype, {
    setup() {
        super.setup(...arguments);
        this.hm = useService("home_menu");
    },
    _loadDefaultApp() {
        return this.hm.toggle(true);
    }
});

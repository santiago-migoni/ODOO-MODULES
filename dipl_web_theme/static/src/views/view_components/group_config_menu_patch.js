import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { user } from "@web/core/user";
import { patch } from "@web/core/utils/patch";
import { GroupConfigMenu } from "@web/views/view_components/group_config_menu";

patch(GroupConfigMenu.prototype, {
    /**
     * @override
     */
    get permissions() {
        const permissions = super.permissions;
        const canOpenAutomations = typeof this._openAutomations === "function";
        return {
            ...permissions,
            canEditAutomations:
                permissions.canEditAutomations ?? (user.isAdmin && canOpenAutomations),
        };
    },

    async openAutomations() {
        if (typeof this._openAutomations === "function") {
            // this is the case if base_automation is installed
            return this._openAutomations();
        }
    },
});

registry.category("group_config_items").add(
    "open_automations",
    {
        label: _t("Automations"),
        method: "openAutomations",
        isVisible: ({ permissions }) => permissions.canEditAutomations,
        class: "o_column_automations",
        icon: "fa-magic",
    },
    { sequence: 25, force: true }
);

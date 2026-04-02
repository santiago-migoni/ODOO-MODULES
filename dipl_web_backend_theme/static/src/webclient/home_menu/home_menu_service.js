import { Component, onMounted, onWillUnmount, reactive, xml } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { registry } from "@web/core/registry";
import { Mutex } from "@web/core/utils/concurrency";
import { useBus, useService } from "@web/core/utils/hooks";
import {
    ControllerNotFoundError,
    standardActionServiceProps,
} from "@web/webclient/actions/action_service";
import { computeAppsAndMenuItems } from "@web/webclient/menus/menu_helpers";

import { DiplegHomeMenu } from "./home_menu";

export const homeMenuService = {
    dependencies: ["action"],
    start(env) {
        const state = reactive({
            hasHomeMenu: false,
            hasBackgroundAction: false,
            toggle,
        });
        const mutex = new Mutex();

        class HomeMenuAction extends Component {
            static components = { DiplegHomeMenu };
            static target = "current";
            static props = { ...standardActionServiceProps };
            static template = xml`<DiplegHomeMenu apps="apps"/>`;
            static displayName = _t("Home");

            setup() {
                this.menuService = useService("menu");
                useBus(this.env.bus, "MENUS:APP-CHANGED", () => this.render());
                onMounted(() => {
                    const { breadcrumbs } = this.env.config;
                    state.hasHomeMenu = true;
                    state.hasBackgroundAction = breadcrumbs.length > 0;
                    this.env.bus.trigger("HOME-MENU:TOGGLED");
                });
                onWillUnmount(() => {
                    state.hasHomeMenu = false;
                    state.hasBackgroundAction = false;
                    this.env.bus.trigger("HOME-MENU:TOGGLED");
                });
            }

            get apps() {
                return computeAppsAndMenuItems(this.menuService.getMenuAsTree("root")).apps;
            }
        }

        registry.category("actions").add("menu", HomeMenuAction);

        env.bus.addEventListener("HOME-MENU:TOGGLED", () => {
            document.body.classList.toggle("dipl-home-menu-open", state.hasHomeMenu);
        });

        async function toggle(show) {
            return mutex.exec(async () => {
                const nextState = show === undefined ? !state.hasHomeMenu : Boolean(show);
                if (nextState === state.hasHomeMenu) {
                    return;
                }
                if (nextState) {
                    await env.services.action.doAction("menu");
                } else {
                    try {
                        await env.services.action.restore();
                    } catch (error) {
                        if (!(error instanceof ControllerNotFoundError)) {
                            throw error;
                        }
                    }
                }
                return new Promise((resolve) => setTimeout(resolve));
            });
        }

        return state;
    },
};

registry.category("services").add("home_menu", homeMenuService);

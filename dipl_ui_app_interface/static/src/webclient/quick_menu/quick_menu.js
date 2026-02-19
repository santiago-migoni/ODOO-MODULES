/** @odoo-module **/
import { Component, useState, useRef, useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService, useBus } from "@web/core/utils/hooks";
import { user } from "@web/core/user";

/**
 * QuickMenu — Sidebar de acceso rápido a apps favoritas.
 *
 * Se monta en el WebClient y aparece como un panel lateral izquierdo
 * que se expande al pasar el mouse o al hacer clic en el botón de pin.
 */
export class QuickMenu extends Component {
    static template = "dipl_ui_app_interface.QuickMenu";
    static props = {};

    setup() {
        this.menus = useService("menu");
        this.homeMenu = useService("home_menu");
        this.state = useState({
            expanded: false,
        });
        this.rootRef = useRef("root");

        // Forzar colapso al cambiar de menú o entrar/salir del inicio
        useBus(this.env.bus, "HOME-MENU:TOGGLED", () => {
            this.state.expanded = false;
            this.clickLock = false;
        });

        // Add class to root to adjust layout (push content)
        useEffect(() => {
            document.documentElement.classList.add("dipl_has_quick_menu");
            return () => {
                document.documentElement.classList.remove("dipl_has_quick_menu");
            };
        }, () => []);
    }

    // -------------------------------------------------------------------------
    // Getters
    // -------------------------------------------------------------------------

    get isVisible() {
        // Hide if Home Menu is active
        return !this.homeMenu.hasHomeMenu;
    }

    get allApps() {
        return this.menus.getApps();
    }

    /**
     * Returns the first few apps to show in the rail.
     * Showing top 10 apps as requested.
     */
    get featuredApps() {
        return this.allApps.slice(0, 10);
    }

    // -------------------------------------------------------------------------
    // Handlers
    // -------------------------------------------------------------------------

    /**
     * Toggles the Home Menu visibility (the "Casita" action).
     */
    async navigateToHome() {
        await this.homeMenu.toggle();
    }

    onMouseEnter() {
        if (!this.clickLock) {
            this.state.expanded = true;
        }
    }

    onMouseLeave() {
        this.state.expanded = false;
        this.clickLock = false; // Permite hover de nuevo
    }

    onAppClick(app) {
        this.state.expanded = false;
        this.clickLock = true; // Bloquea reapertura inmediata
        this.menus.selectMenu(app);

        // El bloqueo se quita al salir (onMouseLeave) o tras un timeout de seguridad
        setTimeout(() => {
            this.clickLock = false;
        }, 1500);
    }
}

registry.category("main_components").add("DiplQuickMenu", {
    Component: QuickMenu,
    props: {},
});

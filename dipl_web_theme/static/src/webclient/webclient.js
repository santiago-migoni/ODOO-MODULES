// Intentionally empty: the home launcher is now isolated behind /odoo/home.
export function loadDefaultAppWithDiplHomeMenu(_webClient, nativeLoadDefaultApp, args = []) {
    return nativeLoadDefaultApp(...args);
}

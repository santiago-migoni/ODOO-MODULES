# OWL Component Constraints (JavaScript / Frontend)

Rules for building OWL 2.x reactive components in Odoo 19. These apply whenever you create or modify JavaScript components in `static/src/`.

## MUST DO

- **`setup()` only**: Initialize state, hooks, and services in `setup()` — NEVER in a constructor. `setup()` enables Odoo's `patch()` extensibility pattern.
- **`useState` for reactivity**: All mutable component state MUST go through `useState`. OWL uses JavaScript Proxy objects to track mutations and schedule async re-renders of only the affected DOM subtree.
- **`useService()` for dependency injection**: Access Odoo services inside `setup()`:

```javascript
import { Component, useState } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";

export class MyDashboard extends Component {
    static template = "dipl_module.MyDashboard";
    static props = {
        recordId: { type: Number },
        title: { type: String, optional: true },
    };

    setup() {
        this.state = useState({ loading: true, data: null });
        this.orm = useService("orm");
        this.action = useService("action");
        this.notification = useService("notification");
    }

    async loadData() {
        this.state.data = await this.orm.call("dipl.model", "read", [this.props.recordId]);
        this.state.loading = false;
    }
}
```

- **Props validation**: Always declare `static props` with types (`Number`, `String`, `Boolean`, `Object`, `Array`, `Function`) and `optional: true` where applicable. This catches integration errors at render time.
- **Lifecycle hooks**: Use the complete set as needed:

| Hook | When | Use For |
|---|---|---|
| `onWillStart` | Before first render (async) | RPC calls to load initial data from backend |
| `onMounted` | After DOM insertion | Initialize third-party libraries, attach event listeners |
| `onWillUpdateProps` | Before re-render from parent | Validate or transform incoming props |
| `onWillRender` | Before each render cycle | Last-moment state adjustments |
| `onRendered` | After each render cycle | Post-render DOM measurements |
| `onWillDestroy` | Before component removal | **CRITICAL**: Clean up listeners, timers, subscriptions — prevents memory leaks |
| `onError` | When child component throws | Error boundaries — graceful degradation |

- **`useEffect()` for side effects**: React to state/prop changes with automatic cleanup:

```javascript
import { useEffect } from "@odoo/owl";

setup() {
    this.state = useState({ partnerId: null });
    useEffect(
        () => { /* effect runs when partnerId changes */ },
        () => [this.state.partnerId]  // dependencies
    );
}
```

- **`patch()` for extending core components**: Never copy-paste core components. Use `patch` to modify behavior non-destructively:

```javascript
import { patch } from "@web/core/utils/patch";
import { FormController } from "@web/views/form/form_controller";

patch(FormController.prototype, {
    setup() {
        super.setup(...arguments);
        // Additional initialization
    },
});
```

- **Template externalization**: Templates MUST reside in separate `.xml` files referenced by `static template = "dipl_module.ComponentName"`. This enables i18n, XPath inheritance by other modules, and separation of concerns.
- **Registry registration**: Custom views/actions MUST register in the global registry:

```javascript
import { registry } from "@web/core/registry";
registry.category("views").add("my_custom_view", MyCustomView);
```

## MUST NOT DO

- **NEVER** use legacy `Widget` classes — OWL 2.x components only.
- **NEVER** use jQuery for DOM manipulation — rely entirely on OWL reactivity (`useState`, `useEffect`).
- **NEVER** use constructors — use `setup()` (constructors break `patch()` extensibility).
- **NEVER** replace state object references — mutate through the proxy (`this.state.key = value`, not `this.state = newObj`).
- **NEVER** skip `onWillDestroy` cleanup — leaked event listeners and timers degrade browser performance progressively.
- **NEVER** use `t-raw` in OWL templates — use `t-out` for safe output (XSS prevention).
- **NEVER** write inline templates as strings — always use externalized XML files.

## Asset Registration (JS/XML)

OWL components MUST be registered in `__manifest__.py`:

```python
"assets": {
    "web.assets_backend": [
        "dipl_module/static/src/components/**/*.js",
        "dipl_module/static/src/components/**/*.xml",
        "dipl_module/static/src/components/**/*.scss",
    ],
},
```

- `web.assets_backend` — internal/admin UI components.
- `web.assets_frontend` — portal/e-commerce facing components.

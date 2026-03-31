---
trigger:
globs: "**/static/src/**/*.js", "**/static/src/**/*.xml", "**/static/src/**/*.scss"
phase: f4
description: OWL component conventions and architecture
---

# owl-frontend

OWL (Odoo Web Library) is the reactive frontend framework consolidated in Odoo 18/19. All custom interactive components MUST follow these conventions.

## Four Architectural Pillars

### 1. Class Definition & Setup

Components extend `owl.Component`. Use `setup()` instead of constructors for state initialization — this enables Odoo's extensibility pattern (patching without destructive overrides).

```javascript
import { Component, useState } from "@odoo/owl";

export class MyDashboard extends Component {
    static template = "dipl_module.MyDashboard";
    static props = { recordId: { type: Number } };

    setup() {
        this.state = useState({ loading: true, data: null });
        // Use hooks here, not in constructor
    }
}
```

### 2. Reactive State (`useState`)

OWL uses JavaScript Proxy objects via `useState` to intercept and track mutations. When state changes, OWL schedules an **asynchronous re-render** of only the affected DOM subtree — minimizing browser reflows.

- Always mutate state through the proxy, never replace the object reference.
- Avoid deep nesting in state — keep it flat for performance.

### 3. Externalized XML Templates

Templates reside in separate XML files, referenced via `static template`. This separation enables:

- i18n processing by Odoo's translation engine.
- XPath inheritance by other modules.
- Clean separation of concerns (logic vs presentation).

```xml
<?xml version="1.0" encoding="UTF-8"?>
<templates xml:space="preserve">
    <t t-name="dipl_module.MyDashboard">
        <div class="o_my_dashboard">
            <t t-if="state.loading">Loading...</t>
            <t t-else="">
                <span t-esc="state.data.name"/>
            </t>
        </div>
    </t>
</templates>
```

### 4. Lifecycle Hooks

| Hook | Purpose | Common Use |
|---|---|---|
| `onWillStart` | Async setup before first render | RPC calls to load initial data from backend |
| `onMounted` | After DOM insertion | Initialize third-party libraries, attach event listeners |
| `onWillUpdateProps` | Before re-render from parent | Validate incoming prop changes |
| `onWillDestroy` | Before component removal | Clean up listeners, timers, prevent memory leaks |

## Asset Registration

Components and templates MUST be registered in the correct asset bundle via `__manifest__.py`:

```python
"assets": {
    "web.assets_backend": [
        "dipl_module/static/src/components/**/*.js",
        "dipl_module/static/src/components/**/*.xml",
        "dipl_module/static/src/components/**/*.scss",
    ],
},
```

- `web.assets_backend` — for internal/admin UI components.
- `web.assets_frontend` — for portal/e-commerce facing components.

## Service Registration

Custom views or actions must register in the global registry:

```javascript
import { registry } from "@web/core/registry";
registry.category("views").add("my_custom_view", MyCustomView);
```

## Rules

- Use `t-esc` or `t-out` for safe output (XSS prevention). Never use `t-raw` unless explicitly justified.
- Always clean up in `onWillDestroy` — leaked listeners degrade browser performance.
- Template names MUST be namespaced: `dipl_module.ComponentName`.
- One component per JS file. File name matches component name in snake_case.
- SCSS files scoped to component class to prevent style bleeding.

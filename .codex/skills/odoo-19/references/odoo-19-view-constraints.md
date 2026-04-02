# View Architecture Constraints (XML / UI)

Rules for writing Odoo 19 XML views, actions, menus, and QWeb templates. These apply whenever you create or modify UI definitions.

## MUST DO

- **`invisible=` directo**: Use `invisible="condition"` as a direct attribute — NEVER use legacy `attrs={"invisible": [(...)]}"`. This is the most critical Odoo 19 convention for views.
- **`<list>` not `<tree>`**: Always use `<list>` as root element for list views. `<tree>` is deprecated in Odoo 19.
- **View structure**: Organize forms with `<header>` (status bar, buttons) → `<sheet>` (content) → `<notebook>` (tabs) → `<group>` (field layout). Place `<chatter/>` after `</sheet>` for mail.thread models.
- **XPath inheritance**: Use `inherit_id` + `<xpath expr="..." position="...">`. Prefer `position="after"`, `"before"`, or `"inside"` over `"replace"` (replace risks breaking other inheriting modules). Use precise XPath expressions targeting `name` attributes: `//field[@name='partner_id']`.
- **Search views**: Define `<filter>` for common business queries, `<group>` for group-by options, `<searchpanel>` for sidebar filtering. Predefine useful domain filters.
- **Actions**: Use `ir.actions.act_window` with explicit `res_model`, `view_mode`, and `domain`. Bind to menus via `<menuitem action="..."/>`.
- **Widgets**: Use modern Odoo 19 widgets appropriately:

| Widget | Use Case |
|---|---|
| `statusbar` | State/selection field in `<header>` — shows pipeline stages |
| `many2many_tags` | Compact tag display for M2M fields |
| `many2many_tags_avatar` | Tags with user avatars (e.g., assignees) |
| `handle` | Drag-and-drop reordering (on `sequence` field) |
| `priority` | Star rating (on selection field) |
| `progressbar` | Visual progress indicator |
| `radio` | Radio buttons for selection fields |
| `image` | Image display/upload |
| `color_picker` | Color selection |
| `monetary` | Currency-aware amount display (pair with `currency_id`) |

- **CSS classes**: Use Odoo standard classes (`oe_highlight`, `oe_stat_button`, `o_field_widget`, `oe_title`) — never inline `style=` attributes.

## Kanban Views

Kanban views require QWeb templates inside `<templates>` / `<t t-name="card">`:

- Use `t-if` / `t-elif` for conditional rendering.
- Use `t-esc` or `t-out` for safe variable output (XSS prevention) — NEVER `t-raw` unless explicitly justified.
- Use `widget="handle"` on sequence fields for drag-and-drop reordering.
- Use `default_group_by` attribute on `<kanban>` for default stage grouping.
- Kanban cards support `<field>`, `<widget>`, and direct QWeb directives — they are NOT standard form views.

## Pivot & Graph Views

Critical for management dashboards and financial analysis:

```xml
<!-- Pivot: multidimensional data crossing -->
<pivot string="Sales Analysis" disable_linking="1">
    <field name="date_order" type="row"/>
    <field name="product_categ_id" type="col"/>
    <field name="amount_total" type="measure"/>
</pivot>

<!-- Graph: visual chart -->
<graph string="Revenue by Month" type="bar">
    <field name="date_order" type="row"/>
    <field name="amount_total" type="measure"/>
</graph>
```

- `type="row"` — horizontal grouping axis.
- `type="col"` — vertical segmentation axis.
- `type="measure"` — aggregated metric (sum, avg) at axis intersections.
- `disable_linking="1"` — prevents drill-down to individual records (useful for read-only dashboards).

## MUST NOT DO

- **NEVER** use inline `style="..."` in XML views — use CSS classes or SCSS in `static/`.
- **NEVER** use `t-raw` in QWeb templates — it bypasses XSS escaping. Use `t-out` instead.
- **NEVER** use `attrs={"invisible": ...}` — use direct `invisible="..."` attribute (Odoo 19).
- **NEVER** use deprecated widgets from v15/v16 without checking Odoo 19 compatibility.
- **NEVER** use `position="replace"` in XPath unless the original element genuinely needs removal — it breaks downstream inheritors.
- **NEVER** hardcode display strings in XML — always use translatable strings via `_()` in Python or translation-ready attributes.

## Asset Registration (CSS/SCSS)

Custom styles for views MUST be registered in `__manifest__.py`:

```python
"assets": {
    "web.assets_backend": [
        "dipl_module/static/src/**/*.scss",
    ],
},
```

Scope SCSS to module-specific classes to prevent style bleeding across modules.

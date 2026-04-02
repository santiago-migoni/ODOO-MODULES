# Theme & Styling Constraints (SCSS / Bootstrap / QWeb Reports)

Rules for developing Odoo 19 website themes, styling backend/frontend interfaces, creating QWeb printable reports, and building website snippets. These apply whenever you work with SCSS, Bootstrap overrides, QWeb templates for website/reports, or the website builder.

## Asset Bundles — When to Use Each

| Bundle | Scope | Use For |
|---|---|---|
| `web.assets_backend` | Internal admin UI | Backend SCSS, OWL component styles, admin dashboard themes |
| `web.assets_frontend` | Public website, portal | Website themes, portal styles, e-commerce layouts |
| `website.assets_wysiwyg` | Website builder editor | Snippet editor styles, drag-and-drop UI customization |
| `web.report_assets_common` | QWeb PDF/HTML reports | Report-specific styles, print layouts, paper format overrides |

Register in `__manifest__.py`:

```python
"assets": {
    "web.assets_frontend": [
        ("prepend", "dipl_module/static/src/scss/_variables.scss"),  # Before Bootstrap
        "dipl_module/static/src/scss/theme.scss",                    # After Bootstrap
    ],
    "web.report_assets_common": [
        "dipl_module/static/src/scss/report.scss",
    ],
},
```

**Asset ordering matters**: Use `("prepend", ...)` for variable overrides that must load before Bootstrap. Default append loads after.

## SCSS Architecture

### Bootstrap 5 Variable Overrides

Odoo 19 uses Bootstrap 5 as its CSS framework. Override variables cleanly — never patch compiled CSS:

```scss
// _variables.scss — MUST be prepended before Bootstrap compilation
$o-brand-odoo: #7C6192;           // Odoo brand color
$o-enterprise-color: #714B67;      // Enterprise accent
$primary: #2C5F2D;                 // Your brand primary
$secondary: #6B717E;               // Your brand secondary
$font-family-base: 'Inter', sans-serif;
$border-radius: 0.375rem;
$enable-rounded: true;
```

### File Organization

```
dipl_module/
└── static/
    └── src/
        └── scss/
            ├── _variables.scss    # Bootstrap/Odoo variable overrides (prepend)
            ├── _mixins.scss       # Reusable SCSS mixins
            ├── theme.scss         # Main theme styles
            ├── report.scss        # Print/report-specific styles
            └── snippets/          # Website snippet styles
                └── s_custom.scss
```

### MUST DO

- **Variable-first approach**: Override Bootstrap/Odoo SCSS variables (`$primary`, `$font-family-base`, etc.) instead of writing raw CSS rules. This ensures consistency across all Odoo components.
- **Use Bootstrap 5 utilities**: `d-flex`, `justify-content-between`, `text-muted`, `rounded`, `shadow-sm`, etc. Never reinvent grid/spacing/typography.
- **Scope custom styles**: Prefix custom classes with module name (`dipl_module_card`, `dipl_module_header`) or use Odoo conventions (`o_dipl_*`) to prevent bleeding.
- **Use SCSS nesting sparingly**: Max 3 levels deep. Overly nested SCSS generates bloated CSS selectors.
- **Responsive design**: Use Bootstrap breakpoints (`@include media-breakpoint-up(md)`) — never hardcode `@media` pixel values.

### MUST NOT DO

- **NEVER** modify core Odoo/Bootstrap CSS directly — always use asset overriding via `__manifest__.py`.
- **NEVER** use `!important` unless overriding a third-party library with no other option.
- **NEVER** hardcode pixel values for layouts — use Bootstrap grid (`col-*`), spacing utilities (`p-3`, `m-2`), and relative units (`rem`, `em`).
- **NEVER** inline `style="..."` in XML/QWeb templates — use CSS classes.
- **NEVER** use deprecated CSS properties without autoprefixer coverage.

## Website Snippets

Snippets are drag-and-drop content blocks in the website builder. Structure:

### Snippet Definition (XML)

```xml
<!-- Template: the visual block -->
<template id="s_dipl_cta" name="Dipleg CTA Block">
    <section class="s_dipl_cta pt32 pb32">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-8">
                    <h2>Ready to get started?</h2>
                    <p class="lead text-muted">Contact us today.</p>
                </div>
                <div class="col-lg-4 text-end">
                    <a href="/contactus" class="btn btn-primary btn-lg">Contact Us</a>
                </div>
            </div>
        </div>
    </section>
</template>

<!-- Register snippet in the website builder palette -->
<template id="s_dipl_cta_snippet" inherit_id="website.snippets" name="Dipleg CTA Snippet">
    <xpath expr="//we-select[@data-variable-name='content-snippet']" position="inside">
        <we-button data-snippet="s_dipl_cta"
                   data-name="Dipleg CTA">
            <img src="/dipl_module/static/src/img/snippets/s_dipl_cta.png" loading="lazy"/>
        </we-button>
    </xpath>
</template>
```

### Snippet Naming Convention

- Template IDs: `s_dipl_<name>` (prefix `s_` is Odoo convention for snippets).
- CSS classes: match template ID (`s_dipl_cta`).
- Thumbnail: provide a preview image in `static/src/img/snippets/`.

### Snippet Options (JS)

For configurable snippets with editor options:

```javascript
import { SnippetOption } from "@website/js/editor/snippets.options";

export class DiplCtaOption extends SnippetOption {
    // Custom editor options for the snippet
}
```

## QWeb Reports (PDF/HTML)

### Report Structure

```xml
<template id="report_dipl_document">
    <t t-call="web.html_container">
        <t t-foreach="docs" t-as="doc">
            <t t-call="web.external_layout">
                <div class="page">
                    <h2><t t-out="doc.name"/></h2>
                    <!-- Report content -->
                </div>
            </t>
        </t>
    </t>
</template>
```

### Key Patterns

- **`web.external_layout`**: Wraps report with company header/footer. Use for official documents (invoices, quotes, delivery slips).
- **`web.internal_layout`**: Minimal layout without header/footer. Use for internal reports.
- **`web.html_container`**: Base HTML wrapper. Always use as outermost call.
- **`t-out`** for safe output — NEVER `t-raw`.
- **`t-call`** for reusable sub-templates.

### Custom Paper Format

```xml
<record id="paperformat_dipl_landscape" model="report.paperformat">
    <field name="name">Dipleg Landscape</field>
    <field name="format">A4</field>
    <field name="orientation">Landscape</field>
    <field name="margin_top">30</field>
    <field name="margin_bottom">20</field>
    <field name="margin_left">10</field>
    <field name="margin_right">10</field>
    <field name="header_spacing">20</field>
    <field name="dpi">90</field>
</record>
```

### Print-Specific CSS

```scss
// report.scss — registered in web.report_assets_common
.dipl_report_table {
    width: 100%;
    border-collapse: collapse;

    th {
        background-color: $primary;
        color: white;
        padding: 8px;
    }

    td {
        padding: 6px 8px;
        border-bottom: 1px solid $gray-300;
    }
}

@media print {
    .page-break {
        page-break-before: always;
    }

    .no-print {
        display: none !important;
    }
}
```

### Report Action

```xml
<record id="action_report_dipl_document" model="ir.actions.report">
    <field name="name">Dipleg Document</field>
    <field name="model">dipl.model</field>
    <field name="report_type">qweb-pdf</field>
    <field name="report_name">dipl_module.report_dipl_document</field>
    <field name="report_file">dipl_module.report_dipl_document</field>
    <field name="paperformat_id" ref="paperformat_dipl_landscape"/>
    <field name="binding_model_id" ref="model_dipl_model"/>
    <field name="binding_type">report</field>
</record>
```

## Fonts & Icons

### Custom Fonts

Register in assets with `@font-face` or import from CDN:

```scss
// In _variables.scss or theme.scss
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
$font-family-base: 'Inter', sans-serif;
```

### Odoo Icon Set

Odoo 19 uses Font Awesome 6 (free subset) + custom Odoo icons (`oi-*`):

```xml
<i class="fa fa-check"/>        <!-- Font Awesome -->
<i class="oi oi-settings"/>     <!-- Odoo custom icons -->
```

Use `fa` classes for standard icons, `oi` for Odoo-specific icons. Check availability in `web/static/src/libs/fontawesome/` and `web/static/src/core/icons/`.

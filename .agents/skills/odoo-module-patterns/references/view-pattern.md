# View Pattern — Dipleg Odoo 19

Complete XML template for form, list, search views, action and menuitem.

## Views File (`views/{name}_views.xml`)

```xml
<?xml version="1.0" encoding="utf-8"?>
<odoo>

    <!-- ============ FORM VIEW ============ -->
    <record id="dipl_example_view_form" model="ir.ui.view">
        <field name="name">dipl.example.form</field>
        <field name="model">dipl.example</field>
        <field name="arch" type="xml">
            <form>
                <header>
                    <button name="action_confirm"
                            string="Confirm"
                            type="object"
                            class="btn-primary"
                            invisible="state != 'draft'"/>
                    <button name="action_cancel"
                            string="Cancel"
                            type="object"
                            invisible="state in ('cancelled', 'done')"/>
                    <field name="state" widget="statusbar"
                           statusbar_visible="draft,confirmed,done"/>
                </header>
                <sheet>
                    <div class="oe_title">
                        <label for="name"/>
                        <h1>
                            <field name="name" placeholder="Name..."/>
                        </h1>
                    </div>
                    <group>
                        <group name="left">
                            <field name="partner_id"/>
                            <field name="company_id"
                                   groups="base.group_multi_company"/>
                        </group>
                        <group name="right">
                            <field name="total"/>
                            <field name="active" invisible="1"/>
                        </group>
                    </group>
                    <notebook>
                        <page string="Lines" name="lines">
                            <field name="line_ids">
                                <list editable="bottom">
                                    <field name="name"/>
                                    <field name="amount"/>
                                </list>
                            </field>
                        </page>
                        <page string="Notes" name="notes">
                            <field name="note" placeholder="Internal notes..."/>
                        </page>
                    </notebook>
                </sheet>
                <chatter/>
            </form>
        </field>
    </record>

    <!-- ============ LIST VIEW ============ -->
    <!-- Odoo 19: use <list>, NOT <tree> -->
    <record id="dipl_example_view_list" model="ir.ui.view">
        <field name="name">dipl.example.list</field>
        <field name="model">dipl.example</field>
        <field name="arch" type="xml">
            <list string="Examples" multi_edit="1">
                <field name="sequence" widget="handle"/>
                <field name="name"/>
                <field name="partner_id"/>
                <field name="total" sum="Total"/>
                <field name="state"
                       decoration-success="state == 'done'"
                       decoration-info="state == 'confirmed'"
                       decoration-muted="state == 'cancelled'"
                       widget="badge"/>
                <field name="company_id" optional="hide"
                       groups="base.group_multi_company"/>
            </list>
        </field>
    </record>

    <!-- ============ SEARCH VIEW ============ -->
    <record id="dipl_example_view_search" model="ir.ui.view">
        <field name="name">dipl.example.search</field>
        <field name="model">dipl.example</field>
        <field name="arch" type="xml">
            <search>
                <field name="name"/>
                <field name="partner_id"/>
                <filter name="filter_draft" string="Draft"
                        domain="[('state', '=', 'draft')]"/>
                <filter name="filter_confirmed" string="Confirmed"
                        domain="[('state', '=', 'confirmed')]"/>
                <separator/>
                <filter name="filter_archived" string="Archived"
                        domain="[('active', '=', False)]"/>
                <group expand="0" string="Group By">
                    <filter name="groupby_state" string="State"
                            context="{'group_by': 'state'}"/>
                    <filter name="groupby_partner" string="Partner"
                            context="{'group_by': 'partner_id'}"/>
                </group>
            </search>
        </field>
    </record>

    <!-- ============ ACTION ============ -->
    <record id="dipl_example_action" model="ir.actions.act_window">
        <field name="name">Examples</field>
        <field name="res_model">dipl.example</field>
        <field name="view_mode">list,form</field>
        <field name="search_view_id" ref="dipl_example_view_search"/>
        <field name="context">{'search_default_filter_draft': 1}</field>
        <field name="help" type="html">
            <p class="o_view_nocontent_smiling_face">
                Create your first example record
            </p>
        </field>
    </record>

    <!-- ============ MENU ============ -->
    <menuitem id="dipl_example_menu_root"
              name="Example"
              sequence="100"/>
    <menuitem id="dipl_example_menu_main"
              name="Examples"
              parent="dipl_example_menu_root"
              action="dipl_example_action"
              sequence="10"/>

</odoo>
```

## Key conventions

- **`<list>` not `<tree>`**: Odoo 19 renamed the list view tag. Using `<tree>` still works but is deprecated.
- **`invisible=` directly**: Never use `attrs={"invisible": [...]}` — use `invisible="condition"` directly.
- **`<chatter/>`**: Shorthand in Odoo 19 for the full chatter block. Requires `mail.thread` mixin.
- **State decorations**: Use `decoration-*` attributes on list fields for color coding.
- **`optional="hide"`**: Use for columns that are rarely needed (e.g., `company_id` in single-company setups).
- **`multi_edit="1"`**: Enables inline editing of multiple selected records in the list view.

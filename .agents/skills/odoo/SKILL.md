---
name: odoo-development
description: Guía experta para el desarrollo en Odoo ERP, incluyendo el ORM de Python, vistas XML y arquitectura de módulos.
---

# Desarrollo en Odoo

Eres un experto en Python, Odoo y el desarrollo de aplicaciones empresariales.

## Principios Clave de Desarrollo

### Calidad de Código y Arquitectura

- Escribe respuestas técnicas claras con ejemplos precisos de Odoo en Python, XML y JSON.
- Aprovecha el ORM de Odoo, los decoradores de la API y la herencia de vistas XML para lograr modularidad.
- Sigue los estándares PEP 8 y las mejores prácticas de Odoo.
- Usa nombres descriptivos alineados con las convenciones de Odoo.

### Organización Estructural

- Separa las responsabilidades entre modelos, vistas, controladores, datos y seguridad.
- Crea archivos `__manifest__.py` bien documentados.
- Organiza los módulos con estructuras de directorios claras.

## Implementación en Python y ORM

- Define modelos que hereden de `models.Model`.
- Aplica los decoradores de la API adecuadamente:
  - `@api.model` para métodos a nivel de modelo.
  - `@api.multi` para métodos de conjuntos de registros (recordsets).
  - `@api.depends` para campos calculados (computed fields).
  - `@api.onchange` para cambios en campos de la interfaz de usuario.
- Crea vistas de interfaz de usuario basadas en XML (formularios, listas, kanban, calendario, gráficos).
- Usa la herencia XML a través de `<xpath>` y `<field>` para realizar modificaciones.
- Implementa controladores con `@http.route` para endpoints HTTP.

## Gestión de Errores y Validación

- Utiliza las excepciones integradas (`ValidationError`, `UserError`).
- Aplica restricciones mediante `@api.constrains`.
- Implementa una lógica de validación robusta.
- Usa bloques try-except de forma estratégica.
- Aprovecha el sistema de registro (logging) de Odoo (`_logger`).
- Escribe pruebas utilizando el framework de pruebas de Odoo.

## Seguridad y Control de Acceso

- Define ACLs y reglas de registro (record rules) en XML.
- Gestiona los permisos de usuario a través de grupos de seguridad.
- Prioriza la seguridad en todas las capas arquitectónicas.
- Implementa los derechos de acceso adecuados en los archivos `ir.model.access.csv`.

## Internacionalización y Automatización

- Marca las cadenas traducibles con `_()`.
- Aprovecha las acciones automatizadas y las acciones de servidor.
- Usa trabajos cron para tareas programadas.
- Usa QWeb para plantillas HTML dinámicas.

## Optimización del Rendimiento

- Optimiza las consultas del ORM con filtros de dominio y contexto.
- Almacena en caché datos estáticos o que se actualizan raramente.
- Delega tareas intensivas a acciones programadas.
- Simplifica las estructuras XML a través de la herencia.
- Usa `prefetch_fields` y métodos de cálculo de forma eficiente.

## Convenciones Guía

1. Aplica "Convención sobre Configuración" (Convention Over Configuration).
2. Refuerza la seguridad en todas las capas.
3. Mantén una arquitectura modular.
4. Documenta de forma exhaustiva.
5. Extiende mediante herencia, nunca modifiques el código base (core).

## Mejores Prácticas para la Estructura de Módulos

```
nombre_del_modulo/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   └── nombre_del_modelo.py
├── views/
│   └── vistas_del_modelo.xml
├── security/
│   ├── ir.model.access.csv
│   └── reglas_de_seguridad.xml
├── data/
│   └── datos.xml
├── controllers/
│   ├── __init__.py
│   └── main.py
├── static/
│   └── src/
├── wizards/
│   ├── __init__.py
│   └── nombre_del_wizard.py
└── reports/
    └── plantillas_de_reporte.xml
```

## Ejemplo de Definición de Modelo

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class CustomModel(models.Model):
    _name = 'custom.model'
    _description = 'Modelo Personalizado'

    name = fields.Char(string='Nombre', required=True)
    active = fields.Boolean(default=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
    ], default='draft')

    @api.depends('name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = record.name

    @api.constrains('name')
    def _check_name(self):
        for record in self:
            if len(record.name) < 3:
                raise ValidationError("El nombre debe tener al menos 3 caracteres")
```

## Ejemplo de Definición de Vista

```xml
<record id="custom_model_form" model="ir.ui.view">
    <field name="name">custom.model.form</field>
    <field name="model">custom.model</field>
    <field name="arch" type="xml">
        <form>
            <header>
                <field name="state" widget="statusbar"/>
            </header>
            <sheet>
                <group>
                    <field name="name"/>
                    <field name="active"/>
                </group>
            </sheet>
        </form>
    </field>
</record>

## Operaciones en el Proyecto Dipleg

### Activar un Módulo en Desarrollo
1. Reiniciar el servicio: `docker restart odoo_dev`
2. En Odoo UI: **Aplicaciones** → **Actualizar lista de aplicaciones**.
3. Buscar el módulo y hacer clic en **Activar**.

### Actualizar vía Terminal (Forzado)
```bash
docker exec -it odoo_dev odoo -u dipl_mi_modulo -d odoo_dev --stop-after-init
```

## Herencia de Terceros (Upstream/OCA)

Cuando se basa un módulo en uno existente (ej. de la OCA):
1. Copiar el módulo original a `repos/dev/dipl_[nuevo_nombre]/`.
2. **Refactorizar**: Renombrar todas las referencias técnicas (clases, modelos, carpetas, XML IDs) del nombre original al nuevo.
3. **Manifest**: Actualizar `name`, `author: 'Dipleg'`, y la `version`.
4. **Verificación**: Asegurar que instale limpiamente en una DB nueva antes de pushear.

```

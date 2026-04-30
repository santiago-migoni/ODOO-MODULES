# Enterprise Web Theme

Modulo de tema backend para Odoo 19 orientado a la shell de trabajo interna de Dipleg.

## Proposito

`dipl_web_theme` define capa visual y de navegacion del backend:
- home menu personalizado,
- navbar ajustada para flujo interno,
- esquema de color claro/oscuro,
- estilos de vistas y componentes web.

No agrega capacidades funcionales de Odoo Studio como parte del contrato base.

## Politica funcional

- El modulo base es estable para Community y Enterprise.
- El modulo base no debe depender de handlers opcionales no garantizados en `web`.
- El theme no expone en UI la accion "Add Custom Field".
- La gestion de campos custom se realiza fuera del theme, mediante modulo funcional dedicado o backend tecnico.

## Compatibilidad

- Dependencias base: `web`, `base_setup`.
- Compatible con entorno sin Studio.
- Mantiene compatibilidad con `base_automation`: la opcion "Automations" solo se muestra cuando la accion es realmente ejecutable.

## Validacion recomendada

1. Abrir backend en usuario interno y validar carga de shell (home menu + navbar).
2. Abrir listas/reportes y confirmar que el dropdown de columnas no produce errores JS.
3. Abrir/cerrar home menu y verificar que la URL se mantiene en `/odoo/` sin `action-*`.
4. Cambiar idioma a espanol y validar carga normal del webclient.

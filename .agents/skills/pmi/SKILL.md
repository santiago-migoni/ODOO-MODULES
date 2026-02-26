# Agile/Adaptive Project Management Skill

## Goal

Aplicar metodologías adaptativas (Ágil, Scrum, Kanban) para la gestión de proyectos, priorizando la entrega temprana de valor, la respuesta al cambio y el trabajo iterativo.

## Triggers

Activa esta skill **CUANDO** el usuario solicite:

- Crear o priorizar un Product Backlog (pila del producto).
- Planificar un Sprint o iteración de trabajo.
- Redactar Historias de Usuario o Criterios de Aceptación.
- Realizar retrospectivas o revisiones de entregables.
- Gestionar flujos de trabajo en tableros visuales (To Do, Doing, Done).

## Instructions

Tu proceso mental debe abandonar las fases estrictas y lineales. Estructura tus respuestas basándote en ciclos iterativos:

1. **Visión y Backlog**: Ayuda a definir la visión del producto. Captura las necesidades como Historias de Usuario estimadas por esfuerzo (ej. Story Points) y priorizadas por valor de negocio.
2. **Planificación de la Iteración (Sprint Planning)**: Selecciona los elementos prioritarios del backlog que caben en el próximo ciclo de trabajo. Divide las historias en tareas técnicas más pequeñas.
3. **Ejecución y Sincronización**: Fomenta la revisión diaria (Daily) para identificar bloqueos. Promueve la entrega continua y la integración de incrementos funcionales.
4. **Revisión y Retrospectiva**: Al final del ciclo, evalúa el incremento del producto generado y pregunta qué se puede mejorar en el proceso para el siguiente ciclo.

## Examples

**User**: Necesito planificar el desarrollo para la nueva integración contable.
**Agent**:
**1. Refinamiento del Product Backlog**

- **Historia de Usuario (Prioridad Alta):** Como responsable financiero, quiero importar automáticamente los extractos bancarios para agilizar la conciliación.
- **Criterios de Aceptación:** El sistema debe leer el formato CSV del banco, emparejar montos exactos y marcar las líneas conciliadas.
**2. Sprint Planning (Tareas Técnicas)**

- *Tarea A:* Desarrollar el parser del CSV en la rama `feat/nueva_funcion`.
- *Tarea B:* Configurar el mapeo de cuentas en el módulo de contabilidad.
- *Tarea C:* Resolver conflictos de integración, hacer el merge hacia la rama `develop` y documentar los cambios en el archivo changelog.

¿Te parece bien esta división de tareas para nuestro próximo Sprint, o hay algún otro requerimiento técnico que debamos agregar al backlog antes de empezar?

## Constraints

- **NO** exijas requerimientos detallados para todo el proyecto por adelantado; enfócate solo en lo que se va a construir en la próxima iteración.
- **NO** crees diagramas de Gantt estrictos; utiliza listas priorizadas, flujos Kanban o burn-down charts.
- Fomenta siempre la flexibilidad: si el usuario pide un cambio a mitad del desarrollo, acéptalo y proponle intercambiarlo por otra tarea de igual esfuerzo en el backlog actual.

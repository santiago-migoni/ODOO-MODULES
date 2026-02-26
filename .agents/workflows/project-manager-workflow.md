---
description: Flujos de trabajo para operaciones comunes de desarrollo de Odoo
---

# Agile/Adaptive - Workflow

## Estado Actual: [VISION | BACKLOG_REFINEMENT | SPRINT_PLANNING | IN_PROGRESS | REVIEW_RETRO]

### 1. VISION (Ideación)

- **Entrada:** Nueva necesidad del producto o proyecto.
- **Acción:** Definir el objetivo final a nivel macro y el valor esperado.
- **Salida:** Visión compartida. Pasar a `BACKLOG_REFINEMENT`.

### 2. BACKLOG_REFINEMENT (Creación y Refinamiento de la Pila)

- **Entrada:** Visión del producto o ideas sueltas.
- **Acción:** 1. Desglosar las ideas en Historias de Usuario.
  2. Estimar el esfuerzo relativo.
  3. Ordenar la lista de mayor a menor prioridad.
- **Salida:** Product Backlog priorizado. Pasar a `SPRINT_PLANNING`.

### 3. SPRINT_PLANNING (Planificación de Iteración)

- **Entrada:** Backlog priorizado y capacidad del equipo.
- **Acción:**
  1. Seleccionar las historias de usuario para el próximo ciclo corto (1-4 semanas).
  2. Dividir esas historias en tareas técnicas ejecutables.
- **Salida:** Sprint Backlog comprometido. Pasar a `IN_PROGRESS`.

### 4. IN_PROGRESS (Ejecución)

- **Entrada:** Sprint Backlog en marcha.
- **Acción:**
  1. Gestionar el flujo de tareas (To Do -> Doing -> Review -> Done).
  2. Detectar cuellos de botella diarios.
- **Salida:** Todas las tareas del Sprint alcanzan la definición de "Terminado" (Done). Pasar a `REVIEW_RETRO`.

### 5. REVIEW_RETRO (Revisión y Retrospectiva)

- **Entrada:** Incremento de producto completado.
- **Acción:**
  1. **Review:** Validar el trabajo funcional con el usuario.
  2. **Retro:** Preguntar: *"¿Qué funcionó bien? ¿Qué falló? ¿Qué mejoramos en el próximo ciclo?"*
- **Salida:** Lecciones integradas. Volver a `BACKLOG_REFINEMENT` para el siguiente ciclo.

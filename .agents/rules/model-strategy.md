---
trigger: always_on
glob:
description:
---

# Regla de Selección de Modelos

Esta regla define qué motor de IA debe utilizar Antigravity según la complejidad de la tarea en este proyecto. El agente debe autoevaluar la tarea antes de proceder y proponer el cambio de modelo si es necesario.

## Criterios de Selección

### 1. Nivel de Complejidad: BAJA

* **Modelo**: `Gemini 3.0 Flash`
* **Tareas**:
  * Corrección de errores ortográficos o de sintaxis menores.
  * Generación de comentarios de código.
  * Tareas de boilerplate (creación de placeholders, carpetas).
  * Consultas rápidas sobre el contenido de un archivo.

### 2. Nivel de Complejidad: MEDIA (Predeterminado)

* **Modelo**: `Gemini 3.1 Pro`
* **Tareas**:
  * Implementación de nueva lógica de negocio basada en patrones existentes.
  * Búsqueda de archivos y navegación por la arquitectura del proyecto.
  * Escritura de tests unitarios y de integración.
  * Análisis de requerimientos y creación de planes de implementación.

### 3. Nivel de Complejidad: ALTA

* **Modelo**: `Claude Sonnet 4.6 Thinking`
* **Tareas**:
  * Depuración de errores lógicos profundos o intermitentes (Heisenbugs).
  * Refactorizaciones críticas que afectan a múltiples módulos.
  * Optimización de algoritmos complejos o consultas SQL pesadas.
  * Tareas que requieran un estilo de codificación extremadamente preciso.

---

## Instrucción para el Agente

sAl recibir una tarea, evalúa su nivel (1, 2 o 3). Si la tarea actual requiere un nivel superior al modelo activo, informa al usuario:
*"Esta tarea parece de Nivel [X], recomiendo cambiar a [Modelo] para mayor precisión. ¿Procedo?"*

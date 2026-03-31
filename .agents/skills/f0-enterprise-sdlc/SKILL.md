---
name: Odoo Enterprise SDLC
description: Foundational reference for the iterative Software Development Life Cycle applied to Odoo Enterprise modules
phase: f0
trigger: Module planning, project kickoff, GAP analysis, sprint structuring, Go-Live preparation
---

# Odoo Enterprise SDLC — Foundational Skill

> **Fase**: 0 — Infraestructura y Marco Fundacional
> **Dónde estamos**: Antes de escribir una sola línea de código. Definiendo el marco metodológico que gobernará todo el desarrollo.
> **Por qué esta fase**: Sin un marco iterativo claro, los equipos caen en desarrollo ad-hoc, scope creep, y entregas que no alinean con las necesidades del negocio. Esta fase establece los cimientos para que todas las fases posteriores (1-7) operen con coherencia.

---

## Principio: Desarrollo Iterativo

El desarrollo de módulos Odoo Enterprise no es escritura lineal de código — es una orquestación arquitectónica que entrelaza planificación comercial, análisis de brechas funcionales, ingeniería de backend (ORM), construcción de interfaces reactivas (OWL) y automatización de pruebas.

El modelo iterativo asume que las necesidades organizacionales evolucionarán a medida que directivos, analistas funcionales y usuarios finales interactúen con versiones preliminares del sistema. En lugar de predecir todos los requisitos desde el inicio, el proceso se estructura en fases cíclicas: ideación → construcción → validación → despliegue → retroalimentación.

**Beneficios del enfoque iterativo**:
- Mitiga riesgos de implementaciones masivas.
- Acelera el ROI mediante entregas continuas de valor operativo.
- Permite adaptación ágil a cambios de requerimientos.
- Facilita la detección temprana de errores arquitectónicos.

---

## Tabla de Fases del SDLC

| Fase | Tareas Principales | Duración (Alta Complejidad) | Entregables |
|---|---|---|---|
| F1: Planificación y Descubrimiento | Entrevistas a stakeholders, GAP Analysis, evaluación de riesgos, plan de proyecto. | 3-6 semanas | Documento de requerimientos, mapeo de procesos, cronograma iterativo, matriz de recursos. |
| F2: Diseño Arquitectónico | Esquemas de DB, estructura de directorios, mapeo de flujos, prototipos de interfaces. | 6-16 semanas | Arquitectura de directorios, prototipos de vistas, diseño de relaciones ORM. |
| F3: Desarrollo Iterativo | Sprints de codificación, integración de módulos estándar, lógica de negocio, componentes OWL. | Ciclos de 1-2 semanas | Entregables funcionales revisables por sprint, configuraciones estabilizadas. |
| F4: Migración de Datos | Limpieza de datos heredados, normalización, scripts de migración, transferencias estructuradas. | 3-6 semanas | BD poblada con registros históricos limpios, integridad referencial validada. |
| F5: Pruebas / QA | Pruebas unitarias, de integración, UAT, simulación de escenarios reales. | 3-4 semanas | Informes de QA, bugs resueltos, estabilidad validada. |
| F6: Despliegue y Go-Live | Paso a producción, capacitación de usuarios, soporte post-implementación. | 2-4 semanas + soporte continuo | Módulo operativo, usuarios capacitados, monitoreo activo. |

**Regla del 10/80/10**: La fase de análisis y diseño ocupa ~10% del presupuesto total. El 80% se destina a ciclos iterativos de desarrollo/configuración/validación. El 10% restante a soporte y estabilización.

---

## GAP Analysis — Metodología

El GAP Analysis es el núcleo de la planificación. Compara las necesidades operativas de la organización con las funcionalidades nativas de Odoo para identificar brechas funcionales que justifiquen desarrollo custom.

### Proceso

1. **Documentar procesos actuales**: El equipo de consultoría funcional, liderado por el Project Leader, colabora con líderes departamentales para mapear flujos de trabajo existentes.
2. **Comparar con Odoo estándar**: Identificar qué cubre Odoo de fábrica y dónde resulta insuficiente.
3. **Cuantificar brechas**: Clasificar por impacto (crítico/alto/medio/bajo) y esfuerzo estimado.
4. **Generar backlog**: Descomponer macro-funcionalidades en tareas técnicas granulares para sprints de 1-2 semanas.
5. **Priorizar por dependencias**: Respetar dependencias lógicas (ej: inventario avanzado necesita extensiones de maestro de productos primero).

### Entregables del GAP Analysis

- Mapeo detallado necesidades comerciales ↔ características del producto.
- Estimación presupuestaria clara.
- Estrategia de gestión del cambio.
- Prueba de concepto (POC) demostrando flujos clave en BD estándar.

### Valor

El GAP Analysis trasciende la viabilidad técnica — actúa como instrumento de gestión de expectativas y control presupuestario. Previene el scope creep al someter requerimientos cambiantes a escrutinio formal.

---

## Equipos Multifuncionales

| Rol | Responsabilidad |
|---|---|
| Project Leader / PM | Lidera GAP Analysis, gestiona expectativas, aprueba entregables. |
| Business Analyst (BA) | Documenta procesos, traduce necesidades de negocio a requerimientos técnicos. |
| Desarrolladores | Implementan modelos, vistas, lógica de negocio, componentes OWL. |
| QA Specialist | Ejecuta pruebas, valida calidad, reporta regresiones. |
| SPoC (Single Point of Contact) | Representante del cliente, valida entregables contra expectativas. |

---

## Estructuración de Iteraciones

Las iteraciones se planifican evaluando dependencias técnicas y operativas:

- **Sprint 0**: Setup de infraestructura (clone, scaffold, configuración de Odoo.sh).
- **Sprints 1-N**: Desarrollo iterativo con entregables revisables al final de cada sprint.
- **Sprint de estabilización**: QA intensivo, UAT, resolución de bugs antes de Go-Live.
- **Sprint de deploy**: Migración a producción, capacitación, soporte.

Cada sprint produce componentes de software completamente operativos y revisables. No se acumulan features incompletas.

---

## Gestión del Cambio y Go-Live

El Go-Live es el umbral donde las simulaciones de Staging se someten al examen de la operatividad real. Más allá del código, el éxito depende del factor humano:

- **Capacitación**: Usuarios finales deben poder operar el sistema sin soporte constante.
- **Soporte post-Go-Live**: Monitoreo activo las primeras semanas (30 min, 24h, 1 semana).
- **Fricción iterativa esperada**: Hallazgos de UI/UX, comportamientos no previstos en integraciones, nuevos ángulos de análisis gerencial.

Todos estos descubrimientos **retroalimentan el backlog** — cerrando el ciclo y abriendo la siguiente iteración.

---

## Cierre Cíclico

El desarrollo iterativo en Odoo descarta un final rígido. Cada cierre de ciclo:

1. Retroalimenta la mesa de análisis técnico.
2. Genera material para expandir o reordenar el backlog.
3. Prepara el código ante actualizaciones mayores del fabricante (migraciones anuales).
4. Refina la estimación de velocidad del equipo para futuros sprints.

---

## Conexión con Fases Posteriores

| Esta skill habilita | Cómo |
|---|---|
| **F1 — Planificación** | Proporciona la metodología de GAP Analysis y estructuración de backlog que el `f1-scrum-master` consume para crear sprints. |
| **F2 — Análisis** | Define el marco de evaluación de brechas que el `f2-odoo-analysis` profundiza a nivel de código. |
| **F3-F7** | Establece el ciclo iterativo que todas las fases posteriores siguen: construir → validar → desplegar → retroalimentar. |

---

## Referencia Completa

Documento fuente: `docs/odoo-enterprise-sdlc.md`

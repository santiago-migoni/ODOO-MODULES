# Ciclo de Módulos Custom y Etapas de Odoo.sh

## Objetivo
Definir cómo se relacionan las etapas de creación de un módulo custom en Odoo 19 con los entornos de Odoo.sh: `desarrollo`, `prueba` y `producción`.

## Relación de etapas

| Etapa funcional | Entorno Odoo.sh sugerido | Resultado esperado |
|---|---|---|
| 1. Descubrimiento y diagnóstico | Desarrollo (o pre-desarrollo) | Problema y proceso actual relevados |
| 2. Definición funcional | Desarrollo | Alcance y criterios de aceptación definidos |
| 3. Diseño técnico | Desarrollo | Diseño de modelos, vistas, seguridad e integraciones |
| 4. Planificación | Desarrollo | Backlog, riesgos, dependencias e hitos |
| 5. Scaffolding del módulo | Desarrollo | Estructura base del módulo creada |
| 6. Implementación | Desarrollo | Funcionalidad desarrollada de forma incremental |
| 7. Validación y QA técnica | Prueba | Tests, validaciones y regresión superados |
| 8. UAT con usuarios | Prueba | Validación funcional de negocio y ajustes finales |
| 9. Despliegue | Producción | Versión estable publicada |
| 10. Mantenimiento evolutivo / hotfix | Desarrollo -> Prueba -> Producción | Mejora o corrección aplicada con ciclo completo |

## Guía operativa por entorno

### Desarrollo
- Analizar requerimientos y documentar alcance.
- Diseñar y construir el módulo (`models`, `views`, `security`, `data`).
- Mantener traducciones en `i18n/es.po`.
- Incorporar dependencias en `requirements.txt` y `__manifest__.py`.
- Ejecutar validaciones técnicas tempranas.

### Prueba
- Ejecutar pruebas funcionales y técnicas con datos representativos.
- Validar permisos, reglas de acceso y comportamiento en escenarios críticos.
- Realizar UAT con usuarios clave.
- Cerrar incidencias antes de promover a producción.

### Producción
- Desplegar solo versión aprobada en `prueba`.
- Verificar checklist post-deploy (instalación, actualización, permisos, flujos clave).
- Monitorear incidentes y registrar mejoras para el siguiente ciclo.

## Flujo recomendado de branches en Odoo.sh
1. Implementar en branch de `desarrollo`.
2. Promover a `prueba` para QA + UAT.
3. Promover a `producción` cuando estén cerrados los criterios de aceptación.
4. Para hotfixes, repetir el ciclo completo: `desarrollo -> prueba -> producción`.

## Criterio de cierre por etapa
- Desarrollo: alcance implementado, sin bloqueos técnicos críticos.
- Prueba: QA/UAT aprobados, sin defectos de severidad alta abiertos.
- Producción: despliegue exitoso, operación estable y sin regresiones críticas.

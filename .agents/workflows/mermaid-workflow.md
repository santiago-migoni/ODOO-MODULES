---
description: Flujo de diseño para exportación e interoperabilidad visual de Mermaid
---

# Workflows de Diagramación Mermaid

Proceso para crear, mantener y exportar arte conceptual en texto mediante Mermaid, asegurando su compatibilidad e integración con el resto de la base de conocimiento Odoo/DevOps.

## 1. Flujo de Diagramación (Elaboración y Mantenimiento)

Para documentar una nueva arquitectura o flujo, sigue esta secuencia iterativa:

1. **Definir el caso de uso**: Establecer las entidades participantes o componentes de la función nueva. ¿Es conceptual, DB, flujo temporal?
2. **Definir Esqueleto (Start Simple)**: Volcar sólo lo mínimo vital en texto y validar en el pre-visualizador de markdown nativo (VSCode/GitLab).
3. **Iterar y Añadir Relaciones**: Agregar conexiones (Asociación, Composición, Pasos Secuenciales).
4. **Agregar Notas de Contexto y Comentarios `%%`**: Hacer que el diagrama sea legible de extremo a extremo.

## 2. Renderizado y Exportación a Formato Físico (PNG/SVG)

Generalmente, mantener el formato base puro bastará para su autovisualización en Markdown (como GitHub o editores). Pero si es necesario ser incrustado por exportación a un reporte estático, PDFs, o presentarse en documentos legacy:

**Local a través de Node CLI (Si está preinstalado)**:

```bash
# Convierte diagrama MMD a formato de imagen PNG
mmdc -i ruta/del/diagrama_fuente.mmd -o diagram_export.png
```

**Workflow a través de Docker (Ambientes donde no debe estar ensuciado con NodeJS global)**:

```bash
# Ejecutar un contenedor de un-solo-uso (ephemeral) apuntado a carpeta de trabajo
docker run --rm -v $(pwd):/data minlag/mermaid-cli -i /data/input.mmd -o /data/diagram_export.png
```

## 3. Patrón Odoo-Mermaid (Sugerido)

A la hora de crear diagramación sobre módulos de odoo:

* Se recomienda hacer los **Flowcharts** para representar los flujos preconstruidos por Odoo (Workflow Engine de estados como "draft", "done", "cancel").
* Emplear **ERD Diagrams** o **Class Diagrams** para denotar las relaciones lógicas `Many2one` y `One2many` añadidas nuevas en `models/`.

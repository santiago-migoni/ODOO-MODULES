---
trigger: always_on 
glob: "*.md, *.mmd"
description: Prácticas de diseño y documentación arquitectónica con diagramas Mermaid
---

# Reglas para Diagramas Mermaid

Basado en la skill `mermaid-diagrams`. Para aplicar la diagramación robusta y como código en el proyecto.

## 1. Arquitectura y Sintaxis Base

- Todo diagrama debe iniciar declarando correctamente su tipo (ej. `classDiagram`, `sequenceDiagram`, `flowchart TD`).
- Evitar usar palabras reservadas sin escapar. Emplear identación y saltos de línea para preservar su legibilidad (Markdown puro visual o formato nativo `.mmd`).
- Comentar reglas de negocio complejas dentro del código Mermaid usando el token `%%`.

## 2. Tipificación Conceptual Correcta

Se debe utilizar el diagrama idóneo para el caso de uso sin forzar otros formatos:

- **Class Diagrams**: Diseño de Modelado OOP y Relaciones de Entidades del Dominio (Odoo Models).
- **Sequence Diagrams**: Para interacciones basadas en tiempo, flujos de API, métodos acoplados secuencialmente y autenticación.
- **Flowcharts**: Árboles de decisión, procesos de negocio lógicos, ciclos de vida.
- **ERD (Entity-Relationship Diagrams)**: Exclusivo para diseño y representación de bases de datos/esquemas puros, documentando relaciones de multiplicidad y llaves foráneas.
- **C4 Architecture Diagrams**: Diagramas de contexto, contenedor, componente.

## 3. Prácticas de Simplicidad

- **Un diagrama por concepto**: No realizar diagramas monolíticos gigantes inentendibles; dividir vistas complejas en múltiples subdiagramas.
- **Nombres significativos**: Las etiquetas en los nodos y mensajes de secuencia deben resultar obvias respecto a qué hace el sistema.
- **Siempre agregar Contexto**: Un diagrama nunca debe estar huérfano; requiere de un título y una descripción de texto o notas que expliquen la intención del modelo para quien lo visualice en el futuro.

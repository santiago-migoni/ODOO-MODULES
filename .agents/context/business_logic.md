# Conocimiento de Negocio (.agent/knowledge/business.md)

> Lógica de negocio, clientes clave y reglas comerciales de la empresa. Este archivo es la fuente de verdad para decisiones de implementación que dependen del contexto del negocio.

---

## Modelo Operativo y de Producción

* **Naturaleza:** 100% Make-To-Order (MTO) / Fabricación bajo demanda. No existe catálogo de productos estandarizados.
* **Servicios Core:** Corte láser de fibra óptica 2D, plegado CNC, corte con guillotina y rolado de chapas (con capacidad hasta 4 metros de longitud). Especialización en aceros inoxidables.
* **Modalidades de Trabajo:**
  1. **Provisión Completa:** La empresa aporta la materia prima (chapa) y factura el producto terminado y procesado.
  2. **Servicio a Fasón (Mano de Obra):** El cliente provee el material (usualmente manipulado y descargado con puente grúa). Solo se presupuesta y cobra el servicio de transformación geométrica de la chapa.

---

## Clientes Clave

| Segmento / Industria | Particularidades | Canal de Comunicación Preferido |
|---|---|---|
| **Vitivinicultura y Agricultura** | Fuerte demanda local (Mendoza). Requieren trabajos precisos en acero inoxidable para tanques, maquinarias e instalaciones. | Mail Corporativo / WhatsApp |
| **Industria Manufacturera y Construcción** | Exigen estricto cumplimiento de especificaciones técnicas en planos y tiempos de entrega acordados. | Mail Corporativo / WhatsApp |
| **Otras Metalúrgicas (B2B)** | Tercerización de servicios de alta precisión (corte láser, plegado CNC) que no pueden absorber internamente. | WhatsApp |
| **Particulares (B2C)** | Trabajos de menor escala, productos a medida. Ingresan principalmente por consultas directas y recomendaciones (boca en boca). | WhatsApp |

---

## Listas y Lógica de Precios

No existen listas de precios estáticas debido a la naturaleza MTO del negocio. El cálculo de cotizaciones es dinámico y depende estrictamente del proceso productivo involucrado:

* **Procesos Convencionales (Plegado, Guillotina, Rolado):** El precio base se calcula en función de los **kilos** de material a procesar.
* **Proceso de Corte Láser:** El precio final se compone sumando el valor de los **kilos** de material más los **minutos de operación** requeridos por la máquina láser de fibra óptica.

---

## Lógica de Costos e Inventario

* **Material Propio:** Se costea la materia prima consumida sumada al costo del servicio.
* **Material de Terceros (Fasón):** No afecta la valoración contable del inventario propio. Se acopia físicamente separado en planta.
* **Gestión de Retazos (Scrap):** No hay una regla estricta universal. La devolución del material sobrante al cliente o su absorción como chatarra interna depende del acuerdo comercial previo establecido con cada cliente.

---

## Reglas de Negocio Críticas

* **Validación Financiera Previa:** Ninguna orden de producción puede iniciarse sin la validación de un cobro (pago total o adelanto/seña). Esto exige una conciliación ágil con las entidades bancarias (ej. importación de extractos del Banco Galicia).
* **Dependencia de Planos CAD:** Todo trabajo en planta requiere la elaboración de un plano productivo definitivo. Este procesamiento técnico se centraliza en estaciones de trabajo dedicadas (ej. la computadora del primo encargada de procesar archivos de AutoCAD). Estos planos deben estar accesibles y vinculados a la orden de trabajo.
* **Aprobaciones Jerárquicas (Estructura Familiar):** Las compras de abastecimiento, autorizaciones de gastos y decisiones comerciales críticas requieren la revisión y aprobación de la dirección (padre y tíos). Este flujo de autorización se canaliza de manera formal a través del correo electrónico corporativo.
* **Trazabilidad de Comunicación:** Toda la gestión comercial rápida, envío de cotizaciones a prospectos y notificaciones de entrega se centraliza vía WhatsApp, por lo que el estado de los pedidos debe ser fácilmente consultable para responder en tiempo real.

---

## Flujos Comerciales Principales

### 1. Ciclo de Venta y Producción (End-to-End)

1. **Captura y Asesoramiento:** El cliente ingresa su necesidad (WhatsApp/Mail). Se brinda asesoramiento técnico especializado.
2. **Definición y Cotización:** Se determina un plano preliminar, se calculan los costos (Kilos vs. Kilos + Minutos Láser) y se coordinan los tiempos de entrega.
3. **Cobranza:** El cliente realiza el pago (total o anticipo). Se concilia el ingreso.
4. **Ingeniería:** Se procesa y elabora el plano productivo definitivo en AutoCAD.
5. **Producción:** La orden pasa a los centros de trabajo en planta. Se ejecuta el corte (láser o guillotina) y posteriormente el conformado (plegado CNC o rolado).
6. **Cierre y Entrega:** Se inventaría el producto terminado, se separa la chapa/scrap si corresponde, y se notifica al cliente vía WhatsApp para que retire el trabajo en planta.

### 2. Ciclo de Compras y Abastecimiento

1. Detección de necesidad de reposición de chapa, gases para corte o insumos de taller.
2. Solicitud de presupuestos a proveedores.
3. Envío de la solicitud de compra a la dirección para su revisión.
4. Autorización vía correo electrónico por parte de los socios directores.
5. Emisión de la orden de compra y posterior recepción física del material.

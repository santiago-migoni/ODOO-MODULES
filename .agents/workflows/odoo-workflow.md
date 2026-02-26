---
description: Flujos de trabajo para operaciones comunes de desarrollo de Odoo
---

# Workflows de Odoo

Procedimientos estándar para el desarrollo y despliegue dentro del proyecto Odoo.

## 1. Activar un Módulo en Desarrollo

Para ver los cambios reflejados de un módulo nuevo en la interfaz por primera vez:

```bash
# 1. Reiniciar el servicio
$ docker restart odoo_dev

# 2. Actualizar lista de aplicaciones
# En Odoo UI (en modo desarrollador): Aplicaciones -> Actualizar lista de aplicaciones

# 3. Instalar
# Buscar el módulo por su nombre técnico y hacer clic en Activar.
```

## 2. Actualizar un Módulo vía Terminal (Forzado)

Cuando los cambios en vistas o código Python no se reflejen recargando la página, forzar la actualización del módulo para la base de datos de desarrollo:

```bash
docker exec -it odoo_dev odoo -u dipl_mi_modulo -d odoo_dev --stop-after-init
```

## 3. Integración y Herencia de Módulos de Terceros (Upstream/OCA)

Procedimiento para incorporar y customizar módulos de OCA u otros proveedores:

1. **Copiar**: Traer el módulo original a la carpeta de desarrollo local (ej: `repos/dev/dipl_[nuevo_nombre]/`).
2. **Refactorizar**: Renombrar sistemáticamente todas las clases técnicas, archivos, modelos y `ids` de vistas XML de acuerdo a la taxonomía del proyecto.
3. **Modificar el Manifest**:
   - Cambiar `name` y `version`.
   - Modificar el autor (p. ej. `author: 'Dipleg'`).
4. **Verificación**: Antes de publicar (commit/push), validar que el módulo se instale correctamente en una base de datos limpia sin arrojar errores.

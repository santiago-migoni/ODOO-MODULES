---
description: Clona el repositorio oficial de Odoo Community 19.0 en .src.
---
# Clone Odoo 19 Community

Este workflow automatiza la descarga del código fuente oficial de Odoo 19 para desarrollo.

## Steps
1. **Verificar directorio**: Comprobar si `.src/odoo-community` ya existe.
2. **Clonación**: Si no existe (o si el usuario lo permite), ejecutar:
// turbo
   `git clone --depth 1 -b 19.0 https://github.com/odoo/odoo.git .src/odoo-community`
3. **Configuración de Remotos**: Asegurar que el remote oficial esté configurado como `origin`.
4. **Finalización**: Confirmar que la rama activa es `19.0`.

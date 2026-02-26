---
description:
---

# Workflows de Docker

Acciones automatizadas y manuales comunes para la gestión integral del entorno Docker (específicamente documentado para el "Entorno Dipleg").

## Gestión del Entorno de Desarrollo (Compose)

### Iniciar y Detener Servicios

```bash
# Construir e iniciar servicios en el perfil de desarrollo en segundo plano (detached)
docker compose --profile dev up -d --build

# Detener los servicios del entorno dev
docker compose --profile dev down
```

### Inspección y Depuración Rápida

```bash
# Observar los logs del contenedor (ej: Odoo) con límite de lectura (tail)
docker compose logs -f --tail=50 odoo_dev

# Abrir sesión interactiva en bash para inspeccionar el filesystem del contenedor
docker exec -it odoo_dev /bin/bash
```

## Operaciones de Base de Datos y Mantenimiento

### Acceso Directo por PSQL

Si se necesita interactuar o correr consultas directamente a la BD de dev:

```bash
docker exec -it postgres_dev psql -U odoo -d odoo_dev
```

### Respaldos (Backups) Manuales

Dumping local en archivo plano usando utilidades preinstaladas en el contenedor de postgres:

```bash
docker exec postgres_dev pg_dump -U odoo odoo_dev > backup_$(date +%Y%m%d).sql
```

## Solución de Problemas (Troubleshooting Local)

- **Permisos de Archivos del Host**: Cuando Odoo u otro contenedor reporta errores al escribir en carpetas host montadas en un volumen, se pueden restaurar permisos:

  ```bash
  sudo chown -R 1000:1000 ./repos/dev
  ```

- **Conflicto de Puertos (ej: 8069)**: Ocurre si servicios de Odoo u otro backend ya corren sin Docker o en un contenedor huérfano:

  ```bash
  sudo lsof -i :8069
  ```

- **Módulos no encontrados en la Interfaz**: Tras reinicios, cambios en bind-mounts o código, si los módulos de desarrollo no se ven reflejados, ejecutar siempre "Actualizar lista de aplicaciones" (`Update App List`) en Odoo con modo desarrollador activo.

## Diagnósticos Frecuentes

1. **Construcciones extremadamente lentas**: Evaluar la inclusión de montajes temporales de caché para los gestores de paquetes.
2. **Imágenes muy pesadas**: Pasar etapa final a _distroless_ o _alpine_, eliminando instaladores o código fuente sobrante.
3. **Servicio se reinicia continuamente**: Revisar configuración de `healthcheck` y validar que los puertos internos sean correctos en el contexto del servicio de docker.

---
trigger: always_on
glob:
description:
---

# Reglas de Docker

Basado en las mejores prácticas de la industria y el skill `docker-expert`.

## 1. Optimización de Dockerfile y Compilaciones

- **Single Responsibility Layering**: Separar la instalación de dependencias de la copia del código fuente para maximizar la caché entre construcciones.
- **Multi-stage Builds Obligatorios**: Utilizar siempre compilaciones multietapa para minimizar el tamaño de la imagen de producción manteniendo la flexibilidad de construcción (`deps` -> `build` -> `runtime`).
- **Eficiencia del Contexto**: Usar un `.dockerignore` exhaustivo. Nunca copiar archivos de desarrollo en capas de producción.
- **Consolidación de capas**: Combinar comandos `RUN` estratégicamente para reducir el número de capas.
- **Selección de Imagen Base**: Preferir `alpine`, `distroless` o `scratch` para entornos de producción por su reducido tamaño y superficie de ataque.

## 2. Seguridad en Contenedores

- **Privilegios (No Root)**: Crear un grupo y usuario sin privilegios (ej. `appuser`, UID 1001) y ejecutar el contenedor bajo la directiva `USER`.
- **Gestión de Secretos**: No exponer secretos en variables de entorno (ENV). Utilizar el mecanismo de gestión de secretos de Docker o Docker Compose (`/run/secrets/`).
- **Superficie de Ataque**: Solo instalar los binarios o paquetes estrictamente necesarios para el runtime. Evitar herramientas de compilación o de sistema en la imagen final.
- **Sólo Lectura**: De ser posible, establecer el sistema de archivos raíz de solo lectura y limitar las capabilities.

## 3. Orquestación (Docker Compose)

- **Definición de Dependencias**: Al declarar dependencias usando `depends_on`, especificar estrictamente `condition: service_healthy` (evitar que servicios arranquen antes de que su dependencia esté lista).
- **Controles de Salud**: Implementar la directiva `HEALTHCHECK` precisando `interval`, `timeout`, `start_period` y `retries`.
- **Límites de Recursos**: En definiciones que vayan a despliegue o producción, definir los recursos de `deploy` (`limits` y `reservations` para CPU y memoria).
- **Aislamiento de Red**: Emplear redes personalizadas (ej. frontend, backend). Configurar las redes traseras con `internal: true` para restringir acceso exterior a bases de datos y caches.
- **Políticas de Reinicio**: Para resiliencia ante caídas temporales, utilizar políticas como `restart_policy: on-failure` con `delay` y `max_attempts`.

## 4. Desarrollo Local

- Configurar montajes de volúmenes (bind mounts) para carga en caliente (hot reloading).
- Exponer puertos de depuración solo en servicios delimitados y sobreescritos para la etapa de desarrollo.

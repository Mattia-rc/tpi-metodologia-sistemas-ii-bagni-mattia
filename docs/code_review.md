# Revisión técnica asistida

Revisor: ChatGPT, durante esta sesión. No se presenta como revisión independiente de un compañero o docente. La validación personal de Bagni Mattia sigue pendiente. Criterio: observaciones sobre evidencia concreta y una acción verificable, sin juicios sobre la persona.

| Control | Resultado | Evidencia / criterio de aceptación |
|---|---|---|
| Funcionalidades mínimas | Cumple | Tres entidades, cinco operaciones verificadas en API y siete pasos HTTP reales. |
| Validación antes de persistir | Cumple en casos probados | Datos incorrectos retornan 400 y no crean filas; actualización inválida no cambia el estado. |
| Errores y métodos HTTP | Cumple en casos probados | 400 de validación, 404 de solicitud ausente y 405 de método no permitido. |
| Protección CSRF | Cumple | POST sin token da 403; con cookie y token funciona. Middleware conservado. |
| Cohesión de vistas | Corregido | Las vistas delegan validación, operaciones y consultas. |
| Respuesta pública consistente | Corregido | solicitud_a_dict es el único mapeo de Solicitud. |
| Parámetros relacionados | Corregido | NuevaSolicitud reemplaza seis argumentos. |
| Consultas por relaciones | Corregido | Listado de 11 registros usa una consulta; prueba evita regresión. |
| Contrato estable | Cumple en muestra | Diez pasos con igualdad de status y JSON antes/después. No demuestra equivalencia para toda entrada posible. |
| Tipado y compilación Angular | Cumple | strict y strictTemplates, compilación de producción aprobada. |
| Mensajes y reintento | Corregido | Se reemplazó onclick con recarga global por evento Angular y cargarCatalogos; prueba del botón aprobada. |
| Datos, dependencias y secretos | Cumple para demo | Datos sintéticos, sin bases recibidas, entornos ni claves personales en el paquete. |
| Instalación desde cero | Pendiente de validación local | Se verificó con dependencias del ZIP recibido; no se ejecutó npm ci con descarga limpia. |
| Inspección visual en navegador | Pendiente | Pruebas de DOM en JSDOM y HTTP real, sin captura de un navegador gráfico. |
| Actualización de Django | Mejora futura | Se mantuvo 4.2.30 para reproducir la base; requiere actualizar antes de un uso público. |

## Observaciones y correcciones
- CR01: “El mapeo de solicitud aparece en tres respuestas. Centralizarlo evita que agregar un campo produzca contratos diferentes.” Se resolvió con solicitud_a_dict y comparación JSON.
- CR02: “El listado carga relaciones dentro del bucle. La captura mide 22 consultas para 11 registros. Usar select_related y fijar una prueba que limite las consultas.” Se resolvió con una consulta y prueba de regresión.
- CR03: “El reintento de conexión usa un manejador inline y recarga toda la página. Conviene un evento Angular que repita la carga de catálogos y pueda probarse.” Se reemplazó por `(click)=cargarCatalogos()` y se agregó una séptima prueba frontend.

## Aceptación técnica
Las operaciones acordadas, las 21 pruebas originales backend y las 6 originales frontend deben mantenerse; las pruebas finales añaden 2 controles de consultas y 1 de reintento. No debe cambiar el esquema ni el contrato observado. Las limitaciones de instalación limpia y revisión visual quedan abiertas y no se declaran resueltas.

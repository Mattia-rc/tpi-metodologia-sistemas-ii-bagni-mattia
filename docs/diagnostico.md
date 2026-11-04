# Diagnóstico de la versión funcional inicial

Origen: la entrega recibida era un esqueleto. Los siguientes hallazgos corresponden al prototipo funcional construido después de recibirlo, identificado por el tag `estado-inicial`. No son hallazgos atribuidos al trabajo previo del alumno.

La calidad externa inicial permite registrar, consultar, asignar responsables, cambiar estado y emitir reportes. La calidad interna presenta oportunidades de mejora. Se protege el contrato con pruebas antes del refactoring.

| ID | Ubicación en estado-inicial | Evidencia | Impacto y riesgo | Prioridad | Acción |
|---|---|---|---|---|---|
| D01 | backend/mi_app/views.py, solicitudes | Un handler resuelve alta, validaciones, filtros, consultas y mapeo. | Varias razones para cambiar; un ajuste en validación puede afectar consultas. | Alta | Extraer validación y mover operaciones a servicios. |
| D02 | backend/mi_app/views.py, solicitudes y actualizar_solicitud | Conversión de JSON y verificación de objeto repetidas. | Cambios inconsistentes en mensajes y formatos de error. | Media | Extract Method a leer_json. |
| D03 | backend/mi_app/views.py, tres respuestas de solicitud | El diccionario público se repite en alta, listado y actualización. | Agregar un campo exige tres cambios y puede romper el contrato. | Alta | Extraer solicitud_a_dict. |
| D04 | backend/mi_app/views.py, crear_solicitud | Seis argumentos posicionales, varios del mismo tipo. | Confusión entre título, descripción, tipo y prioridad. | Media | Introduce Parameter Object con NuevaSolicitud. |
| D05 | backend/mi_app/views.py, validaciones | Tipos, prioridades y estados se repiten como literales además de models.py. | Divergencias entre reglas de la API y modelo. | Media | Reutilizar elecciones declaradas en el modelo. |
| D06 | backend/mi_app/views.py, bucle de listado | Acceso a estudiante.nombre y responsable.nombre por cada fila. | N+1: el costo crece con el listado; 22 consultas para 11 solicitudes en la captura. | Alta | select_related en consultas. |
| D07 | backend/mi_app/views.py, reporte | Cuatro conteos independientes y estados escritos manualmente. | Costo evitable y omisiones al agregar estados. | Baja | Agrupar por estado y completar ceros desde las elecciones. |
| D08 | frontend/src/app/app.ts | El componente conoce URLs, HTTP, parámetros, formulario y avisos. | Acoplamiento entre transporte y pantalla; difícil sustitución en pruebas. | Alta | Mover HTTP a SolicitudesApi, inyectado. |
| D09 | frontend/src/app/app.ts | catalogos, reporte, lista y cambios usan any. | Errores de nombres y tipos se descubren al ejecutar. | Media | Interfaces y uniones de tipos para el contrato. |
| D10 | backend/mi_app/views.py, actualizar_solicitud | Cambios de estado y asignación se persisten desde la vista. | Las reglas quedan ligadas a HTTP y son difíciles de reutilizar. | Alta | Move Method/reubicación a servicios transaccionales. |

## Criterio de priorización
Alta: afecta varias rutas o crece con el volumen. Media: aumenta el riesgo de inconsistencias o errores de edición. Baja: mejora localizada con impacto limitado en esta demo. No se inventa una estimación económica de deuda ni se afirma cobertura total de defectos.

## Referencias exactas
Las líneas se registran en `diagnostico.json` y corresponden al tag, no al archivo final. Cada ubicación puede verificarse con `git show estado-inicial:RUTA`.

# Refactorings aplicados y trazabilidad

La comparación parte del prototipo funcional creado con asistencia, no del esqueleto recibido. Las pruebas de caracterización existían antes de modificar la estructura. No se agregaron funcionalidades de dominio durante el refactoring.

| ID | Técnica | Antes (estado-inicial) | Después | Motivo | Verificación |
|---|---|---|---|---|---|
| R01 | Extract Method | Parseo de JSON duplicado en views.py | presentacion.leer_json y errores_json | Unificar errores previstos y validación del cuerpo | JSON inválido, objeto no válido y mensajes del contrato |
| R02 | Move Method / reubicación de responsabilidad | Escrituras y reglas mezcladas con HTTP | servicios.registrar_solicitud y actualizar_solicitud | Mantener las vistas centradas en transporte | Alta, cambio de estado, asignación y atomicidad |
| R03 | Introduce Parameter Object | crear_solicitud recibe 6 argumentos | NuevaSolicitud, dataclass inmutable | Dar nombre al conjunto de datos relacionado | Alta con y sin responsable, valores por defecto |
| R04 | Extract Method | Diccionario público copiado 3 veces | solicitud_a_dict | Evitar divergencia entre alta, lista y cambio | Comparación JSON de 10 pasos, idéntica |
| R05 | Reubicación de acceso HTTP | App conoce URLs y HttpParams | SolicitudesApi inyectado | Separar pantalla y transporte; tipar el contrato | 6 pruebas de pantalla conservadas |
| R06 | Encapsular consulta y optimizar carga | Acceso tardío a relaciones por cada fila | consultas.listar_solicitudes con select_related | Eliminar N+1 sin cambiar el resultado | 22 a 1 consultas con 11 solicitudes |
| R07 | Consolidar consulta repetida | Cuatro count separados | Un GROUP BY para reporte | Reducir repetición y centralizar estados | Reporte vacío, conteos y prueba de una consulta |

## SOLID con alcance explícito
- SRP: aplicado separando vistas, validaciones, operaciones, consultas y presentación. En Angular el servicio HTTP deja de estar mezclado con el estado del formulario.
- OCP: mejora parcial al reutilizar elecciones del modelo; agregar tipos todavía puede requerir cambiar uniones TypeScript. No se afirma extensión sin modificaciones en todo el sistema.
- LSP: no se incorporaron jerarquías propias ni polimorfismo que justifique una demostración de sustitución. No se agregaron herencias artificiales.
- ISP: se conservaron contratos acotados por operación; no se construyó un sistema de interfaces generales ni se afirma una aplicación completa de ISP.
- DIP: aplicación parcial mediante inyección de SolicitudesApi y HttpClient en Angular, sustituibles en pruebas. El backend continúa dependiendo directamente del ORM; no implementa una inversión total con repositorios abstractos.

Clean Code: nombres del dominio, funciones enfocadas, un único mapeo público, DTOs inmutables, errores esperados explícitos y tipado estricto en el frontend. Los errores inesperados no se silencian con un catch general.

## Invariantes conservadas
Mismos endpoints y métodos, nombres de campos, estados, valores por defecto, códigos de respuesta y orden del listado. La asignación nula permite quitar un responsable. El reporte es global aunque el listado se filtre. Los cambios entre estados permitidos son libres en este prototipo; no se inventó una nueva regla durante el refactoring.

## Fragmentos verificables
Antes: `crear_solicitud(estudiante_id, titulo, descripcion, tipo, prioridad, responsable_id)`.
Después: `registrar_solicitud(datos: NuevaSolicitud)`.
Antes: `for s in registros: ... s.estudiante.nombre ... s.responsable.nombre` con carga diferida.
Después: `Solicitud.objects.select_related('estudiante', 'responsable')`.
Los diffs completos están en el historial del bundle; usar `git diff estado-inicial estadorefactorizado -- backend/mi_app frontend/src/app`.

# Guía para video propio (12 minutos aproximadamente)

No leer resultados como experiencia personal si no se comprende su explicación. Practicar ejecutando el proyecto localmente. Usar voz propia y presentación en cámara, según la consigna.

| Tiempo | Mostrar | Explicar |
|---|---|---|
| 0:00-0:40 | Rostro y nombre completo | “Soy Bagni Mattia. Presento el TPI individual de Metodología de Sistemas II.” Indicar apoyo de IA según el registro real. |
| 0:40-2:00 | Pantalla del sistema | Dominio, usuarios, tres entidades, alcance y almacenamiento en SQLite. |
| 2:00-3:10 | Alta, filtros y asignación | Registrar con datos ficticios, cambiar estado y mostrar el reporte global. |
| 3:10-4:40 | Tag estado-inicial | Distinguir calidad visible de calidad interna; explicar tres hallazgos concretos y su prioridad. |
| 4:40-7:10 | Diff de código | Extract Method, Move Method, Parameter Object y mapper único. Mostrar antes y después de cada uno. |
| 7:10-8:20 | SOLID y Clean Code | SRP y dependencia HTTP inyectada. Explicar por qué no se forzó una jerarquía para LSP. |
| 8:20-10:00 | Terminal y evidencias | Ejecutar pruebas, explicar los diez pasos iguales y las 22 frente a 1 consultas SQL. |
| 10:00-11:10 | Checklist y commits | Mostrar observaciones, corrección del reintento y tags de etapas. |
| 11:10-12:00 | Cierre | Límites del prototipo y reflexión personal real. Aclarar el alcance de la asistencia utilizada. |

## Preguntas para practicar
1. ¿Por qué un sistema que funciona puede tener deuda técnica?
2. ¿Qué comportamiento preservaste al refactorizar?
3. ¿Qué es N+1 y por qué select_related lo evita en este caso?
4. ¿Qué diferencia hay entre un DTO y un modelo persistente?
5. ¿Por qué SQLite es una base de datos aunque se guarde en un archivo local?
6. ¿Qué verifica CSRF y qué no resuelve respecto de autenticación?
7. ¿Qué parte de SOLID se aplicó y cuál no tenía una justificación concreta?
8. ¿Qué limitaciones tienen los tests del frontend con HTTP simulado?

## Antes de grabar
Cargar datos ficticios con `cargar_demo`, abrir las dos terminales, verificar puertos, ajustar zoom y tamaño de letra y tener preparados el diff y el checklist. No mostrar contraseñas ni datos reales. Al finalizar, obtener un enlace accesible y agregarlo al informe.

# Declaración y registro de asistencia de IA

Herramienta: ChatGPT. Sesión de trabajo con Bagni Mattia; paquete preparado el 4 de noviembre de 2026. No se registra un identificador de modelo porque no está confirmado.

Grado de intervención: sustancial. La asistencia abarcó interpretación de consigna, revisión del ZIP, desarrollo de la versión funcional sobre las plantillas aportadas, refactoring, diseño y ejecución de pruebas, revisión técnica, documentación y borrador de informe. No se limita a corrección de redacción ni a consultas aisladas sobre conceptos.

El alumno indicó que no tenía proyecto, que trabajaría individualmente con autorización y que podía usar Angular y Django. Luego aportó un ZIP con plantillas sin funcionalidad de dominio. No se atribuyen al alumno implementaciones o verificaciones realizadas por la herramienta. Queda pendiente su revisión, ejecución local, reflexión personal y defensa.

## Intercambios relevantes en orden
Este es un registro de los intercambios técnicos relevantes con citas del alumno y resúmenes identificados de las respuestas. No es una exportación íntegra de la conversación. Si la cátedra solicita el intercambio completo, adjuntar también la exportación original; no sustituirla por una conversación inventada.

1. Solicitud inicial (fragmento): “chat necesito que se me realice este TP integrador para la materia metodologias” y “decime que es lo necesario que necesitas que te pase.” Se adjuntaron la consigna PDF y una copia Markdown. Respuesta resumida: se explicó la necesidad de sistema base, diagnóstico, refactoring, pruebas, repositorio y video, y la declaración real del uso de IA exigida por la materia.
2. Alumno: “no tengo ningun proyecto, lo hago individual, y tengo la autorizacion. se podria arrancar de 0, con lenguaje en angular y python con django si queres. se necesita frontend y backend?” Respuesta resumida: se aclaró que la consigna admite un prototipo y no exige separación frontend/backend; se propuso gestión de solicitudes.
3. Alumno: “dale, necesitas que arme el back y el front y te pase el zip? y de ahi lo seguis?” Respuesta resumida: se acordó recibir una versión inicial sencilla y conservarla para comparación.
4. Alumno: “pero necesitamos guardar datos en una bdd? o podemos guardarlo de manera local en un file”. Respuesta resumida: se compararon JSON y SQLite, y se eligió la conveniencia de SQLite con Django.
5. Alumno: “dale ahora armo el front y el back.” Respuesta resumida: se precisaron las operaciones mínimas y los archivos a incluir.
6. Alumno: “ahi esta.” Se recibió un primer ZIP con una carpeta vacía. Se informó el resultado de la inspección y se pidió volver a comprimir los archivos.
7. Alumno: segundo ZIP adjunto, sin texto adicional. La revisión encontró plantillas de Django y Angular sin modelos ni operaciones de dominio. Se informó que se construiría el prototipo, diferenciando el origen de cada versión.

## Actividades de la herramienta durante el desarrollo
- Inspección del ZIP y registro de su hash SHA-256 en origen.json. Se excluyeron dependencias, caches, bases recibidas y claves generadas del paquete entregable.
- Construcción de una versión funcional con datos sintéticos. Se añadieron pruebas de caracterización antes del refactoring y se etiquetó estado-inicial.
- Diagnóstico con diez hallazgos, evidencia por archivo y línea, impacto y prioridad.
- Aplicación de siete mejoras de estructura, incluyendo las técnicas obligatorias. No se afirmó una aplicación completa de todos los principios SOLID.
- Ejecución real de pruebas y comparación de respuestas. Las salidas están en archivos TXT y JSON del anexo. La primera compilación de Angular falló por una restricción de lectura de memoria del entorno; se adaptó esa consulta de telemetría sin alterar la compilación ni el código de aplicación.
- Revisión asistida, corrección del reintento de conexión y pruebas adicionales. No hubo una revisión humana independiente.
- Elaboración de documentación y un informe provisional; no se inventaron un enlace GitHub, video, comisión, docente ni reflexión personal del alumno.

## Validación pendiente del alumno
Confirmar la exactitud de esta declaración, revisar el código, ejecutar el proyecto en su equipo y preparar una defensa propia. La herramienta no puede afirmar esa comprensión ni reemplazarla.

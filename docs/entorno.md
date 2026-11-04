# Entorno de verificación
Python 3.12.14, Node 24.22.1, npm 11.9.0. Django 4.2.30, asgiref 3.8.1, sqlparse 0.5.5; Angular 22.2, CLI 22.2.5 y Vitest 5.1.0 resueltos por el lockfile recibido.
Se reutilizaron las dependencias empaquetadas en el ZIP del alumno; no se afirmó una instalación limpia desde Internet.

El sandbox bloquea la consulta RSS de Node que Angular usa para telemetría de rendimiento. Para ejecutar build y pruebas se precargó compat_rss_entorno.cjs mediante NODE_OPTIONS. Solo sustituye esa estadística si la consulta devuelve ENOENT; no modifica Angular, los tests ni la aplicación. En una máquina habitual no debería requerirse.

No se dispuso de un navegador gráfico. Se verificaron compilación, DOM con JSDOM, API con Django TestCase e integración HTTP real por el proxy de Angular. No se adjuntan capturas simuladas.

Los servidores de prueba se iniciaron juntos en el mismo proceso de ejecución del entorno; los primeros intentos desde sesiones separadas no eran accesibles. La verificación integrada posterior pasó siete pasos. Ver integracion_http.json.

Para repetir la captura de contrato, desde backend/:
`python ../scripts/capturar_contrato.py ../docs/contrato_nuevo.json`
Para la integración real, iniciar ambos servidores y, desde la raíz del proyecto:
`python scripts/probar_integracion_http.py`
La prueba HTTP agrega una solicitud ficticia a la base local. Se usa exclusivamente para demo.

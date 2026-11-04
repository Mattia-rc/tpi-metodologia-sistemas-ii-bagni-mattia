"""Genera el borrador PDF y su fuente Markdown. Requiere reportlab (dependencia documental)."""
from pathlib import Path
import json
from html import escape
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Preformatted, KeepTogether
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
OUT = ROOT / 'informe'
OUT.mkdir(exist_ok=True)
datos = json.loads((DOCS/'datos_entrega.json').read_text())
verificacion = json.loads((DOCS/'verificacion.json').read_text())
diagnostico = json.loads((DOCS/'diagnostico.json').read_text())
estilos = getSampleStyleSheet()
estilos.add(ParagraphStyle(name='CuerpoTPI',fontName='Helvetica',fontSize=10,leading=14,spaceAfter=9,textColor=colors.HexColor('#253b4c')))
estilos.add(ParagraphStyle(name='PequenoTPI',parent=estilos['CuerpoTPI'],fontSize=8.4,leading=11,spaceAfter=6))
estilos.add(ParagraphStyle(name='CeldaTPI',parent=estilos['CuerpoTPI'],fontSize=8,leading=10.5,spaceAfter=0))
estilos.add(ParagraphStyle(name='TituloTPI',fontName='Helvetica-Bold',fontSize=21,leading=25,spaceAfter=15,textColor=colors.HexColor('#174b69')))
estilos.add(ParagraphStyle(name='SubTPI',fontName='Helvetica-Bold',fontSize=12,leading=16,spaceBefore=9,spaceAfter=8,textColor=colors.HexColor('#174b69')))
estilos.add(ParagraphStyle(name='CodigoTPI',fontName='Courier',fontSize=8,leading=10.5,backColor=colors.HexColor('#eff4f7'),borderPadding=9,spaceAfter=10))
story=[];md=[]

def texto(s,small=False):
    story.append(Paragraph(escape(s),estilos['PequenoTPI' if small else 'CuerpoTPI']))
    md.append(s+'\n')

def titulo(s):
    story.append(Paragraph(escape(s),estilos['TituloTPI']));md.append('# '+s+'\n')

def sub(s):
    story.append(Paragraph(escape(s),estilos['SubTPI']));md.append('## '+s+'\n')

def espacio(n=8):story.append(Spacer(1,n))

def tabla(encabezado,filas,anchos):
    data=[[Paragraph('<b>'+escape(str(x))+'</b>',estilos['CeldaTPI']) for x in encabezado]]
    data += [[Paragraph(escape(str(x)),estilos['CeldaTPI']) for x in fila] for fila in filas]
    t=Table(data,colWidths=anchos,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e4edf3')),
        ('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),8),
        ('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),
        ('BOTTOMPADDING',(0,0),(-1,-1),7),('LINEBELOW',(0,0),(-1,0),.8,colors.HexColor('#a5b9c8')),
        ('LINEBELOW',(0,1),(-1,-1),.4,colors.HexColor('#d7e0e7'))]))
    story.append(t);espacio()
    md.append('| '+' | '.join(encabezado)+' |\n| '+' | '.join(['---']*len(encabezado))+' |')
    md.extend('| '+' | '.join(str(x).replace('\n',' ') for x in fila)+' |' for fila in filas);md.append('')

def codigo(s):story.append(Preformatted(s,estilos['CodigoTPI']));md.append('```\n'+s+'\n```\n')
def pagina():story.append(PageBreak());md.append('\n---\n')
def valor(k):return datos.get(k) or 'Pendiente de completar'

# 1
texto('TECNICATURA UNIVERSITARIA EN PROGRAMACIÓN A DISTANCIA',True)
espacio(20)
titulo('Trabajo Práctico Integrador')
sub('Metodología de Sistemas II')
texto('Evolución de un sistema de solicitudes académicas: calidad interna, deuda técnica, refactoring y revisión técnica.')
espacio(12)
tabla(['Dato','Información'],[
    ['Alumno',datos['alumno']],['Modalidad','Individual, con autorización informada por el alumno'],
    ['Comisión',valor('comision')],['Docente',valor('docente')],['Fecha de entrega',valor('fecha_limite')],
    ['Estado del documento','Borrador para revisión y defensa del alumno']], [115,380])
sub('Resumen ejecutivo')
for s in [
 'Se construyó un prototipo local de solicitudes con Angular, Django y SQLite.',
 'La base recibida contenía plantillas, sin operaciones académicas implementadas.',
 'Sobre la primera versión funcional se diagnosticaron diez debilidades técnicas.',
 'Se separaron responsabilidades y se aplicaron siete mejoras de estructura.',
 'Las pruebas conservaron las respuestas y el listado pasó de 22 consultas a 1.',
 'El desarrollo contó con asistencia sustancial de IA, declarada en este informe.']:
    story.append(Paragraph(escape(s),estilos['PequenoTPI']));md.append(s+'  ')
espacio(10)
texto('Pendientes para la entrega: revisión personal, ejecución en el equipo del alumno, datos de portada, publicación del repositorio, video propio y reflexión individual. No se presentan esos puntos como realizados.',True)
pagina()

# 2
titulo('1. Sistema base y alcance')
texto('El caso es un sistema de gestión de solicitudes académicas. Permite registrar un pedido de un estudiante, indicar tipo y prioridad, asignar un responsable, cambiar el estado y consultar un reporte. El alcance se mantiene acotado para concentrar el análisis en la mantenibilidad.')
sub('Actores y entidades')
texto('El estudiante origina una solicitud. Un operador de secretaría la registra y actualiza su seguimiento. Un responsable representa el área que la atiende. En esta demo los roles describen el dominio; no se implementó autenticación ni permisos por usuario.')
tabla(['Entidad','Datos principales','Relación'],[
 ['Estudiante','Nombre y legajo ficticios','Un estudiante puede tener muchas solicitudes.'],
 ['Responsable','Nombre y área ficticios','Puede atender muchas solicitudes; la asignación es opcional.'],
 ['Solicitud','Título, descripción, tipo, prioridad y estado','Pertenece a un estudiante y puede tener un responsable.']], [88,184,223])
sub('Operaciones verificables')
tabla(['Operación','API y comportamiento'],[
 ['Registrar','POST /api/solicitudes/: valida y guarda; devuelve 201.'],
 ['Consultar y filtrar','GET /api/solicitudes/: título, estado y prioridad combinables.'],
 ['Cambiar estado','PATCH /api/solicitudes/<id>/: pendiente, en_proceso o resuelta.'],
 ['Asignar responsable','PATCH en la misma ruta; null permite quitar la asignación.'],
 ['Reportar','GET /api/reporte/: total y cantidad por estado, sin filtros.'],
 ['Catálogos','GET /api/catalogos/: datos ficticios y opciones; entrega cookie CSRF.']], [115,380])
sub('Tecnología y almacenamiento')
texto('Se utilizó Angular 22.2 en el frontend y Python con Django 4.2.30 en el backend, conservando las dependencias aportadas. SQLite guarda datos en db.sqlite3 dentro del equipo local. El archivo se genera con las migraciones y no se distribuye una base recibida con posibles datos personales.')
texto('La interfaz incluye formulario, listado, filtros, asignación y reporte. Las pruebas de componentes verifican el DOM en JSDOM. La integración se probó por HTTP real; no se dispone de una captura de navegador y no se adjuntan imágenes simuladas.',True)
pagina()

# 3
titulo('2. Calidad externa e interna')
tabla(['Perspectiva','Observación sobre la versión funcional inicial'],[
 ['Calidad externa','Permite completar las operaciones esperadas, informa errores y conserva los datos al consultar. Se verificó con pruebas, no solo con una descripción de funcionalidades.'],
 ['Calidad interna','Las vistas concentran decisiones, repiten el mapeo público y cargan relaciones por cada fila. El componente Angular mezcla transporte HTTP con el estado de la pantalla.'],
 ['Consecuencia','La corrección visible no garantiza bajo costo de cambio. Un nuevo campo podría exigir cambios en tres respuestas y un listado más grande aumenta el número de consultas.']], [105,390])
sub('Origen y versiones del caso')
tabla(['Estado','Contenido y autoría del proceso'],[
 ['Archivo recibido','Dos esqueletos Django y Angular con la pantalla generada. Sin entidades ni operaciones académicas. Se conserva el ZIP original sin modificar.'],
 ['estado-inicial','Primera versión funcional construida después de recibir las plantillas, con asistencia sustancial de ChatGPT. No se presenta como implementación previa del alumno.'],
 ['estadorefactorizado','Mismas operaciones, con responsabilidades separadas, contrato tipado y consultas optimizadas. El bundle conserva los cambios reales de esta sesión.']], [110,385])
sub('Criterio de análisis')
texto('El diagnóstico usa evidencia observable: una función que reúne varias responsabilidades, código duplicado, un conjunto de parámetros relacionado y consultas ejecutadas en el listado. No se asignaron costos monetarios ni métricas de cobertura que no se hayan medido.')
texto('La prioridad alta corresponde a cambios que afectan varias rutas o escalan con el volumen; la media, a inconsistencias y errores de edición; la baja, a una mejora localizada. Las ubicaciones del diagnóstico se refieren al tag estado-inicial. Los archivos finales tienen otras líneas.')
sub('Trazabilidad')
texto('docs/origen.json registra el nombre y SHA-256 del ZIP recibido. docs/diagnostico.json conserva el archivo, la línea y un fragmento de cada hallazgo. La comparación completa puede revisarse con git diff estado-inicial estadorefactorizado.',True)
pagina()

# 4
titulo('3. Deuda técnica y code smells')
texto('Los diez hallazgos siguientes pertenecen a la primera versión funcional. Las primeras cinco debilidades explican cambios propensos a inconsistencias. La tabla continúa en la página siguiente.')
hallazgos=[
 ('D01','Vista con varias responsabilidades','solicitudes combina alta, filtros, consultas y respuesta.','Un ajuste local obliga a revisar varias rutas del flujo.','Alta'),
 ('D02','Parseo de JSON duplicado','Las dos vistas de escritura repiten lectura y comprobación del cuerpo.','Puede divergir el manejo de entradas y mensajes de error.','Media'),
 ('D03','Mapeo público duplicado','El diccionario de Solicitud se copia en alta, listado y actualización.','Un campo nuevo puede aparecer solo en algunas respuestas.','Alta'),
 ('D04','Lista de parámetros extensa','crear_solicitud recibe seis argumentos posicionales.','Es fácil intercambiar argumentos de tipo string o perder contexto.','Media'),
 ('D05','Literales repetidos','Estados, tipos y prioridades se repiten además de sus elecciones en el modelo.','Una modificación puede dejar reglas incompatibles.','Media'),
 ('D06','N+1 en acceso a relaciones','El bucle accede a estudiante.nombre y responsable.nombre con carga diferida.','22 consultas para 11 solicitudes en el escenario medido.','Alta'),
 ('D07','Conteos repetidos','El reporte ejecuta total y tres count separados.','Costo evitable y estados escritos manualmente.','Baja'),
 ('D08','Acoplamiento de pantalla a HTTP','App conoce URLs, parámetros, formulario y avisos.','Modificar el transporte obliga a editar la pantalla.','Alta'),
 ('D09','Contrato sin tipos precisos','Catálogos, reporte y lista usan any.','Errores de estructura se detectan al ejecutar.','Media'),
 ('D10','Operaciones persistentes en la vista','La vista de actualización asigna campos y guarda.','Las decisiones quedan ligadas al transporte HTTP.','Alta'),
]
def mostrar_hallazgo(h):
    ident,nombre,evidencia,impacto,prioridad=h
    loc=next(x for x in diagnostico if x['id']==ident)
    sub(f'{ident}. {nombre} | Prioridad {prioridad.lower()}')
    texto(f"Ubicación: {loc['archivo']}:{loc['linea']} (estado-inicial).",True)
    texto('Evidencia: '+evidencia+' Impacto y riesgo: '+impacto)
for h in hallazgos[:5]:mostrar_hallazgo(h)
pagina()

# 5
titulo('3. Diagnóstico (continuación)')
for h in hallazgos[5:]:mostrar_hallazgo(h)
sub('Deuda y decisión de corrección')
texto('Se priorizó separar responsabilidades, centralizar el contrato y evitar N+1. Las demás mejoras se aplicaron en pasos verificables. No toda repetición justifica una abstracción: no se incorporaron repositorios genéricos, microservicios ni jerarquías sin una necesidad del caso.',True)
pagina()

# 6
titulo('4. SOLID y Clean Code')
texto('La aplicación de principios se justifica por problemas concretos. No se presenta una lista de siglas como si todas hubieran requerido cambios en este prototipo.')
tabla(['Principio','Aplicación y límite'],[
 ['SRP','Aplicado: vistas para HTTP; validación para entradas; servicios para operaciones; consultas para lectura; presentación para el JSON público. El frontend delega HTTP en SolicitudesApi.'],
 ['OCP','Mejora parcial: las elecciones del modelo centralizan opciones. Un nuevo tipo todavía puede requerir modificar uniones TypeScript. No se afirma extensión sin cambios en todo el sistema.'],
 ['LSP','No se añadieron jerarquías propias. No corresponde inventar una demostración de sustitución ni forzar herencia solo para mencionar el principio.'],
 ['ISP','Se mantienen contratos pequeños por operación. No se construyó una interfaz general ni se atribuye una aplicación formal completa a esta separación.'],
 ['DIP','Aplicación parcial en Angular: inyección del servicio y HttpClient, sustituible en pruebas. El backend conserva dependencia directa del ORM de Django; no implementa inversión total.']], [66,429])
sub('Responsabilidades finales')
tabla(['Archivo o módulo','Responsabilidad'],[
 ['views.py','Coordinar entrada y salida HTTP.'],['validacion.py + dtos.py','Validar el formato y representar datos relacionados.'],
 ['servicios.py','Registrar y actualizar solicitudes dentro de transacciones.'],['consultas.py','Consultar relaciones, filtrar y agregar conteos.'],
 ['presentacion.py','Leer JSON, mapear la solicitud y responder errores previstos.'],['solicitudes-api.ts','Encapsular rutas, parámetros y métodos del backend.'],
 ['app.ts + modelos.ts','Estado de la pantalla y tipos del contrato.']], [180,315])
sub('Clean Code')
texto('Se utilizan nombres del dominio, funciones enfocadas, DTOs inmutables, tipado estricto y un único mapeo de salida. Los errores esperados se distinguen de fallas inesperadas. No se agregó un catch general que oculte defectos. Se mantuvo el esquema de datos para reducir variables durante la comparación.')
pagina()

# 7
titulo('5. Refactoring seguro')
sub('R01. Extract Method: lectura del cuerpo')
texto('Antes se repetía json.loads y la comprobación del objeto. Después leer_json concentra esa lectura y errores_json transforma únicamente errores previstos en respuestas. Se conservan los mensajes y códigos de las entradas probadas.',True)
codigo('Antes: datos = json.loads(request.body)  # en dos vistas\nDespués: datos = leer_json(request)')
sub('R02. Move Method: operaciones de escritura')
texto('Las vistas dejan de actualizar directamente los campos. servicios.registrar_solicitud y servicios.actualizar_solicitud reúnen las operaciones y su transacción. La vista solo valida, delega y presenta el resultado.',True)
codigo('Antes, en la vista: s.estado = datos["estado"]; s.save()\nDespués: solicitud = servicios.actualizar_solicitud(pk, cambios)')
sub('R03. Introduce Parameter Object')
texto('NuevaSolicitud agrupa los seis datos relacionados. La dataclass es inmutable y sus nombres hacen explícito el significado de cada valor. Se reduce la posibilidad de intercambiar argumentos posicionales.',True)
codigo('Antes: crear_solicitud(eid, titulo, descripcion, tipo, prioridad, rid)\nDespués: registrar_solicitud(datos: NuevaSolicitud)')
sub('R04. Extract Method: respuesta pública')
texto('El diccionario repetido en tres lugares se reemplaza por solicitud_a_dict. Alta, consulta y actualización mantienen el mismo contrato sin copiar su definición.',True)
codigo('Antes: {"id": s.id, "titulo": s.titulo, ...}  # tres copias\nDespués: solicitud_a_dict(solicitud)')
sub('Protección del comportamiento')
texto('Las 21 pruebas iniciales del backend y las 6 iniciales del frontend se ejecutaron antes y después. También se capturaron diez pasos de API en una base temporal y se compararon status y JSON. Las capturas no incluyen fechas variables ni tokens.',True)
pagina()

# 8
titulo('5. Otras mejoras y verificación')
tabla(['Cambio','Antes y después','Evidencia'],[
 ['R05. Mover acceso HTTP','App conoce rutas y parámetros; después usa SolicitudesApi inyectado y tipos explícitos.','Las seis pruebas iniciales de pantalla siguen aprobadas.'],
 ['R06. Encapsular consulta','Carga diferida de relaciones por fila; después select_related.','Mismo JSON; 22 consultas pasan a 1 con 11 solicitudes.'],
 ['R07. Consolidar reporte','Cuatro conteos separados; después una agregación por estado.','Reportes vacío y no vacío coinciden; una prueba exige una consulta.']], [110,240,145])
sub('Resultados observados')
tabla(['Verificación','Inicial','Refactorizada'],[
 ['Pruebas backend','21 aprobadas','23 aprobadas: mismas 21 y 2 de consultas'],
 ['Pruebas frontend','6 aprobadas','7 aprobadas: mismas 6 y 1 de reintento'],
 ['Contrato de API','10 pasos capturados','10 status y JSON idénticos'],
 ['Listado de 11 solicitudes','22 consultas SQL','1 consulta SQL'],
 ['Compilación de producción','Aprobada','Aprobada'],
 ['Migraciones pendientes','Esquema inicial creado','Ninguna diferencia de esquema'],
 ['Integración HTTP real','No se usa como comparación visual','7 pasos aprobados por proxy Angular-Django']], [170,125,200])
texto('Las pruebas adicionales protegen mejoras concretas; no sustituyen las pruebas conservadas. La igualdad en diez pasos es evidencia de estabilidad de esa muestra, no una demostración de equivalencia para todas las entradas posibles.')
sub('Límites del entorno de pruebas')
texto('Se usaron dependencias empaquetadas en el ZIP recibido. No se realizó una descarga e instalación limpia con npm ci. Los componentes Angular se probaron en JSDOM con HTTP simulado. La conexión completa se verificó además por HTTP real, sin navegador gráfico.')
texto('El entorno bloqueó la consulta RSS de Node utilizada por la telemetría de Angular. Se utilizó una precarga local que sustituye esa estadística únicamente al fallar. El código de la aplicación y el compilador no fueron modificados para ese ajuste. El detalle está en docs/entorno.md.',True)
pagina()

# 9
titulo('6. Pruebas y evidencias')
tabla(['Caso','Resultado esperado y verificado'],[
 ['Alta válida','201; datos persistidos; pendiente y media por defecto.'],
 ['Alta con responsable','201; identificación y nombre del responsable en la respuesta.'],
 ['Datos inválidos','400; sin crear una solicitud. Incluye texto vacío, longitud, elecciones e identificadores incorrectos.'],
 ['JSON inválido','400; rechazo de texto mal formado y valores que no son objeto.'],
 ['Cambio de estado','200; el cambio se conserva al volver a leer desde la base.'],
 ['Asignar y quitar','200; null quita la asignación sin borrar la solicitud.'],
 ['Actualización inválida','400; estado anterior conservado.'],
 ['Filtros combinados','Solo devuelve filas que cumplen título, estado y prioridad.'],
 ['Solicitud inexistente','404 con error previsto.'],
 ['CSRF','403 sin token; escritura válida con cookie y cabecera.'],
 ['Reporte','Conteos correctos con y sin datos; es global.'],
 ['Interfaz y error de conexión','Muestra lista y reporte, conserva campos ante rechazo, informa errores y permite reintento.']], [130,365])
sub('Comandos principales')
codigo('cd backend\npython manage.py test mi_app -v 2\npython manage.py makemigrations --check --dry-run\n\n# Desde frontend/\nnpm run build\nnpm test -- --watch=false')
texto('Las salidas se guardan en backend_final.txt, frontend_final.txt, build_final.txt y migraciones_final.txt. Los casos detallados están en tests.py, test_rendimiento.py y app.spec.ts. contrato_inicial.json y contrato_refactorizado.json conservan la comparación. integracion_http.json registra los siete pasos reales.',True)
pagina()

# 10
titulo('7. Revisión técnica')
texto('Se aplicó un checklist con observaciones sobre el código y acciones verificables. La revisión fue asistida por ChatGPT; no se atribuye a un compañero ni a un docente. La revisión personal del alumno está pendiente.')
tabla(['Control','Resultado y evidencia'],[
 ['Responsabilidades','Corregido: vistas pequeñas que delegan operaciones y consultas.'],
 ['Contrato público','Corregido: mapeo único y diez respuestas comparadas.'],
 ['Consultas','Corregido: carga de relaciones anticipada y pruebas de límite.'],
 ['Entradas y errores','Verificado en casos probados: 400, 404, 405 y CSRF.'],
 ['Tipado y compilación','Verificado: TypeScript y plantillas con comprobación estricta.'],
 ['Reintento de conexión','Corregido: evento Angular y método cargarCatalogos, con prueba.'],
 ['Instalación limpia / revisión visual','Pendientes de validación local. No se declaran realizadas.']], [155,340])
sub('Feedback y correcciones')
texto('CR01. La respuesta de solicitud está repetida en tres puntos. Centralizarla evita contratos distintos al agregar un campo. Se resolvió con solicitud_a_dict y comparación de JSON.')
texto('CR02. El listado carga relaciones dentro del bucle y escala con la cantidad de filas. Se resolvió con select_related y una prueba que exige una consulta.')
texto('CR03. El botón de reintento usaba un manejador inline y recargaba toda la página. Se reemplazó por el evento Angular y un método de carga comprobable; una prueba adicional verifica el botón.')
sub('Criterio de aceptación')
texto('Mantener las operaciones acordadas y todas las pruebas iniciales, no modificar el esquema ni el contrato observado y conservar las mejoras de consultas. Los controles incorporados pasan; las limitaciones abiertas permanecen registradas en docs/code_review.md.')
pagina()

# 11
titulo('8. Conclusiones y cierre pendiente')
sub('Conclusión técnica')
texto('El caso muestra que una implementación puede resolver las operaciones visibles y aun así presentar deuda técnica. La separación de responsabilidades, el mapeo único y los objetos de parámetros permiten localizar mejor los cambios. Las pruebas aportan evidencia de que esa reorganización conserva las respuestas esperadas.')
texto('La mejora medible principal es la eliminación de N+1 en el escenario de listado: 22 consultas pasan a 1 para 11 solicitudes. Esa medición describe cantidad de consultas, no tiempo de respuesta ni rendimiento bajo carga, que no fueron medidos.')
sub('Dificultades y límites del proceso')
texto('La base recibida todavía no era funcional, por lo que fue necesario construir el prototipo antes del diagnóstico. Se conservan por separado el origen y la versión funcional inicial para no confundir esas etapas. La instalación limpia y la inspección visual quedan pendientes de ejecución local.')
texto('El sistema no incluye autenticación, control de permisos, paginación ni restricciones de transición entre estados. No se utiliza en producción. Django 4.2.30 es una dependencia heredada sin soporte; actualizar a una rama mantenida requiere una tarea y verificación separadas.')
sub('Reflexión individual a completar por Bagni Mattia')
texto('Este apartado requiere experiencia y comprensión propias. Antes de entregar, redactar brevemente: qué concepto resultó más difícil; qué cambio puede explicar y justificar con un ejemplo del código; y qué mejora priorizaría después de ejecutar el sistema. No se inventa una reflexión personal en su nombre.')
sub('Entregables y enlaces')
tabla(['Recurso','Estado'],[
 ['Repositorio GitHub',valor('repositorio_github')],['Video de defensa',valor('video')],
 ['ZIP de evidencias','Incluye versiones, bundle Git, pruebas, diagnóstico y registro de IA.'],
 ['Portada y revisión','Completar datos, validar el proyecto y agregar reflexión individual.']], [140,355])
texto('El video debe grabarse con voz propia y presentación en cámara. La guía de 12 minutos está en docs/guion_video.md. Los recursos deben estar accesibles al momento de la corrección.',True)
pagina()

# 12
titulo('9. IA, anexos y fuentes')
sub('Declaración de asistencia')
texto('Se utilizó ChatGPT con intervención sustancial para interpretar la consigna, continuar las plantillas aportadas, desarrollar el prototipo funcional, refactorizar, diseñar y ejecutar pruebas, revisar técnicamente y preparar este borrador. No se limita su participación a consultas de teoría o redacción.')
texto('El alumno debe revisar el material, ejecutar el sistema y defender las decisiones. No se afirma que esas actividades personales ya hayan ocurrido. docs/registro_ia.md contiene citas reales de intercambios técnicos, resúmenes identificados y acciones de la herramienta. No es una exportación completa; puede complementarse con el chat original si la cátedra lo requiere.')
sub('Historial y anexos')
tabla(['Recurso','Contenido'],[
 ['historial_tpi.bundle','Commits reales de esta sesión y tags; se puede clonar con Git.'],
 ['version_inicial/','Código exportado del tag estado-inicial.'],
 ['version_refactorizada/','Código final y documentación del proceso.'],
 ['docs/diagnostico.*','Diez hallazgos y ubicaciones de la versión inicial.'],
 ['docs/refactorings.md','Relación entre problemas, cambios y verificaciones.'],
 ['docs/code_review.md','Checklist, observaciones, correcciones y controles pendientes.'],
 ['docs/*.txt y *.json','Salidas de pruebas, contratos y resultados HTTP.'],
 ['informe/','PDF provisional y fuente Markdown editable.']], [170,325])
texto('Tags: estado-inicial, estadorefactorizado, etapa-diagnostico, etapa-refactoring, etapa-pruebas y etapa-docs. Los commits se identifican como trabajo asistido y no simulan contribuciones anteriores.',True)
sub('Fuentes')
for s in [
 'Consigna oficial aportada: TP MS2V2 (1).pdf, secciones 4 a 7 y 11. Material complementario aportado: Markdown pegado(7).md.',
 'Django, Writing and running tests: https://docs.djangoproject.com/en/4.2/topics/testing/overview/',
 'Angular, Setting up HttpClient: https://angular.dev/guide/http/setup',
 'Angular, Serving Angular apps for development: https://angular.dev/tools/cli/serve']:
    texto(s,True)

def pie(c,doc):
    c.saveState();w,h=A4
    c.setStrokeColor(colors.HexColor('#c4d2dc'));c.line(50,46,w-50,46)
    c.setFont('Helvetica',8);c.setFillColor(colors.HexColor('#526d80'))
    c.drawString(50,32,'Bagni Mattia | Metodología de Sistemas II | Borrador revisable')
    c.drawRightString(w-50,32,str(doc.page));c.restoreState()

destino=OUT/'TPI_Bagni_Mattia_borrador.pdf'
doc=SimpleDocTemplate(str(destino),pagesize=A4,rightMargin=50,leftMargin=50,topMargin=43,bottomMargin=65,
    title='TPI - Solicitudes académicas - Bagni Mattia',author='Bagni Mattia; elaboración asistida por ChatGPT',
    subject='Borrador académico con asistencia declarada y verificación documentada')
doc.build(story,onFirstPage=pie,onLaterPages=pie)
(OUT/'TPI_Bagni_Mattia_borrador.md').write_text('\n'.join(md),encoding='utf-8')
print(destino)

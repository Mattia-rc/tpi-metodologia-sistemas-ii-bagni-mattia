# Solicitudes académicas - TPI de Metodología de Sistemas II

Alumno: Bagni Mattia. Modalidad individual autorizada, según declaración del alumno.
Prototipo local: Angular + Django + SQLite. Datos ficticios.

## Origen
El ZIP recibido contenía plantillas de Angular y dos proyectos Django sin funcionalidad de dominio.
Este repositorio continúa esas plantillas; la versión funcional inicial y su refactoring se desarrollan
con asistencia sustancial de ChatGPT. No se atribuyen al alumno pruebas o tareas no confirmadas.

## Ejecución
Python 3.12, Node 24.22.1 y npm 11.9.0 son las versiones usadas en la verificación.
Se conserva Django 4.2.30 y Angular 22.2 del entorno aportado para reproducir el caso académico.

Backend, desde `backend/`:
```bash
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows PowerShell: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py cargar_demo
python manage.py runserver 127.0.0.1:8000
```

Frontend, en otra terminal desde `frontend/`:
```bash
npm ci
npm start
```
Abrir http://localhost:4200. El proxy de desarrollo envía `/api/**` a Django.
Primero se consultan los catálogos y se recibe la cookie CSRF. Angular envía `X-CSRFToken`.
Si cambian puertos u hosts, ajustar `proxy.conf.json` y `CSRF_TRUSTED_ORIGINS`.

## Operaciones y alcance
Registrar una solicitud; asignar o quitar responsable; cambiar estado; buscar por título,
estado y prioridad; consultar reporte global. Los catálogos se cargan con `cargar_demo`.
Entidades: Estudiante, Responsable y Solicitud. SQLite se crea localmente; no se entrega
una base de datos con datos personales. No se incluye autenticación, carga de archivos ni notificaciones.

## Pruebas
```bash
cd backend
python manage.py test mi_app -v 2
python manage.py makemigrations --check --dry-run
```
Desde `frontend/`: `npm run build` y `npm test -- --watch=false`.

## Entrega
Completar comisión, docente, enlace GitHub y enlace al video en `docs/datos_entrega.json`.
Grabar video propio de 10 a 15 minutos. Revisar el informe y el registro de asistencia antes de entregar.
No se simula una revisión por otra persona: las observaciones son revisión técnica asistida.

## Límites
Prototipo local, sin autenticación ni autorización por roles. No publicar datos reales.
Django 4.2 es una dependencia heredada sin soporte; una actualización a una rama mantenida,
con su propia verificación, queda fuera del refactoring de este caso. No desplegar esta demo en producción.

## Informe editable
El borrador PDF y Markdown están en `informe/`. Para regenerarlos tras completar los datos:
```bash
python -m pip install -r requirements-docs.txt
python scripts/generar_informe.py
```
La reflexión individual debe incorporarse con contenido propio antes de entregar. El documento se mantiene como borrador hasta completar los recursos pendientes.

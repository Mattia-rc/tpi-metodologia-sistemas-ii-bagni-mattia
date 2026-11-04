import json
from functools import wraps
from django.http import JsonResponse
from .errores import ErrorSolicitud


def leer_json(request):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ErrorSolicitud('El cuerpo debe ser JSON válido.') from error
    if not isinstance(datos, dict):
        raise ErrorSolicitud('Se esperaba un objeto JSON.')
    return datos


def errores_json(vista):
    @wraps(vista)
    def envolver(*args, **kwargs):
        try:
            return vista(*args, **kwargs)
        except ErrorSolicitud as error:
            return JsonResponse({'error': str(error)}, status=error.status)
    return envolver


def solicitud_a_dict(solicitud):
    return {
        'id': solicitud.id,
        'titulo': solicitud.titulo,
        'descripcion': solicitud.descripcion,
        'tipo': solicitud.tipo,
        'prioridad': solicitud.prioridad,
        'estado': solicitud.estado,
        'estudiante_id': solicitud.estudiante_id,
        'estudiante': solicitud.estudiante.nombre,
        'responsable_id': solicitud.responsable_id,
        'responsable': solicitud.responsable.nombre if solicitud.responsable else None,
    }

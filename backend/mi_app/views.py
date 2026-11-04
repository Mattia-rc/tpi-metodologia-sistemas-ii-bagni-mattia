from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from . import consultas, servicios
from .presentacion import leer_json, errores_json, solicitud_a_dict
from .validacion import validar_alta, validar_cambio, validar_filtros


@require_http_methods(['GET'])
def catalogos(request):
    get_token(request)
    return JsonResponse(consultas.consultar_catalogos())


@require_http_methods(['GET', 'POST'])
@errores_json
def solicitudes(request):
    if request.method == 'POST':
        nueva = validar_alta(leer_json(request))
        solicitud = servicios.registrar_solicitud(nueva)
        return JsonResponse(solicitud_a_dict(solicitud), status=201)
    filtros = validar_filtros(request.GET)
    registros = consultas.listar_solicitudes(filtros)
    return JsonResponse({'solicitudes': [solicitud_a_dict(s) for s in registros]})


@require_http_methods(['PATCH'])
@errores_json
def actualizar_solicitud(request, pk):
    cambios = validar_cambio(leer_json(request))
    solicitud = servicios.actualizar_solicitud(pk, cambios)
    return JsonResponse(solicitud_a_dict(solicitud))


@require_http_methods(['GET'])
def reporte(request):
    return JsonResponse(consultas.consultar_reporte())

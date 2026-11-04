import json
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.http import require_http_methods
from .models import Estudiante, Responsable, Solicitud


@require_http_methods(['GET'])
def catalogos(request):
    get_token(request)
    return JsonResponse({
        'estudiantes': list(Estudiante.objects.order_by('id').values('id', 'nombre', 'legajo')),
        'responsables': list(Responsable.objects.order_by('id').values('id', 'nombre', 'area')),
        'tipos': [x[0] for x in Solicitud.TIPOS],
        'prioridades': [x[0] for x in Solicitud.PRIORIDADES],
        'estados': [x[0] for x in Solicitud.ESTADOS],
    })


def crear_solicitud(estudiante_id, titulo, descripcion, tipo, prioridad, responsable_id):
    return Solicitud.objects.create(estudiante_id=estudiante_id, titulo=titulo,
        descripcion=descripcion, tipo=tipo, prioridad=prioridad, responsable_id=responsable_id)


@require_http_methods(['GET', 'POST'])
def solicitudes(request):
    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse({'error': 'El cuerpo debe ser JSON válido.'}, status=400)
        if not isinstance(datos, dict):
            return JsonResponse({'error': 'Se esperaba un objeto JSON.'}, status=400)
        if set(datos) - {'estudiante_id', 'titulo', 'descripcion', 'tipo', 'prioridad', 'responsable_id'}:
            return JsonResponse({'error': 'Hay campos no admitidos.'}, status=400)
        if not isinstance(datos.get('titulo'), str) or not 1 <= len(datos['titulo'].strip()) <= 120:
            return JsonResponse({'error': 'Título requerido, máximo 120 caracteres.'}, status=400)
        if not isinstance(datos.get('descripcion'), str) or not 1 <= len(datos['descripcion'].strip()) <= 2000:
            return JsonResponse({'error': 'Descripción requerida, máximo 2000 caracteres.'}, status=400)
        if datos.get('tipo') not in ['certificado', 'equivalencia', 'consulta']:
            return JsonResponse({'error': 'Tipo inválido.'}, status=400)
        if datos.get('prioridad', 'media') not in ['baja', 'media', 'alta']:
            return JsonResponse({'error': 'Prioridad inválida.'}, status=400)
        if type(datos.get('estudiante_id')) is not int or not Estudiante.objects.filter(pk=datos['estudiante_id']).exists():
            return JsonResponse({'error': 'Estudiante inexistente.'}, status=400)
        rid = datos.get('responsable_id')
        if rid is not None and (type(rid) is not int or not Responsable.objects.filter(pk=rid).exists()):
            return JsonResponse({'error': 'Responsable inexistente.'}, status=400)
        s = crear_solicitud(datos['estudiante_id'], datos['titulo'].strip(), datos['descripcion'].strip(),
                            datos['tipo'], datos.get('prioridad', 'media'), rid)
        return JsonResponse({'id': s.id, 'titulo': s.titulo, 'descripcion': s.descripcion,
            'tipo': s.tipo, 'prioridad': s.prioridad, 'estado': s.estado,
            'estudiante_id': s.estudiante_id, 'estudiante': s.estudiante.nombre,
            'responsable_id': s.responsable_id,
            'responsable': s.responsable.nombre if s.responsable else None}, status=201)
    estado = request.GET.get('estado', '')
    prioridad = request.GET.get('prioridad', '')
    texto = request.GET.get('q', '').strip()
    if estado and estado not in ['pendiente', 'en_proceso', 'resuelta']:
        return JsonResponse({'error': 'Estado inválido.'}, status=400)
    if prioridad and prioridad not in ['baja', 'media', 'alta']:
        return JsonResponse({'error': 'Prioridad inválida.'}, status=400)
    registros = Solicitud.objects.all()
    if estado:
        registros = registros.filter(estado=estado)
    if prioridad:
        registros = registros.filter(prioridad=prioridad)
    if texto:
        registros = registros.filter(titulo__icontains=texto)
    resultado = []
    for s in registros:
        resultado.append({'id': s.id, 'titulo': s.titulo, 'descripcion': s.descripcion,
            'tipo': s.tipo, 'prioridad': s.prioridad, 'estado': s.estado,
            'estudiante_id': s.estudiante_id, 'estudiante': s.estudiante.nombre,
            'responsable_id': s.responsable_id,
            'responsable': s.responsable.nombre if s.responsable else None})
    return JsonResponse({'solicitudes': resultado})


@require_http_methods(['PATCH'])
def actualizar_solicitud(request, pk):
    try:
        datos = json.loads(request.body)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({'error': 'El cuerpo debe ser JSON válido.'}, status=400)
    if not isinstance(datos, dict):
        return JsonResponse({'error': 'Se esperaba un objeto JSON.'}, status=400)
    if set(datos) - {'estado', 'responsable_id'}:
        return JsonResponse({'error': 'Hay campos no admitidos.'}, status=400)
    if not datos:
        return JsonResponse({'error': 'Indicá estado o responsable_id.'}, status=400)
    if 'estado' in datos and datos['estado'] not in ['pendiente', 'en_proceso', 'resuelta']:
        return JsonResponse({'error': 'Estado inválido.'}, status=400)
    rid = datos.get('responsable_id')
    if rid is not None and (type(rid) is not int or not Responsable.objects.filter(pk=rid).exists()):
        return JsonResponse({'error': 'Responsable inexistente.'}, status=400)
    s = Solicitud.objects.filter(pk=pk).first()
    if s is None:
        return JsonResponse({'error': 'Solicitud inexistente.'}, status=404)
    if 'estado' in datos:
        s.estado = datos['estado']
    if 'responsable_id' in datos:
        s.responsable_id = rid
    s.save()
    return JsonResponse({'id': s.id, 'titulo': s.titulo, 'descripcion': s.descripcion,
        'tipo': s.tipo, 'prioridad': s.prioridad, 'estado': s.estado,
        'estudiante_id': s.estudiante_id, 'estudiante': s.estudiante.nombre,
        'responsable_id': s.responsable_id,
        'responsable': s.responsable.nombre if s.responsable else None})


@require_http_methods(['GET'])
def reporte(request):
    return JsonResponse({'total': Solicitud.objects.count(), 'por_estado': {
        'pendiente': Solicitud.objects.filter(estado='pendiente').count(),
        'en_proceso': Solicitud.objects.filter(estado='en_proceso').count(),
        'resuelta': Solicitud.objects.filter(estado='resuelta').count(),
    }})

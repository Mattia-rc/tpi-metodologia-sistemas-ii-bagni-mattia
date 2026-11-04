from django.db.models import Count
from .dtos import FiltrosSolicitud
from .models import Estudiante, Responsable, Solicitud


def solicitudes_relacionadas():
    return Solicitud.objects.select_related('estudiante', 'responsable')


def listar_solicitudes(filtros: FiltrosSolicitud):
    registros = solicitudes_relacionadas()
    if filtros.estado:
        registros = registros.filter(estado=filtros.estado)
    if filtros.prioridad:
        registros = registros.filter(prioridad=filtros.prioridad)
    if filtros.texto:
        registros = registros.filter(titulo__icontains=filtros.texto)
    return registros


def consultar_reporte():
    conteos = dict(Solicitud.objects.order_by().values('estado').annotate(cantidad=Count('id'))
                   .values_list('estado', 'cantidad'))
    por_estado = {estado: conteos.get(estado, 0) for estado, _ in Solicitud.ESTADOS}
    return {'total': sum(conteos.values()), 'por_estado': por_estado}


def consultar_catalogos():
    return {
        'estudiantes': list(Estudiante.objects.order_by('id').values('id', 'nombre', 'legajo')),
        'responsables': list(Responsable.objects.order_by('id').values('id', 'nombre', 'area')),
        'tipos': [clave for clave, _ in Solicitud.TIPOS],
        'prioridades': [clave for clave, _ in Solicitud.PRIORIDADES],
        'estados': [clave for clave, _ in Solicitud.ESTADOS],
    }

from django.db import transaction
from .consultas import solicitudes_relacionadas
from .dtos import NuevaSolicitud, CambioSolicitud
from .errores import ErrorSolicitud
from .models import Estudiante, Responsable, Solicitud


def verificar_responsable(responsable_id):
    if responsable_id is not None and not Responsable.objects.filter(pk=responsable_id).exists():
        raise ErrorSolicitud('Responsable inexistente.')


@transaction.atomic
def registrar_solicitud(datos: NuevaSolicitud):
    if not Estudiante.objects.filter(pk=datos.estudiante_id).exists():
        raise ErrorSolicitud('Estudiante inexistente.')
    verificar_responsable(datos.responsable_id)
    solicitud = Solicitud.objects.create(estudiante_id=datos.estudiante_id, titulo=datos.titulo,
        descripcion=datos.descripcion, tipo=datos.tipo, prioridad=datos.prioridad,
        responsable_id=datos.responsable_id)
    return solicitudes_relacionadas().get(pk=solicitud.pk)


@transaction.atomic
def actualizar_solicitud(pk: int, cambios: CambioSolicitud):
    verificar_responsable(cambios.responsable_id)
    solicitud = solicitudes_relacionadas().filter(pk=pk).first()
    if solicitud is None:
        raise ErrorSolicitud('Solicitud inexistente.', status=404)
    if cambios.estado is not None:
        solicitud.estado = cambios.estado
    if cambios.cambia_responsable:
        solicitud.responsable_id = cambios.responsable_id
    solicitud.save(update_fields=['estado', 'responsable'])
    return solicitudes_relacionadas().get(pk=solicitud.pk)

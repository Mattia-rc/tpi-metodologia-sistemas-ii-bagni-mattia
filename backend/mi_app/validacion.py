from .dtos import NuevaSolicitud, CambioSolicitud, FiltrosSolicitud
from .errores import ErrorSolicitud
from .models import Solicitud


def validar_campos(datos, admitidos):
    if set(datos) - admitidos:
        raise ErrorSolicitud('Hay campos no admitidos.')


def validar_eleccion(valor, elecciones, mensaje):
    if valor not in [clave for clave, _ in elecciones]:
        raise ErrorSolicitud(mensaje)
    return valor


def validar_texto(valor, maximo, mensaje):
    if not isinstance(valor, str) or not 1 <= len(valor.strip()) <= maximo:
        raise ErrorSolicitud(mensaje)
    return valor.strip()


def validar_id(valor, mensaje, opcional=False):
    if opcional and valor is None:
        return None
    if type(valor) is not int:
        raise ErrorSolicitud(mensaje)
    return valor


def validar_alta(datos):
    validar_campos(datos, {'estudiante_id', 'titulo', 'descripcion', 'tipo', 'prioridad', 'responsable_id'})
    titulo = validar_texto(datos.get('titulo'), 120, 'Título requerido, máximo 120 caracteres.')
    descripcion = validar_texto(datos.get('descripcion'), 2000, 'Descripción requerida, máximo 2000 caracteres.')
    tipo = validar_eleccion(datos.get('tipo'), Solicitud.TIPOS, 'Tipo inválido.')
    prioridad = validar_eleccion(datos.get('prioridad', 'media'), Solicitud.PRIORIDADES, 'Prioridad inválida.')
    estudiante_id = validar_id(datos.get('estudiante_id'), 'Estudiante inexistente.')
    responsable_id = validar_id(datos.get('responsable_id'), 'Responsable inexistente.', opcional=True)
    return NuevaSolicitud(estudiante_id, titulo, descripcion, tipo, prioridad, responsable_id)


def validar_cambio(datos):
    validar_campos(datos, {'estado', 'responsable_id'})
    if not datos:
        raise ErrorSolicitud('Indicá estado o responsable_id.')
    estado = None
    if 'estado' in datos:
        estado = validar_eleccion(datos['estado'], Solicitud.ESTADOS, 'Estado inválido.')
    responsable_id = validar_id(datos.get('responsable_id'), 'Responsable inexistente.', opcional=True)
    return CambioSolicitud(estado, responsable_id, 'responsable_id' in datos)


def validar_filtros(parametros):
    estado = parametros.get('estado', '')
    prioridad = parametros.get('prioridad', '')
    if estado:
        validar_eleccion(estado, Solicitud.ESTADOS, 'Estado inválido.')
    if prioridad:
        validar_eleccion(prioridad, Solicitud.PRIORIDADES, 'Prioridad inválida.')
    return FiltrosSolicitud(estado, prioridad, parametros.get('q', '').strip())

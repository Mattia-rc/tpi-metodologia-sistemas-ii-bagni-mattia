from dataclasses import dataclass


@dataclass(frozen=True)
class NuevaSolicitud:
    estudiante_id: int
    titulo: str
    descripcion: str
    tipo: str
    prioridad: str = 'media'
    responsable_id: int | None = None


@dataclass(frozen=True)
class CambioSolicitud:
    estado: str | None = None
    responsable_id: int | None = None
    cambia_responsable: bool = False


@dataclass(frozen=True)
class FiltrosSolicitud:
    estado: str = ''
    prioridad: str = ''
    texto: str = ''

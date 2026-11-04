export type TipoSolicitud = 'certificado' | 'equivalencia' | 'consulta';
export type Prioridad = 'baja' | 'media' | 'alta';
export type Estado = 'pendiente' | 'en_proceso' | 'resuelta';

export interface Estudiante { id: number; nombre: string; legajo: string; }
export interface Responsable { id: number; nombre: string; area: string; }
export interface NuevaSolicitud {
  estudiante_id: number | null;
  titulo: string;
  descripcion: string;
  tipo: TipoSolicitud;
  prioridad: Prioridad;
  responsable_id: number | null;
}
export interface Solicitud extends NuevaSolicitud {
  id: number;
  estado: Estado;
  estudiante: string;
  responsable: string | null;
}
export interface Catalogos {
  estudiantes: Estudiante[];
  responsables: Responsable[];
  tipos: TipoSolicitud[];
  prioridades: Prioridad[];
  estados: Estado[];
}
export interface FiltrosSolicitud { q: string; estado: Estado | ''; prioridad: Prioridad | ''; }
export interface CambioSolicitud { estado?: Estado; responsable_id?: number | null; }
export interface Reporte { total: number; por_estado: Record<Estado, number>; }
export interface ListaSolicitudes { solicitudes: Solicitud[]; }

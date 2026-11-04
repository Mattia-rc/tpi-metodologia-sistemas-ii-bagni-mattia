import { Injectable, inject } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Catalogos, FiltrosSolicitud, NuevaSolicitud, CambioSolicitud, Solicitud, Reporte, ListaSolicitudes } from './modelos';

@Injectable({ providedIn: 'root' })
export class SolicitudesApi {
  private readonly http = inject(HttpClient);
  private readonly base = '/api';

  catalogos() { return this.http.get<Catalogos>(`${this.base}/catalogos/`); }
  reporte() { return this.http.get<Reporte>(`${this.base}/reporte/`); }

  listar(filtros: FiltrosSolicitud) {
    let params = new HttpParams();
    for (const [clave, valor] of Object.entries(filtros)) {
      if (valor) params = params.set(clave, valor);
    }
    return this.http.get<ListaSolicitudes>(`${this.base}/solicitudes/`, { params });
  }

  registrar(datos: NuevaSolicitud) {
    return this.http.post<Solicitud>(`${this.base}/solicitudes/`, datos);
  }

  actualizar(id: number, cambios: CambioSolicitud) {
    return this.http.patch<Solicitud>(`${this.base}/solicitudes/${id}/`, cambios);
  }
}

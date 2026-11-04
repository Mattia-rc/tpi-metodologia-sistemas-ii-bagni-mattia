import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpErrorResponse } from '@angular/common/http';
import { forkJoin } from 'rxjs';
import { SolicitudesApi } from './solicitudes-api';
import { Catalogos, Solicitud, Reporte, FiltrosSolicitud, NuevaSolicitud, CambioSolicitud } from './modelos';

@Component({selector: 'app-root', imports: [FormsModule], templateUrl: './app.html', styleUrl: './app.css'})
export class App {
  private readonly api = inject(SolicitudesApi);
  readonly catalogos = signal<Catalogos | null>(null);
  readonly solicitudes = signal<Solicitud[]>([]);
  readonly reporte = signal<Reporte>({total: 0, por_estado: {pendiente: 0, en_proceso: 0, resuelta: 0}});
  readonly cargando = signal(false);
  readonly guardando = signal(false);
  readonly error = signal('');
  readonly aviso = signal('');
  filtros: FiltrosSolicitud = {q: '', estado: '', prioridad: ''};
  formulario = this.vacio();

  constructor() {
    this.cargando.set(true);
    this.api.catalogos().subscribe({
      next: c => {this.catalogos.set(c); this.recargar();},
      error: e => {this.error.set(this.mensaje(e)); this.cargando.set(false);}
    });
  }

  vacio(): NuevaSolicitud {
    return {estudiante_id: null, titulo: '', descripcion: '', tipo: 'consulta', prioridad: 'media', responsable_id: null};
  }

  recargar() {
    this.cargando.set(true);
    forkJoin({lista: this.api.listar(this.filtros), reporte: this.api.reporte()}).subscribe({
      next: r => {this.solicitudes.set(r.lista.solicitudes); this.reporte.set(r.reporte);
        this.cargando.set(false); this.error.set('');},
      error: e => {this.error.set(this.mensaje(e)); this.cargando.set(false);}
    });
  }

  registrar() {
    this.guardando.set(true); this.error.set(''); this.aviso.set('');
    this.api.registrar(this.formulario).subscribe({
      next: () => {this.guardando.set(false); this.formulario = this.vacio();
        this.aviso.set('Solicitud registrada.'); this.recargar();},
      error: e => {this.error.set(this.mensaje(e)); this.guardando.set(false);}
    });
  }

  actualizar(id: number, cambios: CambioSolicitud) {
    this.guardando.set(true); this.error.set(''); this.aviso.set('');
    this.api.actualizar(id, cambios).subscribe({
      next: () => {this.guardando.set(false); this.aviso.set('Solicitud actualizada.'); this.recargar();},
      error: e => {this.error.set(this.mensaje(e)); this.guardando.set(false);}
    });
  }

  mensaje(e: HttpErrorResponse): string {
    return e.error?.error ?? 'No se pudo completar la operación. Verificá el backend.';
  }
}

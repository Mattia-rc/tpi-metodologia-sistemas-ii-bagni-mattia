import { Component, inject, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { HttpClient, HttpErrorResponse, HttpParams } from '@angular/common/http';
import { forkJoin } from 'rxjs';

@Component({selector: 'app-root', imports: [FormsModule], templateUrl: './app.html', styleUrl: './app.css'})
export class App {
  private http = inject(HttpClient);
  catalogos = signal<any>(null);
  solicitudes = signal<any[]>([]);
  reporte = signal<any>({total: 0, por_estado: {}});
  cargando = signal(false);
  guardando = signal(false);
  error = signal('');
  aviso = signal('');
  filtros = {q: '', estado: '', prioridad: ''};
  formulario = this.vacio();

  constructor() {
    this.cargando.set(true);
    this.http.get<any>('/api/catalogos/').subscribe({
      next: c => {this.catalogos.set(c); this.recargar();},
      error: e => {this.error.set(this.mensaje(e)); this.cargando.set(false);}
    });
  }

  vacio() {return {estudiante_id: null as number | null, titulo: '', descripcion: '',
    tipo: 'consulta', prioridad: 'media', responsable_id: null as number | null};}

  recargar() {
    this.cargando.set(true);
    let params = new HttpParams();
    for (const [clave, valor] of Object.entries(this.filtros)) {
      if (valor) params = params.set(clave, valor);
    }
    forkJoin({lista: this.http.get<any>('/api/solicitudes/', {params}),
      reporte: this.http.get<any>('/api/reporte/')}).subscribe({
      next: r => {this.solicitudes.set(r.lista.solicitudes); this.reporte.set(r.reporte);
        this.cargando.set(false); this.error.set('');},
      error: e => {this.error.set(this.mensaje(e)); this.cargando.set(false);}
    });
  }

  registrar() {
    this.guardando.set(true); this.error.set(''); this.aviso.set('');
    this.http.post('/api/solicitudes/', this.formulario).subscribe({
      next: () => {this.guardando.set(false); this.formulario = this.vacio();
        this.aviso.set('Solicitud registrada.'); this.recargar();},
      error: e => {this.error.set(this.mensaje(e)); this.guardando.set(false);}
    });
  }

  actualizar(id: number, cambios: any) {
    this.guardando.set(true); this.error.set(''); this.aviso.set('');
    this.http.patch('/api/solicitudes/' + id + '/', cambios).subscribe({
      next: () => {this.guardando.set(false); this.aviso.set('Solicitud actualizada.'); this.recargar();},
      error: e => {this.error.set(this.mensaje(e)); this.guardando.set(false);}
    });
  }

  mensaje(e: HttpErrorResponse) {return e.error?.error ?? 'No se pudo completar la operación. Verificá el backend.';}
}

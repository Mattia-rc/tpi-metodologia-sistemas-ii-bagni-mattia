import { TestBed } from '@angular/core/testing';
import { provideHttpClient } from '@angular/common/http';
import { provideHttpClientTesting, HttpTestingController } from '@angular/common/http/testing';
import { App } from './app';

const catalogos = {
  estudiantes: [{ id: 1, nombre: 'Estudiante Demo', legajo: 'DEMO-1' }],
  responsables: [{ id: 2, nombre: 'Responsable Demo', area: 'Secretaría' }],
  tipos: ['consulta', 'certificado', 'equivalencia'],
  prioridades: ['baja', 'media', 'alta'],
  estados: ['pendiente', 'en_proceso', 'resuelta'],
};
const solicitud = { id: 1, titulo: 'Certificado', descripcion: 'Texto ficticio', tipo: 'certificado',
  prioridad: 'media', estado: 'pendiente', estudiante_id: 1, estudiante: 'Estudiante Demo',
  responsable_id: null, responsable: null };
const reporte = { total: 1, por_estado: { pendiente: 1, en_proceso: 0, resuelta: 0 } };

describe('Flujos de solicitudes en pantalla', () => {
  let http: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({ imports: [App], providers: [provideHttpClient(), provideHttpClientTesting()] });
    http = TestBed.inject(HttpTestingController);
  });
  afterEach(() => http.verify());

  function cargar() {
    const fixture = TestBed.createComponent(App);
    http.expectOne('/api/catalogos/').flush(catalogos);
    http.expectOne('/api/solicitudes/').flush({ solicitudes: [solicitud] });
    http.expectOne('/api/reporte/').flush(reporte);
    fixture.detectChanges();
    return fixture;
  }

  it('muestra listado y reporte recibidos', () => {
    const f = cargar();
    expect(f.nativeElement.querySelector('h1').textContent).toContain('Solicitudes académicas');
    expect(f.nativeElement.querySelector('h3').textContent).toBe('Certificado');
    expect(f.nativeElement.querySelector('.resumen strong').textContent).toBe('1');
  });

  it('envía filtros y muestra una búsqueda sin resultados', () => {
    const f = cargar();
    f.componentInstance.filtros = { q: 'sin resultado', estado: 'resuelta', prioridad: 'alta' };
    f.componentInstance.recargar();
    const peticion = http.expectOne(r => r.url === '/api/solicitudes/' && r.params.get('q') === 'sin resultado');
    expect(peticion.request.params.get('estado')).toBe('resuelta');
    expect(peticion.request.params.get('prioridad')).toBe('alta');
    peticion.flush({ solicitudes: [] });
    http.expectOne('/api/reporte/').flush(reporte);
    f.detectChanges();
    expect(f.nativeElement.textContent).toContain('No hay solicitudes con estos filtros.');
  });

  it('registra desde el formulario, limpia los campos y actualiza el listado', async () => {
    const f = cargar();
    f.componentInstance.formulario = { estudiante_id: 1, titulo: 'Nueva consulta', descripcion: 'Texto',
      tipo: 'consulta', prioridad: 'media', responsable_id: null };
    f.detectChanges();
    await f.whenStable();
    f.nativeElement.querySelector('form').dispatchEvent(new Event('submit', { bubbles: true, cancelable: true }));
    const req = http.expectOne('/api/solicitudes/');
    expect(req.request.method).toBe('POST');
    expect(req.request.body.titulo).toBe('Nueva consulta');
    req.flush({ ...solicitud, id: 2 });
    http.expectOne('/api/solicitudes/').flush({ solicitudes: [solicitud] });
    http.expectOne('/api/reporte/').flush(reporte);
    f.detectChanges();
    expect(f.componentInstance.formulario.titulo).toBe('');
    expect(f.nativeElement.querySelector('[role="status"]').textContent).toContain('Solicitud registrada.');
  });

  it('conserva lo escrito si el servidor rechaza el alta', () => {
    const f = cargar();
    f.componentInstance.formulario.titulo = 'Mi consulta';
    f.componentInstance.registrar();
    http.expectOne('/api/solicitudes/').flush({ error: 'Título requerido.' }, { status: 400, statusText: 'Bad Request' });
    f.detectChanges();
    expect(f.componentInstance.formulario.titulo).toBe('Mi consulta');
    expect(f.nativeElement.querySelector('[role="alert"]').textContent).toContain('Título requerido.');
    expect(f.componentInstance.guardando()).toBe(false);
  });

  it('envía el cambio de estado y refresca el reporte', () => {
    const f = cargar();
    f.componentInstance.actualizar(1, { estado: 'resuelta' });
    const req = http.expectOne('/api/solicitudes/1/');
    expect(req.request.method).toBe('PATCH');
    expect(req.request.body).toEqual({ estado: 'resuelta' });
    req.flush({ ...solicitud, estado: 'resuelta' });
    http.expectOne('/api/solicitudes/').flush({ solicitudes: [{ ...solicitud, estado: 'resuelta' }] });
    http.expectOne('/api/reporte/').flush({ total: 1, por_estado: { pendiente: 0, en_proceso: 0, resuelta: 1 } });
    f.detectChanges();
    expect(f.componentInstance.reporte().por_estado.resuelta).toBe(1);
    expect(f.nativeElement.textContent).toContain('Solicitud actualizada.');
  });

  it('informa una falla de conexión sin dejar la pantalla cargando', () => {
    const f = TestBed.createComponent(App);
    http.expectOne('/api/catalogos/').error(new ProgressEvent('error'));
    f.detectChanges();
    expect(f.nativeElement.querySelector('[role="alert"]').textContent).toContain('Verificá el backend.');
    expect(f.componentInstance.cargando()).toBe(false);
  });
});

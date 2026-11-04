import json
from django.test import TestCase, Client
from django.core.management import call_command
from .models import Estudiante, Responsable, Solicitud


class ContratoApiTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.estudiante = Estudiante.objects.create(nombre='Prueba A', legajo='TEST-1')
        cls.responsable = Responsable.objects.create(nombre='Prueba R', area='Pruebas')

    def datos(self, **cambios):
        return dict(estudiante_id=self.estudiante.id, titulo='Certificado',
                    descripcion='Descripción ficticia', tipo='certificado', **cambios)

    def alta(self, datos=None):
        return self.client.post('/api/solicitudes/', data=json.dumps(self.datos() if datos is None else datos),
                                content_type='application/json')

    def solicitud(self, **cambios):
        return Solicitud.objects.create(**self.datos(**cambios))

    def patch(self, pk, datos):
        return self.client.patch(f'/api/solicitudes/{pk}/', data=json.dumps(datos),
                                 content_type='application/json')

    def test_catalogos_datos_y_cookie_csrf(self):
        r=self.client.get('/api/catalogos/')
        self.assertEqual(r.status_code, 200)
        self.assertEqual(r.json()['estudiantes'][0]['legajo'], 'TEST-1')
        self.assertIn('csrftoken', r.cookies)

    def test_registro_persiste_y_devuelve_contrato(self):
        r=self.alta(); self.assertEqual(r.status_code, 201)
        self.assertEqual(Solicitud.objects.count(), 1)
        self.assertEqual(r.json()['estado'], 'pendiente')
        self.assertEqual(r.json()['prioridad'], 'media')
        self.assertIsNone(r.json()['responsable'])
        self.assertEqual(r.json()['estudiante'], 'Prueba A')

    def test_registro_con_responsable(self):
        r=self.alta(self.datos(responsable_id=self.responsable.id))
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['responsable'], 'Prueba R')

    def test_recorta_espacios(self):
        datos=self.datos();datos.update(titulo='  Certificado  ', descripcion='  texto  ')
        self.assertEqual(self.alta(datos).json()['titulo'], 'Certificado')
        self.assertEqual(Solicitud.objects.get().descripcion, 'texto')

    def test_campos_invalidos_no_persisten(self):
        casos=[{'titulo':' '}, {'titulo':'x'*121}, {'titulo':42}, {'descripcion':''},
               {'descripcion':'x'*2001}, {'descripcion':False}, {'tipo':'otro'},
               {'prioridad':'urgente'}, {'estudiante_id':999}, {'estudiante_id':True},
               {'estudiante_id':'1'}, {'responsable_id':999}, {'responsable_id':False},
               {'estado':'resuelta'}, {'desconocido':'x'}]
        for cambios in casos:
            with self.subTest(cambios=cambios):
                datos=self.datos();datos.update(cambios)
                self.assertEqual(self.alta(datos).status_code, 400)
                self.assertFalse(Solicitud.objects.exists())

    def test_json_invalido(self):
        for body in ['{', 'null', '[]', '4', '"texto"']:
            with self.subTest(body=body):
                r=self.client.post('/api/solicitudes/',data=body, content_type='application/json')
                self.assertEqual(r.status_code, 400)

    def test_listado_orden_descendente(self):
        a=self.solicitud();b=self.solicitud()
        self.assertEqual([x['id'] for x in self.client.get('/api/solicitudes/').json()['solicitudes']], [b.id,a.id])

    def test_filtros_combinados(self):
        a=self.solicitud(prioridad='alta',estado='en_proceso')
        self.solicitud(prioridad='baja')
        r=self.client.get('/api/solicitudes/', {'q':'CERT', 'estado':'en_proceso', 'prioridad':'alta'})
        self.assertEqual([x['id'] for x in r.json()['solicitudes']], [a.id])

    def test_filtro_sin_coincidencia(self):
        self.solicitud()
        self.assertEqual(self.client.get('/api/solicitudes/',{'q':'ausente'}).json(), {'solicitudes':[]})

    def test_filtros_invalidos(self):
        for filtro in [{'estado':'otro'}, {'prioridad':'otra'}]:
            self.assertEqual(self.client.get('/api/solicitudes/',filtro).status_code, 400)

    def test_cambio_estado_persiste(self):
        s=self.solicitud();r=self.patch(s.id,{'estado':'resuelta'})
        self.assertEqual(r.status_code, 200)
        s.refresh_from_db();self.assertEqual(s.estado, 'resuelta')

    def test_asignar_y_quitar_responsable(self):
        s=self.solicitud()
        self.assertEqual(self.patch(s.id,{'responsable_id':self.responsable.id}).json()['responsable'], 'Prueba R')
        self.assertIsNone(self.patch(s.id,{'responsable_id':None}).json()['responsable_id'])
        s.refresh_from_db();self.assertIsNone(s.responsable_id)

    def test_actualizacion_invalida_es_atomica(self):
        s=self.solicitud()
        r=self.patch(s.id,{'estado':'resuelta','responsable_id':999})
        self.assertEqual(r.status_code, 400)
        s.refresh_from_db();self.assertEqual(s.estado, 'pendiente')

    def test_actualizacion_rechaza_campos_y_vacio(self):
        s=self.solicitud()
        for datos in [{}, {'estado':'otro'}, {'titulo':'nuevo'}, {'responsable_id':True}]:
            self.assertEqual(self.patch(s.id,datos).status_code,400)

    def test_patch_json_invalido(self):
        s=self.solicitud()
        for body in ['{','[]','null']:
            self.assertEqual(self.client.patch(f'/api/solicitudes/{s.id}/',body,
                             content_type='application/json').status_code,400)

    def test_solicitud_inexistente(self):
        self.assertEqual(self.patch(999,{'estado':'resuelta'}).status_code,404)

    def test_reporte_global(self):
        self.solicitud();self.solicitud(estado='resuelta')
        self.assertEqual(self.client.get('/api/reporte/').json(),
            {'total':2,'por_estado':{'pendiente':1,'en_proceso':0,'resuelta':1}})

    def test_reporte_vacio(self):
        self.assertEqual(self.client.get('/api/reporte/').json(),
            {'total':0,'por_estado':{'pendiente':0,'en_proceso':0,'resuelta':0}})

    def test_metodos_no_admitidos(self):
        self.assertEqual(self.client.delete('/api/solicitudes/').status_code,405)
        self.assertEqual(self.client.post('/api/reporte/').status_code,405)
        self.assertEqual(self.client.get('/api/solicitudes/1/').status_code,405)

    def test_csrf_se_exige_y_token_funciona(self):
        cliente=Client(enforce_csrf_checks=True)
        r=cliente.post('/api/solicitudes/',json.dumps(self.datos()),content_type='application/json')
        self.assertEqual(r.status_code,403)
        cliente.get('/api/catalogos/')
        token=cliente.cookies['csrftoken'].value
        r=cliente.post('/api/solicitudes/',json.dumps(self.datos()),content_type='application/json',HTTP_X_CSRFTOKEN=token)
        self.assertEqual(r.status_code,201)

    def test_carga_demo_repetible(self):
        call_command('cargar_demo',verbosity=0)
        conteos=(Estudiante.objects.count(),Responsable.objects.count(),Solicitud.objects.count())
        call_command('cargar_demo',verbosity=0)
        self.assertEqual(conteos,(Estudiante.objects.count(),Responsable.objects.count(),Solicitud.objects.count()))

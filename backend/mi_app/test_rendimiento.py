from django.test import TestCase
from .models import Estudiante, Responsable, Solicitud


class ConsultasAcotadasTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        estudiante = Estudiante.objects.create(nombre='Prueba volumen', legajo='VOL-1')
        responsable = Responsable.objects.create(nombre='Prueba área', area='Demo')
        for numero in range(11):
            Solicitud.objects.create(estudiante=estudiante, responsable=responsable,
                titulo=f'Solicitud {numero}', descripcion='Sintética', tipo='consulta')

    def test_listado_no_genera_consultas_por_cada_fila(self):
        with self.assertNumQueries(1):
            respuesta = self.client.get('/api/solicitudes/')
            self.assertEqual(len(respuesta.json()['solicitudes']), 11)

    def test_reporte_agrupado_usa_una_consulta(self):
        with self.assertNumQueries(1):
            respuesta = self.client.get('/api/reporte/')
            self.assertEqual(respuesta.json()['total'], 11)

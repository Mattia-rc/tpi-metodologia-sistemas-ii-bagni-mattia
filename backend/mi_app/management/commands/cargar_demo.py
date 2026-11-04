from django.core.management.base import BaseCommand
from django.db import transaction
from mi_app.models import Estudiante, Responsable, Solicitud


class Command(BaseCommand):
    help = 'Carga idempotente de datos ficticios para la demostración.'

    @transaction.atomic
    def handle(self, *args, **options):
        e1, _ = Estudiante.objects.get_or_create(legajo='DEMO-001', defaults={'nombre': 'Estudiante Demo A'})
        e2, _ = Estudiante.objects.get_or_create(legajo='DEMO-002', defaults={'nombre': 'Estudiante Demo B'})
        r, _ = Responsable.objects.get_or_create(nombre='Responsable Demo', area='Secretaría académica')
        Solicitud.objects.get_or_create(estudiante=e1, titulo='Certificado de alumno regular',
            defaults={'descripcion': 'Solicitud de demostración con datos ficticios.', 'tipo': 'certificado',
                      'prioridad': 'media', 'responsable': r})
        Solicitud.objects.get_or_create(estudiante=e2, titulo='Consulta sobre inscripción',
            defaults={'descripcion': 'Consulta ficticia para probar filtros.', 'tipo': 'consulta',
                      'prioridad': 'alta', 'estado': 'en_proceso'})
        self.stdout.write(self.style.SUCCESS('Datos ficticios disponibles.'))

from django.db import models


class Estudiante(models.Model):
    nombre = models.CharField(max_length=100)
    legajo = models.CharField(max_length=20, unique=True)


class Responsable(models.Model):
    nombre = models.CharField(max_length=100)
    area = models.CharField(max_length=100)


class Solicitud(models.Model):
    TIPOS = [('certificado', 'Certificado'), ('equivalencia', 'Equivalencia'), ('consulta', 'Consulta')]
    PRIORIDADES = [('baja', 'Baja'), ('media', 'Media'), ('alta', 'Alta')]
    ESTADOS = [('pendiente', 'Pendiente'), ('en_proceso', 'En proceso'), ('resuelta', 'Resuelta')]
    estudiante = models.ForeignKey(Estudiante, on_delete=models.PROTECT)
    responsable = models.ForeignKey(Responsable, on_delete=models.PROTECT, null=True, blank=True)
    titulo = models.CharField(max_length=120)
    descripcion = models.TextField(max_length=2000)
    tipo = models.CharField(max_length=20, choices=TIPOS)
    prioridad = models.CharField(max_length=10, choices=PRIORIDADES, default='media')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    creada_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

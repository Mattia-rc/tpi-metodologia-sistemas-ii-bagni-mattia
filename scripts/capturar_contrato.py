"""Ejecutar desde backend/: python ../scripts/capturar_contrato.py SALIDA.json.
Usa base temporal; no toca db.sqlite3. Compara respuestas observables, no detalles internos.
"""
import os, sys, tempfile, json
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
os.environ.setdefault('DJANGO_SETTINGS_MODULE','back_proyecto.settings')
from django.conf import settings
with tempfile.TemporaryDirectory() as temporal:
    settings.DATABASES['default']['NAME']=str(Path(temporal)/'contrato.sqlite3')
    import django
    django.setup()
    from django.core.management import call_command
    from django.test import Client
    from django.test.utils import CaptureQueriesContext
    from django.db import connection
    from mi_app.models import Estudiante, Responsable, Solicitud
    call_command('migrate',verbosity=0)
    e=Estudiante.objects.create(nombre='Estudiante Contrato',legajo='SINT-1')
    r=Responsable.objects.create(nombre='Responsable Contrato',area='Demo')
    c=Client(enforce_csrf_checks=True)
    catalogo=c.get('/api/catalogos/')
    token=c.cookies['csrftoken'].value
    salidas=[{'paso':'catalogos','status':catalogo.status_code,'json':catalogo.json()}]
    def paso(nombre,metodo,url,datos=None):
        kwargs={} if datos is None else {'data':json.dumps(datos),'content_type':'application/json','HTTP_X_CSRFTOKEN':token}
        resp=getattr(c,metodo)(url,**kwargs)
        salidas.append({'paso':nombre,'status':resp.status_code,'json':resp.json()})
    paso('listado_vacio','get','/api/solicitudes/')
    paso('alta','post','/api/solicitudes/',{'estudiante_id':e.id,'titulo':' Certificado ',
        'descripcion':'Texto ficticio','tipo':'certificado','prioridad':'alta'})
    paso('asignar','patch','/api/solicitudes/1/',{'responsable_id':r.id})
    paso('resolver','patch','/api/solicitudes/1/',{'estado':'resuelta'})
    paso('filtrar','get','/api/solicitudes/?estado=resuelta&q=CERT&prioridad=alta')
    paso('reporte','get','/api/reporte/')
    paso('quitar_responsable','patch','/api/solicitudes/1/',{'responsable_id':None})
    paso('error_validacion','post','/api/solicitudes/',{'titulo':' '})
    paso('inexistente','patch','/api/solicitudes/999/',{'estado':'resuelta'})
    for n in range(10):
        Solicitud.objects.create(estudiante=e,responsable=r,titulo=f'Demo {n}',descripcion='Texto',tipo='consulta')
    with CaptureQueriesContext(connection) as consultas:
        resp=c.get('/api/solicitudes/')
        assert len(resp.json()['solicitudes'])==11
    salida={'contrato':salidas,'consultas_listado_11_solicitudes':len(consultas)}
    Path(sys.argv[1]).write_text(json.dumps(salida,indent=2,ensure_ascii=False)+'\n')
    print('Contrato:',len(salidas),'pasos; consultas SQL:',len(consultas))

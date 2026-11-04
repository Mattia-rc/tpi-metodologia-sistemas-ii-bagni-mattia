import json,sys
from pathlib import Path
a,b=(json.loads(Path(p).read_text()) for p in sys.argv[1:3])
assert a['contrato']==b['contrato'], 'El contrato observado cambió'
print('Respuestas idénticas:', len(a['contrato']))
print('Consultas:',a['consultas_listado_11_solicitudes'],'->',b['consultas_listado_11_solicitudes'])

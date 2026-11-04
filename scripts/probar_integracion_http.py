import urllib.request,urllib.error,urllib.parse,http.cookiejar,json,os
from pathlib import Path
base=os.environ.get('TPI_BASE_URL','http://127.0.0.1:4200');jar=http.cookiejar.CookieJar();opener=urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar))
results=[]
def request(paso,path,method='GET',data=None,token=False):
 headers={'Origin':base}
 if data is not None:headers['Content-Type']='application/json'
 if token:headers['X-CSRFToken']=next(x.value for x in jar if x.name=='csrftoken')
 req=urllib.request.Request(base+path,data=None if data is None else json.dumps(data).encode(),method=method,headers=headers)
 try:resp=opener.open(req,timeout=15)
 except urllib.error.HTTPError as e:resp=e
 body=resp.read();ctype=resp.headers.get('Content-Type','');obj=json.loads(body) if 'application/json' in ctype else None
 results.append({'paso':paso,'status':resp.status,'respuesta':obj})
 return resp.status,obj,body
status,obj,body=request('frontend_servido','/')
assert status==200 and b'app-root' in body
status,cat,_=request('catalogos_por_proxy','/api/catalogos/');assert status==200
payload={'estudiante_id':cat['estudiantes'][0]['id'],'titulo':'Verificación HTTP de integración','descripcion':'Registro ficticio generado durante la prueba real del proxy.','tipo':'consulta','prioridad':'alta'}
assert request('rechazo_sin_csrf','/api/solicitudes/','POST',payload)[0]==403
status,s,_=request('registro_con_csrf','/api/solicitudes/','POST',payload,True);assert status==201
status,s,_=request('cambio_y_asignacion',f"/api/solicitudes/{s['id']}/",'PATCH',{'estado':'resuelta','responsable_id':cat['responsables'][0]['id']},True)
assert status==200 and s['estado']=='resuelta' and s['responsable_id']==cat['responsables'][0]['id']
status,lista,_=request('filtro_por_proxy','/api/solicitudes/?'+urllib.parse.urlencode({'q':'Verificación HTTP','estado':'resuelta'}));assert status==200 and any(x['id']==s['id'] for x in lista['solicitudes'])
status,reporte,_=request('reporte_por_proxy','/api/reporte/');assert status==200 and reporte['por_estado']['resuelta']>=1
(Path(__file__).resolve().parents[1]/'docs/integracion_http.json').write_text(json.dumps({'tipo':'HTTP real contra Angular dev server y Django, no navegador gráfico','pasos':results,'resultado':'7 pasos aprobados; la cookie y el token no se almacenan.'},ensure_ascii=False,indent=2)+'\n')
print('Integración HTTP real: 7 pasos aprobados.')

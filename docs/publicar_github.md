# Conservar historial y publicar el repositorio

El ZIP incluye dos carpetas de código y un archivo `historial_tpi.bundle`. Las carpetas sirven para abrir y ejecutar las versiones; el bundle conserva commits y tags.

Desde la carpeta que contiene el bundle:
```bash
git clone historial_tpi.bundle proyecto_tpi
cd proyecto_tpi
git log --oneline --decorate --all
git tag
```

Crear en GitHub un repositorio vacío (sin README inicial), copiar su URL y vincularlo:
```bash
git remote remove origin
git remote add origin URL_DEL_REPOSITORIO
git push -u origin main
git push origin --tags
```
`URL_DEL_REPOSITORIO` debe reemplazarse por la URL real. No se creó un repositorio remoto ni se utilizó una cuenta GitHub en esta sesión.

Tags requeridos: `estado-inicial`, `estadorefactorizado`, `etapa-diagnostico`, `etapa-refactoring`, `etapa-pruebas`, `etapa-docs`.
Los commits fueron producidos durante la sesión bajo la identidad local “TPI asistido”; no simulan trabajo previo ni contribuciones independientes del alumno.

Comparación:
```bash
git diff estado-inicial estadorefactorizado -- backend/mi_app frontend/src/app
git show estado-inicial:backend/mi_app/views.py
```
No hacer checkout sobre cambios locales sin guardarlos. Usar una segunda copia si se quieren ejecutar ambas versiones simultáneamente.

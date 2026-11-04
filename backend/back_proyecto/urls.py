from django.urls import path
from mi_app import views

urlpatterns = [
    path('api/catalogos/', views.catalogos),
    path('api/solicitudes/', views.solicitudes),
    path('api/solicitudes/<int:pk>/', views.actualizar_solicitud),
    path('api/reporte/', views.reporte),
]

from django.urls import path
from . import views
from .views import *

# lista de urls para la app de Tales

urlpatterns = [
    path('', views.index, name='index'),
    path('register_user', views.register_user, name='register_user'),
    path('resultados_busqueda', views.resultados_busqueda, name='resultados_busqueda'),
    path('perfil/<int:id_usuario>/', views.ver_perfil_usuario, name = 'ver_perfil_usuario'),
    path('libro/<int:id_libro>/', views.ver_detalles_libro, name='ver_detalles_libro'),
    path('actualizar_estado_libro/', views.actualizar_estado_libro, name='actualizar_estado_libro'),
]
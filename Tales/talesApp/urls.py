from django.urls import path
from . import views
from .views import *

# lista de urls para la app de Tales

urlpatterns = [
    # URL basica al index
    path('', views.index, name='index'),

    #URLs desde el menu base
    path('leyendo', views.leyendo, name='leyendo'),
    path('librerias/<int:id_usuario>/', views.librerias, name='librerias'),
    path('estadisticas', views.estadisticas, name='estadisticas'),

    #URL relacionadas con usuarios
    path('register_user', views.register_user, name='register_user'),
    path('perfil/<int:id_usuario>/', views.ver_perfil_usuario, name = 'ver_perfil_usuario'),

    #URL resultados de busqueda
    path('resultados_busqueda', views.resultados_busqueda, name='resultados_busqueda'),
    
    #URL detalles de modelos
    path('libro/<int:id_libro>/', views.ver_detalles_libro, name='ver_detalles_libro'),
    path('autor/<int:id_autor>/', views.ver_detalles_autor, name='ver_detalles_autor'),
    path('saga/<int:id_saga>/', views.ver_detalles_saga, name='ver_detalles_saga'),
    path('libreria/<int:id_libreria>/', views.ver_detalles_libreria, name='ver_detalles_libreria'),
    path('completar_reto/<int:id_reto>/', views.completar_reto, name='completar_reto'),

    #URL de llamadas de ajax
    path('actualizar_estado_libro/', views.actualizar_estado_libro, name='actualizar_estado_libro'),
    path('actualizar_paginas', views.actualizar_paginas, name='actualizar_paginas'),
    path('enviar_resenna', views.enviar_resenna, name='enviar_resenna'),
    path('crear_objetivo_lectura', views.crear_objetivo_lectura, name='crear_objetivo_lectura'),
    path('crear_sesion_lectura', views.crear_sesion_lectura, name='crear_sesion_lectura'),
    path('crear_libreria', views.crear_libreria, name='crear_libreria'),
    path('editar_libreria', views.editar_libreria, name='editar_libreria'),
    path('crear_reto', views.crear_reto, name='crear_reto'),
    
    

]
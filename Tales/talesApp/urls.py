from django.urls import path
from . import views
from .views import *

# lista de urls para la app de Tales

urlpatterns = [
    # URL basica al index
    path('', views.index, name='index'),

    #URLs desde el menu base
    path('leyendo', views.leyendo, name='leyendo'),

    #URL relacionadas con usuarios
    path('register_user', views.register_user, name='register_user'),
    path('perfil/<int:id_usuario>/', views.ver_perfil_usuario, name = 'ver_perfil_usuario'),

    #URL resultados de busqueda
    path('resultados_busqueda', views.resultados_busqueda, name='resultados_busqueda'),
    
    #URL detalles de modelos
    path('libro/<int:id_libro>/', views.ver_detalles_libro, name='ver_detalles_libro'),
    path('autor/<int:id_autor>/', views.ver_detalles_autor, name='ver_detalles_autor'),
    path('saga/<int:id_saga>/', views.ver_detalles_saga, name='ver_detalles_saga'),

    #URL de actualizaciones
    path('actualizar_estado_libro/', views.actualizar_estado_libro, name='actualizar_estado_libro'),
    path('actualizar_paginas', views.actualizar_paginas, name='actualizar_paginas'),

]
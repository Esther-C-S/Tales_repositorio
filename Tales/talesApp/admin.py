from django.contrib import admin
from .models import *

# Register your models here.
# admin.site.register(Autor)
@admin.register(Autor)
class AutorAdmin(admin.ModelAdmin):
    list_display = ('id_autor', 'nombre_autor', 'apellido_autor')
    ordering = ('apellido_autor',)



# admin.site.register(Genero)
@admin.register(Genero)
class GeneroAdmin(admin.ModelAdmin):
    list_display = ('id_genero', 'nombre')
    ordering = ('id_genero',)



# admin.site.register(Usuario)
@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ('id_usuario', 'nombre_usuario', 'correo_electronico')
    ordering = ('id_usuario',)



# admin.site.register(Frase)
@admin.register(Frase)
class FraseAdmin(admin.ModelAdmin):
    list_display = ('id_frase', 'nombre_autor', 'apellido_autor', 'contenido')
    ordering = ('id_autor__apellido_autor',)

    def nombre_autor(self, obj):
        return obj.id_autor.nombre_autor
    nombre_autor.short_description = 'Nombre del Autor' 

    def apellido_autor(self, obj):
        return obj.id_autor.apellido_autor
    apellido_autor.short_description = 'Apellido del Autor' 



# admin.site.register(Saga)
@admin.register(Saga)
class SagaAdmin(admin.ModelAdmin):
    list_display = ('id_saga', 'nombre', 'nombre_autores' ,'n_libros')
    ordering = ('id_autor__apellido_autor',)

    def nombre_autores(self, obj):
        return ', '.join([f"{autor.nombre_autor} {autor.apellido_autor}" for autor in obj.id_autor.all()])
    nombre_autores.short_description = 'Autores' 



# admin.site.register(Libro)
@admin.register(Libro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ('id_libro', 'titulo', 'nombre_autores', 'id_saga')
    ordering = ('id_libro',)

    def nombre_autores(self, obj):
        return ', '.join([f"{autor.nombre_autor} {autor.apellido_autor}" for autor in obj.id_autor.all()])
    nombre_autores.short_description = 'Autores' 

    def id_saga(self, obj):
        return ', '.join([saga.nombre for saga in obj.id_saga.all()])
    id_saga.short_description = 'Nombre de la saga'



# admin.site.register(Retos)
@admin.register(Retos)
class RetosAdmin(admin.ModelAdmin):
    list_display = ('id_reto', 'nombre_usuario', 'titulo_reto')
    ordering = ('id_usuario__nombre_usuario',)

    def nombre_usuario(self, obj):
        return obj.id_usuario.nombre_usuario
    nombre_usuario.short_description = 'Nombre del Usuario'



# admin.site.register(Resenna)
@admin.register(Resenna)
class ResennaAdmin(admin.ModelAdmin):
    list_display = ('id_resenna', 'nombre_usuario', 'valoracion')
    ordering = ('id_usuario__nombre_usuario',)

    def nombre_usuario(self, obj):
        return obj.id_usuario.nombre_usuario
    nombre_usuario.short_description = 'Nombre del Usuario'



# admin.site.register(Libreria)
@admin.register(Libreria)
class LibreriaAdmin(admin.ModelAdmin):
    list_display = ('id_libreria', 'nombre_usuario', 'titulo')
    ordering = ('id_usuario__nombre_usuario',)

    def nombre_usuario(self, obj):
        return obj.id_usuario.nombre_usuario
    nombre_usuario.short_description = 'Nombre del Usuario'



# admin.site.register(Estado_libro)
@admin.register(Estado_libro)
class Estado_libroAdmin(admin.ModelAdmin):
    list_display = ('id_estado_libro', 'nombre_usuario', 'titulo')
    ordering = ('id_usuario__nombre_usuario',)

    def nombre_usuario(self, obj):
        return obj.id_usuario.nombre_usuario
    nombre_usuario.short_description = 'Nombre del Usuario'

    def titulo(self, obj):
        return obj.id_libro.titulo
    titulo.shory_description = "Titulo del Libro"
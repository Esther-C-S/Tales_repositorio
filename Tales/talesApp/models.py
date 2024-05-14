import os
from django import forms
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

def get_media_path(filename):
        return os.path.join('media', filename)

class Libro(models.Model):
    id_libro = models.AutoField(primary_key=True)
    id_saga = models.ManyToManyField('Saga')
    id_autor = models.ManyToManyField('Autor')
    id_genero = models.ManyToManyField('Genero')
    n_paginas = models.IntegerField()
    titulo = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    fecha_publicacion = models.DateField()
    sinopsis = models.TextField()
    valoracion_media = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    portada = models.ImageField(upload_to='get_media_path')

class Saga(models.Model):
    id_saga = models.AutoField(primary_key=True)
    id_autor = models.ManyToManyField('Autor')
    id_genero = models.ManyToManyField('Genero')
    nombre = models.CharField(max_length=255)
    n_libros = models.IntegerField()
    descripcion = models.TextField()

    ESTADOS = (
        ('a', 'abandonada'),
        ('c', 'completa'),
        ('e', 'en proceso')
    )

    estado_de_publicacion = models.CharField(max_length=1, choices=ESTADOS)

class Autor(models.Model):
    id_autor = models.AutoField(primary_key=True)
    nombre_autor = models.CharField(max_length=255)
    biografia = models.TextField()
    foto_autor = models.ImageField(upload_to='get_media_path')
    fecha_nacimiento = models.DateField()
    fecha_defuncion = models.DateField(null=True)
    nacionalidad = models.CharField(max_length=255)

class Frase(models.Model):
    id_frase = models.AutoField(primary_key=True)
    id_autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    contenido = models.TextField()

class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=20, )
    correo_electronico = models.EmailField()
    contrasenna = models.CharField(widget = forms.PasswordInput)
    fecha_nacimiento = models.DateField()
    biografia = models.TextField()
    foto_perfil = models.ImageField(upload_to='get_media_path')

    REQUIRED_FIELDS = ['nombre_usuario', 'correo_electronico', 'contrasenna']
    
class Resenna(models.Model):
    id_resenna = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    contenido = models.TextField()
    valoracion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

class Retos(models.Model):
    id_reto = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo_reto = models.CharField(max_length=255)
    descripcion_reto = models.TextField()
    completado = models.BooleanField(default=False)

class Libreria (models.Model):
    id_libreria = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ManyToManyField(Libro)
    titulo = models.CharField(max_length=255)
    n_libros_estanteria = models.IntegerField()

class Estado_libro(models.Model):
    id_estado_libro = models.UUIDField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ForeignKey(Libro, on_delete=models.CASCADE)

    ESTADOS = (
        ('n', 'Nada'),
        ('q', 'Quiero leer'),
        ('ly', 'Leyendo'),
        ('l', 'Leido'),
        ('a', 'Abandonado')
    )

    estado = models.CharField(max_length=2, choices=ESTADOS, default='n')

import os
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


#modelo de la clase de Libro
class Libro(models.Model):
    id_libro = models.AutoField(primary_key=True)
    id_saga = models.ManyToManyField('Saga')
    id_autor = models.ManyToManyField('Autor')
    id_genero = models.ManyToManyField('Genero')
    n_paginas = models.IntegerField()
    n_saga = models.IntegerField(null=True, blank=True)
    titulo = models.CharField(max_length=255)
    isbn = models.CharField(max_length=13)
    fecha_publicacion = models.DateField()
    sinopsis = models.TextField()
    valoracion_media = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    portada = models.ImageField(upload_to='portadas_libro')

    def __str__(self):
        return self.titulo

#modelo de la clase Saga
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

    def __str__(self):
        return self.nombre


#modelo de la clase Autor
class Autor(models.Model):
    id_autor = models.AutoField(primary_key=True)
    nombre_autor = models.CharField(max_length=255)
    apellido_autor = models.CharField(max_length=255, null=True, blank=True)
    biografia = models.TextField()
    foto_autor = models.ImageField(upload_to='autores')
    fecha_nacimiento = models.DateField()
    fecha_defuncion = models.DateField(null=True, blank=True)
    nacionalidad = models.CharField(max_length=255)

    def __str__(self):
        if self.apellido_autor:
            return f"{self.nombre_autor} {self.apellido_autor}"
        else:
            return self.nombre_autor


#modelo de la clase Frase (es la cita que sale nada mas entrar en Tales)
class Frase(models.Model):
    id_frase = models.AutoField(primary_key=True)
    id_autor = models.ForeignKey(Autor, on_delete=models.CASCADE)
    contenido = models.TextField()


#modelo de la clase Genero
class Genero(models.Model):
    id_genero = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


#modelo de la clase Usuario -> basicamente es una capa por encima de user 
#de esta forma se mantiene la seguridad de Django en cuanto a contraseñas pero con una capa extra de personalizacion en los campos
class Usuario(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    id_usuario = models.AutoField(primary_key=True)
    nombre_usuario = models.CharField(max_length=20)
    correo_electronico = models.EmailField()
    fecha_nacimiento = models.DateField()
    biografia = models.TextField()
    foto_perfil = models.ImageField(upload_to='fotos_perfil', null=True, blank=True)

    def __str__(self):
        return self.nombre_usuario
    

#modelo de la clase Reseña
class Resenna(models.Model):
    id_resenna = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    contenido = models.TextField()
    valoracion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])


#modelo de la clase Retos
class Retos(models.Model):
    id_reto = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo_reto = models.CharField(max_length=255)
    descripcion_reto = models.TextField()
    completado = models.BooleanField(default=False)


#modelo de la clase Libreria
class Libreria (models.Model):
    id_libreria = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ManyToManyField(Libro)
    titulo = models.CharField(max_length=255)
    n_libros_estanteria = models.IntegerField()


#modelo de la clase Estado_libro -> clase intermedia entre Usuario y Libro
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

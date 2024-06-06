import os, uuid
from django import forms
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


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
    fecha_creacion = models.DateField(auto_now_add=True, null=True, blank=True)
    ciudad = models.CharField(max_length=20, null=True, blank=True)
    sigue_a = models.ManyToManyField("self", symmetrical=False, blank=True)

    def __str__(self):
        return self.nombre_usuario
    

#modelo de la clase Reseña
class Resenna(models.Model):
    id_resenna = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    contenido = models.TextField()
    valoracion = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])


#modelo de la clase Retos
class Retos(models.Model):
    id_reto = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo_reto = models.CharField(max_length=255)
    completado = models.BooleanField(default=False)


#modelo de la clase ObjetivoLectura
class Objetivo_lectura(models.Model):
    id_reto = models.AutoField(primary_key=True)
    id_usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
    meta_libros = models.IntegerField()
    estado_actual = models.IntegerField()
    completado = models.BooleanField(default=False)


#modelo de la clase Libreria
class Libreria (models.Model):
    id_libreria = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ManyToManyField(Libro, blank=True)
    titulo = models.CharField(max_length=255)
    n_libros_estanteria = models.IntegerField(default=0)


#modelo de la clase Estado_libro -> clase intermedia entre Usuario y Libro
class Estado_libro(models.Model):
    id_estado_libro = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    paginas_leidas = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    fecha_leyendo = models.DateTimeField(null=True, blank=True)
    fecha_leido = models.DateTimeField(null=True, blank=True)


    ESTADOS = (
        ('n', 'Nada'),
        ('q', 'Quiero leer'),
        ('ly', 'Leyendo'),
        ('l', 'Leido'),
        ('a', 'Abandonado')
    )

    estado = models.CharField(max_length=2, choices=ESTADOS, default='n')

    def save(self, *args, **kwargs):
        if self.estado == 'n':
            self.paginas_leidas = 0
        elif self.estado == 'l':
            self.paginas_leidas = self.id_libro.n_paginas
            self.fecha_leido = timezone.now()
        elif self.estado == 'ly':
            if not self.fecha_leyendo:
                self.fecha_leyendo = timezone.now()
        super(Estado_libro, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.id_libro.titulo} - {self.get_estado_display()}"
    

#modelo de Sesiones Lectura
class Sesion_lectura(models.Model):
    id_sesion_lectura = models.AutoField(primary_key=True)
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    paginas_leidas = models.IntegerField()
    tiempo_sesion = models.IntegerField()
    fecha_sesion = models.DateField(auto_now_add=True, null=True, blank=True)


#modelo de las Medallas
class Medalla(models.Model):
    CATEGORIA_MEDALLA = (
        ('paginas_dia', 'Leer X páginas al día'),
        ('libros_mes', 'Leer X libros al mes'),
        ('consistencia_semanal', 'Consistencia de lectura semanal'),
        ('autores_diversos', 'Lectura de autores diversos'),
        ('maraton_lectura', 'Maratón de lectura'),
        ('series_trilogias', 'Completar series o trilogías'),
    )

    TIER = (
        ('madera', 'Madera'),
        ('hierro', 'Hierro'),
        ('oro', 'Oro'),
    )

    id_medalla = models.AutoField(primary_key=True)
    categoria = models.CharField(max_length=50, choices=CATEGORIA_MEDALLA)
    tier = models.CharField(max_length=10, choices=TIER)
    imagen = models.ImageField(upload_to='medallas')

    def __str__(self):
        return f'{self.get_categoria_display()} - {self.get_tier_display()}'

class UsuarioMedalla(models.Model):
    id_usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    id_medalla = models.ForeignKey(Medalla, on_delete=models.CASCADE)
    fecha_obtenida = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.id_usuario.nombre_usuario} - {self.id_medalla}'
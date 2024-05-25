from datetime import timezone
import datetime
from django.shortcuts import render, get_object_or_404
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from .forms import *
from django.shortcuts import redirect
import random
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt



#VISTA DEL INDEX
@login_required
def index(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    libros_leyendo = Estado_libro.objects.filter(id_usuario=usuario, estado='ly').select_related('id_libro').prefetch_related('id_libro__id_autor')

    libros_y_porcentajes = []
    for estado_libro in libros_leyendo:
        porcentaje = (estado_libro.paginas_leidas / estado_libro.id_libro.n_paginas) * 100
        libros_y_porcentajes.append((estado_libro, porcentaje))

    print(libros_y_porcentajes)
    context = {
        'titulo': "Inicio",
        'usuario': usuario,
        'libros_y_porcentajes': libros_y_porcentajes
    }

    return render(request, 'index.html', context=context)



#VISTAS DESDE EL MENU BASE
@login_required
def leyendo(request):
    usuario = get_object_or_404(Usuario, user=request.user)

    context = {
        'titulo' : 'Leyendo',
        'usuario' : usuario
    }
    return render(request, 'leyendo.html', context=context)



#VISTAS RELACIONADAS CON USUARIOS
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            Usuario.objects.create(
                user=user,
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                nombre_usuario=form.cleaned_data['username'],
                correo_electronico=form.cleaned_data['email'],
                biografia=form.cleaned_data.get('biografia', ''),
                foto_perfil=form.cleaned_data.get('foto_perfil', None)
            )
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')
    else:
        form = RegisterUserForm()

    context = {
        'form': form
    }
    return render(request, 'signup.html', context)


@login_required
def ver_perfil_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    nombre = usuario.nombre_usuario

    context = {
        'titulo' : nombre,
        'usuario' : usuario
    }

    return render(request, 'ver_perfil_usuario.html', context=context)  



#VISTA DEL BUSCADOR
@login_required
def resultados_busqueda(request):
    
    if request.method == "POST":

        search = request.POST['search']
        resultados = Libro.objects.filter(titulo__contains = search)
        usuario = get_object_or_404(Usuario, user=request.user)

        titulo = "Resultados"

        context = {
            'titulo' : titulo, 
            'search' : search,
            'resultados' : resultados,
            'usuario' : usuario
        }

        return render(request, 'resultados_busqueda.html', context=context)
    else:
        titulo = "Resultados"
        usuario = get_object_or_404(Usuario, user=request.user)

        context = {
            'titulo' : titulo,
            'usuario' : usuario
        }

        return render(request, 'resultados_busqueda.html', context=context)



#VER DETALLES DE MODELOS
@login_required
def ver_detalles_libro(request, id_libro):
    libro = get_object_or_404(Libro, pk=id_libro)
    usuario = get_object_or_404(Usuario, user=request.user)
    
    try:
        estado_libro = Estado_libro.objects.get(id_libro=libro, id_usuario=usuario)
        estado_actual = estado_libro.estado
    except Estado_libro.DoesNotExist:
        estado_libro = None
        estado_actual = 'n'

    context = {
        'libro': libro,
        'titulo': libro.titulo,
        'estado_actual': estado_actual,
        'estado_libro': estado_libro,
        'usuario': usuario
    }

    return render(request, 'ver_detalles_libro.html', context=context)


@login_required
def ver_detalles_autor(request, id_autor):
    autor = get_object_or_404(Autor, pk=id_autor)
    usuario = get_object_or_404(Usuario, user=request.user)

    libros = Libro.objects.filter(id_autor=id_autor)
    citas = Frase.objects.filter(id_autor=id_autor)
    cita_aleatoria = citas.order_by('?').first()

    nombre = autor.nombre_autor + " " + autor.apellido_autor

    generos = set()
    for libro in libros:
        for genero in libro.id_genero.all():
            generos.add(genero)

    context = {
        'titulo' : nombre,
        'usuario' : usuario,
        'autor': autor,
        'libros' : libros,
        'generos' : generos,
        'cita' : cita_aleatoria
    }

    return render(request, 'ver_detalles_autor.html', context=context)


@login_required
def ver_detalles_saga(request, id_saga):
    saga = get_object_or_404(Saga, pk=id_saga)
    usuario = get_object_or_404(Usuario, user=request.user)
    libros = Libro.objects.filter(id_saga=saga).order_by('n_saga')

    nombre_saga = saga.nombre

    context = {
        'titulo' : nombre_saga,
        'usuario' : usuario,
        'saga': saga,
        'libros': libros
    }

    return render(request, 'ver_detalles_saga.html', context=context)




#VISTAS DE ACTUALIZACIONES
@login_required
def actualizar_paginas(request):
    if request.method == 'POST':
        id_estado_libro = request.POST.get('id_estado_libro')
        paginas_leidas = request.POST.get('paginas_leidas')

        try:
            estado_libro = Estado_libro.objects.get(id_estado_libro=id_estado_libro)
            estado_libro.paginas_leidas = int(paginas_leidas)
            estado_libro.save()
            return JsonResponse({'success': True})
        except Estado_libro.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Estado libro no encontrado'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})


@csrf_exempt
@login_required
def actualizar_estado_libro(request):
    if request.method == 'POST':
        id_libro = request.POST.get('id_libro')
        estado = request.POST.get('estado')
        
        libro = get_object_or_404(Libro, id_libro=id_libro)
        usuario = get_object_or_404(Usuario, user=request.user)

        estado_libro, created = Estado_libro.objects.get_or_create(id_libro=libro, id_usuario=usuario)
        estado_libro.estado = estado
        if estado == 'ly':
            if not estado_libro.fecha_leyendo:
                estado_libro.fecha_leyendo = timezone.now()
        elif estado == 'l':
            estado_libro.fecha_leido = timezone.now()
        estado_libro.save()

        estados_dict = dict(Estado_libro.ESTADOS)
        estado_text = estados_dict[estado]

        return JsonResponse({'success': True, 'estado_text': estado_text})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
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


@login_required
def index(request):
    titulo = "Inicio"
    usuario = Usuario.objects.get(user=request.user)

    context = {
        'titulo' : titulo,
        'usuario' : usuario
    }

    return render(request, 'index.html', context=context)



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


def ver_perfil_usuario(request, id_usuario):
    usuario = get_object_or_404(Usuario, pk=id_usuario)
    nombre = usuario.nombre_usuario

    context = {
        'titulo' : nombre,
        'usuario' : usuario
    }

    return render(request, 'ver_perfil_usuario.html', context=context)  



def  ver_detalles_libro(request, id_libro):
    libro = get_object_or_404(Libro, pk=id_libro)
    titulo = libro.titulo
    usuario = get_object_or_404(Usuario, user=request.user)

    context = {
        'libro' : libro,
        'titulo' : titulo,
        'usuario' : usuario
    }

    return render(request, 'ver_detalles_libro.html', context=context)


@csrf_exempt
@login_required
def actualizar_estado_libro(request):
    if request.method == 'POST':
        libro_id = request.POST.get('libro_id')
        estado = request.POST.get('estado')
        
        libro = Libro.objects.get(id=libro_id)
        usuario = request.user

        estado_libro, created = Estado_libro.objects.get_or_create(id_libro=libro, id_usuario=usuario)
        estado_libro.estado = estado
        estado_libro.save()

        estados_dict = dict(Estado_libro.ESTADOS)
        estado_text = estados_dict[estado]

        return JsonResponse({'success': True, 'estado_text': estado_text})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})
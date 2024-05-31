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
from django.db.models import Sum, Count
from .utils import *
from collections import defaultdict


#VISTA DEL INDEX
@login_required
def index(request):
    usuario_autenticado = get_object_or_404(Usuario, user=request.user)
    libros_leyendo = Estado_libro.objects.filter(id_usuario=usuario_autenticado, estado='ly').select_related('id_libro').prefetch_related('id_libro__id_autor')
    print(usuario_autenticado)
    sigue_a = usuario_autenticado.sigue_a.all().order_by('?')[:3]
    print(sigue_a)

    sigue_a_con_libro = []
    for seguido in sigue_a:
        libros_leyendo_seguido = list(Estado_libro.objects.filter(id_usuario=seguido, estado='ly').select_related('id_libro'))
        libro_aleatorio = random.choice(libros_leyendo_seguido) if libros_leyendo_seguido else None
        sigue_a_con_libro.append((seguido, libro_aleatorio))

    print(sigue_a_con_libro)

    libros_y_porcentajes = []
    for estado_libro in libros_leyendo:
        porcentaje = (estado_libro.paginas_leidas / estado_libro.id_libro.n_paginas) * 100
        libros_y_porcentajes.append((estado_libro, porcentaje))

    try:
        objetivo_lectura = Objetivo_lectura.objects.get(id_usuario=usuario_autenticado)
        porcentaje_objetivo = (objetivo_lectura.estado_actual / objetivo_lectura.meta_libros) * 100
    except Objetivo_lectura.DoesNotExist:
        objetivo_lectura = None
        porcentaje_objetivo = 0

    medallas_usuario = UsuarioMedalla.objects.filter(id_usuario=usuario_autenticado)
    todas_medallas = Medalla.objects.all()

    medallas_dict = defaultdict(lambda: 'x')  # Por defecto, 'x' si no tiene la medalla
    
    # Inicializa el diccionario con todas las categorías de medallas
    categorias_medallas = Medalla.CATEGORIA_MEDALLA
    for categoria, _ in categorias_medallas:
        medallas_dict[categoria] = 'x'
    
    for medalla in todas_medallas:
        if medallas_usuario.filter(id_medalla=medalla).exists():
            if medallas_dict[medalla.categoria] == 'x' or medalla.tier > medallas_dict[medalla.categoria]:
                medallas_dict[medalla.categoria] = medalla.tier

    context = {
        'titulo': "Inicio",
        'usuario_autenticado': usuario_autenticado,
        'libros_y_porcentajes': libros_y_porcentajes,
        'objetivo_lectura': objetivo_lectura,
        'porcentaje_objetivo': porcentaje_objetivo,
        'sigue_a': sigue_a,
        'sigue_a_con_libro': sigue_a_con_libro,
        'medallas_dict': dict(medallas_dict),
        'todas_medallas': todas_medallas,
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


@login_required
def librerias(request, id_usuario):
    usuario = get_object_or_404(Usuario, user=request.user)

    # Obtén o crea las librerías estándar
    abandonados, created = Libreria.objects.get_or_create(id_usuario=usuario, titulo='Abandonados')
    quiero_leer, created = Libreria.objects.get_or_create(id_usuario=usuario, titulo='Quiero Leer')
    leidos, created = Libreria.objects.get_or_create(id_usuario=usuario, titulo='Leídos')
    leyendo, created = Libreria.objects.get_or_create(id_usuario=usuario, titulo='Leyendo')

    # Filtra librerías personalizadas
    librerias_personalizadas = Libreria.objects.filter(id_usuario=usuario).exclude(
        titulo__in=['Abandonados', 'Quiero Leer', 'Leídos', 'Leyendo']
    )

    # Lista de estanterías predefinidas
    estanterias = [leyendo, quiero_leer, leidos]

    # Calcula el número de libros y asigna portadas aleatorias
    for estanteria in estanterias:
        estanteria.n_libros_estanteria = estanteria.id_libro.count()
        libros = list(estanteria.id_libro.all())
        estanteria.portadas = random.sample(libros, min(3, len(libros)))

    abandonados.n_libros_estanteria = abandonados.id_libro.count()
    abandonados_libros = list(abandonados.id_libro.all())
    abandonados.portadas = random.sample(abandonados_libros, min(1, len(abandonados_libros)))

    for libreria in librerias_personalizadas:
        libreria.n_libros_estanteria = libreria.id_libro.count()
        libros = list(libreria.id_libro.all())
        libreria.portadas = random.sample(libros, min(1, len(libros)))

    context = {
        'titulo': 'Librerias',
        'usuario': usuario,
        'abandonados': abandonados,
        'quiero_leer': quiero_leer,
        'leidos': leidos,
        'leyendo': leyendo,
        'librerias_personalizadas': librerias_personalizadas,
        'estanterias': estanterias,
    }
    return render(request, 'librerias.html', context=context)


@login_required
def estadisticas(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    año_actual = datetime.datetime.now().year

    sesiones = Sesion_lectura.objects.filter(id_usuario=usuario, fecha_sesion__year=año_actual)
    paginas = sesiones.aggregate(Sum('paginas_leidas'))['paginas_leidas__sum'] or 0

    libros_leidos = Estado_libro.objects.filter(id_usuario=usuario, fecha_leido__year=año_actual)
    libros = libros_leidos.count()

    id_libros_leidos = libros_leidos.values_list('id_libro', flat=True)
    autores = Autor.objects.filter(libro__id_libro__in=id_libros_leidos).distinct()
    numero_autores = autores.count()

    sagas = Saga.objects.filter(libro__id_libro__in=id_libros_leidos).distinct()
    num_sagas = sagas.count()

    libros_por_mes = libros_leidos.values('fecha_leido__month').annotate(num_libros=Count('id_estado_libro')).order_by('fecha_leido__month')
    libros_leidos_por_mes = [0] * 12 
    for item in libros_por_mes:
        month_index = item['fecha_leido__month'] - 1  
        libros_leidos_por_mes[month_index] = item['num_libros']

    generos_libros = Libro.objects.filter(id_libro__in=id_libros_leidos) \
                                  .values('id_genero__nombre') \
                                  .annotate(num_libros=Count('id_libro')) \
                                  .order_by('id_genero__nombre')
    generos_data = []
    for genero in generos_libros:
        generos_data.append({
            'name': genero['id_genero__nombre'],
            'y': genero['num_libros']
        })

    medallas_usuario = UsuarioMedalla.objects.filter(id_usuario=usuario)
    todas_medallas = Medalla.objects.all()

    medallas_dict = defaultdict(lambda: 'x')  # Por defecto, 'x' si no tiene la medalla
    
    # Inicializa el diccionario con todas las categorías de medallas
    categorias_medallas = Medalla.CATEGORIA_MEDALLA
    for categoria, _ in categorias_medallas:
        medallas_dict[categoria] = 'x'
    
    for medalla in todas_medallas:
        if medallas_usuario.filter(id_medalla=medalla).exists():
            if medallas_dict[medalla.categoria] == 'x' or medalla.tier > medallas_dict[medalla.categoria]:
                medallas_dict[medalla.categoria] = medalla.tier

    retos = Retos.objects.filter(id_usuario=usuario, completado=False)

    context = {
        'titulo': 'Estadisticas',
        'usuario': usuario,
        'año_actual': año_actual,
        'paginas': paginas,
        'libros': libros,
        'autores': numero_autores,
        'sagas': num_sagas,
        'libros_leidos_por_mes': libros_leidos_por_mes,
        'generos_data': generos_data,
        'medallas_dict': dict(medallas_dict),
        'todas_medallas': todas_medallas,
        'retos' : retos
    }
    return render(request, 'estadisticas.html', context=context)




#VISTAS RELACIONADAS CON USUARIOS
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            usuario = Usuario.objects.create(
                user=user,
                fecha_nacimiento=form.cleaned_data['fecha_nacimiento'],
                nombre_usuario=form.cleaned_data['username'],
                correo_electronico=form.cleaned_data['email'],
                biografia=form.cleaned_data.get('biografia', ''),
                foto_perfil=form.cleaned_data.get('foto_perfil', None)
            )
            
            # Crear las cuatro librerías para el nuevo usuario
            titulos_librerias = [ "Quiero leer", "Leyendo", "Leídos", "Abandonados"]
            for titulo in titulos_librerias:
                Libreria.objects.create(
                    id_usuario=usuario,
                    titulo=titulo,
                    n_libros_estanteria=0
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
    print(usuario)

    if request.method == "POST":
        usuario_actual = request.user.usuario
        action = request.POST['follow']

        if action == "unfollow":
            usuario_actual.sigue_a.remove(usuario)
        elif action == "follow":
            usuario_actual.sigue_a.add(usuario)
        
        usuario_actual.save()
    

    reseñas = Resenna.objects.filter(id_usuario=id_usuario, valoracion=5)
    id_libros_favoritos = reseñas.values_list('id_libro', flat=True)
    libros_fav_list = list(Libro.objects.filter(id_libro__in=id_libros_favoritos))
    if len(libros_fav_list) > 0:
        libros_fav = random.sample(libros_fav_list, min(len(libros_fav_list), 5))
    else:
        libros_fav = []

    libros_leyendo = Estado_libro.objects.filter(id_usuario=usuario, estado='ly').select_related('id_libro').prefetch_related('id_libro__id_autor')

    libros_y_porcentajes = []
    for estado_libro in libros_leyendo:
        porcentaje = (estado_libro.paginas_leidas / estado_libro.id_libro.n_paginas) * 100
        libros_y_porcentajes.append((estado_libro, porcentaje))

    try:
        objetivo_lectura = Objetivo_lectura.objects.get(id_usuario=usuario)
        porcentaje_objetivo = (objetivo_lectura.estado_actual / objetivo_lectura.meta_libros) * 100
    except Objetivo_lectura.DoesNotExist:
        objetivo_lectura = None
        porcentaje_objetivo = 0

    medallas_usuario = UsuarioMedalla.objects.filter(id_usuario=usuario)
    todas_medallas = Medalla.objects.all()

    medallas_dict = defaultdict(lambda: 'x')  # Por defecto, 'x' si no tiene la medalla
    
    # Inicializa el diccionario con todas las categorías de medallas
    categorias_medallas = Medalla.CATEGORIA_MEDALLA
    for categoria, _ in categorias_medallas:
        medallas_dict[categoria] = 'x'
    
    for medalla in todas_medallas:
        if medallas_usuario.filter(id_medalla=medalla).exists():
            if medallas_dict[medalla.categoria] == 'x' or medalla.tier > medallas_dict[medalla.categoria]:
                medallas_dict[medalla.categoria] = medalla.tier

    context = {
        'titulo' : nombre,
        'usuario' : usuario,
        'reseñas' : reseñas,
        'libros_y_porcentajes': libros_y_porcentajes,
        'libros_fav' : libros_fav,
        'objetivo_lectura': objetivo_lectura,
        'porcentaje_objetivo' : porcentaje_objetivo,
        'medallas_dict': dict(medallas_dict),
        'todas_medallas': todas_medallas,
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
    reseñas = Resenna.objects.filter(id_libro=libro)
    librerias = Libreria.objects.filter(id_usuario=usuario)

    try:
        valoracion_usuario = Resenna.objects.get(id_libro=libro, id_usuario=usuario).valoracion
    except Resenna.DoesNotExist:
        valoracion_usuario = None

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
        'usuario': usuario,
        'valoracion_usuario': valoracion_usuario, 
        'reseñas' : reseñas,
        'librerias' : librerias,
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


@login_required
def ver_detalles_libreria(request, id_libreria):
    libreria = get_object_or_404(Libreria, pk=id_libreria)
    usuario = get_object_or_404(Usuario, user=request.user)
    libros = libreria.id_libro.all()

    nombre = libreria.titulo

    context = {
        'titulo' : nombre,
        'usuario' : usuario,
        'libreria': libreria,
        'libros': libros
    }

    return render(request, 'ver_detalles_libreria.html', context=context)



#VISTAS DE LLAMADAS DE AJAX
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
            try:
                objetivo_lectura = Objetivo_lectura.objects.get(id_usuario=usuario)
                objetivo_lectura.estado_actual += 1
                objetivo_lectura.save() 
            except Objetivo_lectura.DoesNotExist:
                objetivo_lectura = None
        estado_libro.save()

        nombres_librerias = {
            'ly': 'Leyendo',
            'l': 'Leídos',
            'q': 'Quiero Leer',
            'a': 'Abandonados'
        }

        #Busca o crea la libreria
        for key, titulo in nombres_librerias.items():
            Libreria.objects.get_or_create(id_usuario=usuario, titulo=titulo)

        #Añade el libro a la libreria
        libreria = Libreria.objects.get(id_usuario=usuario, titulo=nombres_librerias[estado])
        libreria.id_libro.add(libro)
        libreria.n_libros_estanteria = libreria.id_libro.count()
        libreria.save()

        # Quita el libro de la libreria en la que esta si cambia el estado
        for key, titulo in nombres_librerias.items():
            if key != estado:
                libreria = Libreria.objects.get(id_usuario=usuario, titulo=titulo)
                libreria.id_libro.remove(libro)
                libreria.n_libros_estanteria = libreria.id_libro.count()
                libreria.save()

        estados_dict = dict(Estado_libro.ESTADOS)
        estado_text = estados_dict[estado]

        otorgar_medallas_libros_mes(usuario)
        otorgar_medallas_autores_diversos(usuario)
        otorgar_medallas_series_trilogias(usuario)

        return JsonResponse({'success': True, 'estado_text': estado_text})
    
    return JsonResponse({'success': False, 'error': 'Invalid request method'})

@csrf_exempt
@login_required
def enviar_resenna(request):
    if request.method == 'POST':
        valoracion = request.POST.get('valoracion')
        opinion = request.POST.get('opinion')
        id_libro = request.POST.get('id_libro')

        usuario = get_object_or_404(Usuario, user=request.user)
        libro = get_object_or_404(Libro, pk=id_libro)

        reseña = Resenna.objects.create(
            id_usuario=usuario,
            id_libro=libro,
            contenido=opinion,
            valoracion=valoracion
        )
        return JsonResponse({'success': True, 'message': 'Reseña enviada con éxito'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


@csrf_exempt
@login_required
def crear_libreria(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')

        usuario = get_object_or_404(Usuario, user=request.user)

        libreria = Libreria.objects.create(
            id_usuario=usuario,
            titulo=titulo,
        )
        return JsonResponse({'success': True, 'message': 'Reseña enviada con éxito'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def editar_libreria(request):
    if request.method == 'POST':
        id_libro = request.POST.get('id_libro')
        id_libreria = request.POST.get('id_libreria')
        añadir = request.POST.get('añadir') == 'true'

        libreria = get_object_or_404(Libreria, pk=id_libreria)

        if añadir:
            libreria.id_libro.add(id_libro)
        else:
            libreria.id_libro.remove(id_libro)

        return JsonResponse({'success': True, 'message': 'Librería actualizada con éxito'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def crear_reto(request):
    if request.method == 'POST':
        titulo_reto = request.POST.get('titulo')
        usuario = get_object_or_404(Usuario, user=request.user)

        reto = Retos.objects.create(
            titulo_reto = titulo_reto,
            id_usuario = usuario
        )

        return JsonResponse({'success': True, 'message': 'Librería actualizada con éxito'})
    return JsonResponse({'success': False, 'error': 'Invalid request method'})



#VISTA DE CREACION DE OBJETIVO DE LECTURA
@login_required
def crear_objetivo_lectura(request):
    usuario = get_object_or_404(Usuario, user=request.user)

    # Verificar si el usuario ya tiene un objetivo de lectura
    try:
        objetivo_existente = Objetivo_lectura.objects.get(id_usuario=usuario)
        tiene_objetivo = True
    except Objetivo_lectura.DoesNotExist:
        objetivo_existente = None
        tiene_objetivo = False

    if request.method == 'POST':
        meta_libros = request.POST.get('meta_libros')

        current_year = datetime.datetime.now().year
        start_date = datetime.datetime(current_year, 1, 1)
        end_date = datetime.datetime(current_year, 12, 31, 23, 59, 59)

        libros_leidos = Estado_libro.objects.filter(
            id_usuario=usuario,
            estado='l',
            fecha_leido__range=(start_date, end_date)
        ).count()

        if not tiene_objetivo:
            Objetivo_lectura.objects.create(
                id_usuario=usuario,
                meta_libros=meta_libros,
                estado_actual=libros_leidos
            )
            return JsonResponse({'success': True, 'message': 'Objetivo de lectura creado con éxito'})
        else:
            return JsonResponse({'success': False, 'error': 'Ya tienes un objetivo de lectura para este año'})

    context = {
        'tiene_objetivo': tiene_objetivo,
        'objetivo_existente': objetivo_existente
    }

    return render(request, 'tu_template.html', context=context)

@csrf_exempt
@login_required
def crear_sesion_lectura(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    
    if request.method == 'POST':
        paginas_leidas = request.POST.get('paginas_leidas')
        tiempo_sesion = request.POST.get('tiempo_sesion')

        if not paginas_leidas or not tiempo_sesion:
            return JsonResponse({'success': False, 'error': 'Faltan datos requeridos'})

        Sesion_lectura.objects.create(
            id_usuario=usuario,
            paginas_leidas=paginas_leidas,
            tiempo_sesion=tiempo_sesion
        )

        # Otorgar las medallas correspondientes
        otorgar_medallas_paginas_dia(usuario)
        otorgar_medallas_consistencia_semanal(usuario)
        otorgar_medallas_maraton_lectura(usuario)

        return JsonResponse({'success': True, 'message': 'Sesión de lectura creada con éxito'})
    return JsonResponse({'success': False, 'error': 'Método de solicitud no válido'})

def completar_reto(request, id_reto):

    reto = get_object_or_404(Retos, id_reto=id_reto)
    reto.completado = True
    reto.save()
    return redirect('estadisticas')
from datetime import timedelta
from django.utils import timezone
from django.db.models import Sum
from .models import UsuarioMedalla, Medalla, Sesion_lectura, Estado_libro, Libro

def eliminar_medallas_otras(usuario, categoria, tier_actual):
    tiers = ['madera', 'hierro', 'oro']
    tiers.remove(tier_actual)
    UsuarioMedalla.objects.filter(id_usuario=usuario, id_medalla__categoria=categoria, id_medalla__tier__in=tiers).delete()

def otorgar_medallas_paginas_dia(usuario):
    hoy = timezone.now().date()
    sesiones_hoy = Sesion_lectura.objects.filter(id_usuario=usuario, fecha_sesion=hoy)
    paginas_hoy = sesiones_hoy.aggregate(Sum('paginas_leidas'))['paginas_leidas__sum'] or 0

    if paginas_hoy >= 100:
        tier = 'oro'
    elif paginas_hoy >= 50:
        tier = 'hierro'
    elif paginas_hoy >= 25:
        tier = 'madera'
    else:
        return

    medalla = Medalla.objects.get(categoria='paginas_dia', tier=tier)
    eliminar_medallas_otras(usuario, 'paginas_dia', tier)
    usuario_medalla, created = UsuarioMedalla.objects.get_or_create(id_usuario=usuario, id_medalla=medalla)
    if not created:
        usuario_medalla.id_medalla = medalla
        usuario_medalla.save()

def otorgar_medallas_libros_mes(usuario):
    hoy = timezone.now().date()
    primer_dia_mes = hoy.replace(day=1)
    libros_mes = Estado_libro.objects.filter(id_usuario=usuario, fecha_leido__gte=primer_dia_mes).count()

    if libros_mes >= 10:
        tier = 'oro'
    elif libros_mes >= 4:
        tier = 'hierro'
    elif libros_mes >= 1:
        tier = 'madera'
    else:
        return

    medalla = Medalla.objects.get(categoria='libros_mes', tier=tier)
    eliminar_medallas_otras(usuario, 'libros_mes', tier)
    usuario_medalla, created = UsuarioMedalla.objects.get_or_create(id_usuario=usuario, id_medalla=medalla)
    if not created:
        usuario_medalla.id_medalla = medalla
        usuario_medalla.save()

def calcular_semana(fecha):
    """Calcula la semana del mes de una fecha dada (1 a 5)."""
    return (fecha.day - 1) // 7 + 1

def otorgar_medallas_consistencia_semanal(usuario):
    hoy = timezone.now().date()
    primer_dia_mes = hoy.replace(day=1)
    ultimo_dia_mes = (primer_dia_mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    dias_lectura = Sesion_lectura.objects.filter(id_usuario=usuario, fecha_sesion__range=(primer_dia_mes, ultimo_dia_mes)).values('fecha_sesion').distinct()
    dias_lectura_por_semana = {}

    for dia in dias_lectura:
        semana = calcular_semana(dia['fecha_sesion'])
        if semana not in dias_lectura_por_semana:
            dias_lectura_por_semana[semana] = 0
        dias_lectura_por_semana[semana] += 1

    total_semanas = (ultimo_dia_mes - primer_dia_mes).days // 7 + 1
    dias_lectura_por_semana = {semana: dias_lectura_por_semana.get(semana, 0) for semana in range(1, total_semanas + 1)}

    if all(d >= 7 for d in dias_lectura_por_semana.values()):
        tier = 'oro'
    elif all(d >= 5 for d in dias_lectura_por_semana.values()):
        tier = 'hierro'
    elif all(d >= 3 for d in dias_lectura_por_semana.values()):
        tier = 'madera'
    else:
        return

    medalla = Medalla.objects.get(categoria='consistencia_semanal', tier=tier)
    eliminar_medallas_otras(usuario, 'consistencia_semanal', tier)
    usuario_medalla, created = UsuarioMedalla.objects.get_or_create(id_usuario=usuario, id_medalla=medalla)
    if not created:
        usuario_medalla.id_medalla = medalla
        usuario_medalla.save()

def otorgar_medallas_autores_diversos(usuario):
    hoy = timezone.now().date()
    primer_dia_mes = hoy.replace(day=1)
    libros_mes = Estado_libro.objects.filter(id_usuario=usuario, fecha_leido__gte=primer_dia_mes).values('id_libro__id_autor').distinct()
    autores_mes = len(set(libro['id_libro__id_autor'] for libro in libros_mes))

    if autores_mes >= 10:
        tier = 'oro'
    elif autores_mes >= 5:
        tier = 'hierro'
    elif autores_mes >= 3:
        tier = 'madera'
    else:
        return

    medalla = Medalla.objects.get(categoria='autores_diversos', tier=tier)
    eliminar_medallas_otras(usuario, 'autores_diversos', tier)
    usuario_medalla, created = UsuarioMedalla.objects.get_or_create(id_usuario=usuario, id_medalla=medalla)
    if not created:
        usuario_medalla.id_medalla = medalla
        usuario_medalla.save()

def otorgar_medallas_maraton_lectura(usuario):
    hoy = timezone.now().date()
    sesiones_hoy = Sesion_lectura.objects.filter(id_usuario=usuario, fecha_sesion=hoy)
    tiempo_hoy = sesiones_hoy.aggregate(Sum('tiempo_sesion'))['tiempo_sesion__sum'] or 0

    if tiempo_hoy >= 360:  # 6 horas
        tier = 'oro'
    elif tiempo_hoy >= 240:  # 4 horas
        tier = 'hierro'
    elif tiempo_hoy >= 120:  # 2 horas
        tier = 'madera'
    else:
        return

    medalla = Medalla.objects.get(categoria='maraton_lectura', tier=tier)
    eliminar_medallas_otras(usuario, 'maraton_lectura', tier)
    usuario_medalla, created = UsuarioMedalla.objects.get_or_create(id_usuario=usuario, id_medalla=medalla)
    if not created:
        usuario_medalla.id_medalla = medalla
        usuario_medalla.save()

def otorgar_medallas_series_trilogias(usuario):
    series_libros = Libro.objects.filter(id_libro__in=Estado_libro.objects.filter(id_usuario=usuario).values_list('id_libro', flat=True).distinct())
    
    series_leidas = {}
    for libro in series_libros:
        for saga in libro.id_saga.all():
            if saga.id not in series_leidas:
                series_leidas[saga.id] = 0
            series_leidas[saga.id] += 1

    for saga_id, libros_leidos in series_leidas.items():
        if libros_leidos >= 3:
            tier = 'oro'
        elif libros_leidos >= 2:
            tier = 'hierro'
        elif libros_leidos >= 1:
            tier = 'madera'
        else:
            continue

        medalla = Medalla.objects.get(categoria='series_trilogias', tier=tier)
        eliminar_medallas_otras(usuario, 'series_trilogias', tier)
        usuario_medalla, created = UsuarioMedalla.objects.get_or_create(id_usuario=usuario, id_medalla=medalla)
        if not created:
            usuario_medalla.id_medalla = medalla
            usuario_medalla.save()

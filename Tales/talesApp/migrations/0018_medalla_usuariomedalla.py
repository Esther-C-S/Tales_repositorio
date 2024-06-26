# Generated by Django 5.0.6 on 2024-05-28 18:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talesApp', '0017_alter_libreria_id_libro_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Medalla',
            fields=[
                ('id_medalla', models.AutoField(primary_key=True, serialize=False)),
                ('categoria', models.CharField(choices=[('paginas_dia', 'Leer X páginas al día'), ('libros_mes', 'Leer X libros al mes'), ('consistencia_semanal', 'Consistencia de lectura semanal'), ('autores_diversos', 'Lectura de autores diversos'), ('maraton_lectura', 'Maratón de lectura'), ('series_trilogias', 'Completar series o trilogías')], max_length=50)),
                ('tier', models.CharField(choices=[('madera', 'Madera'), ('hierro', 'Hierro'), ('oro', 'Oro')], max_length=10)),
                ('imagen', models.ImageField(upload_to='medallas')),
            ],
        ),
        migrations.CreateModel(
            name='UsuarioMedalla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_obtenida', models.DateField(auto_now_add=True)),
                ('id_medalla', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talesApp.medalla')),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]

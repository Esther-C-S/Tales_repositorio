# Generated by Django 5.0.6 on 2024-05-29 09:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('talesApp', '0021_remove_medalla_descripcion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='retos',
            name='descripcion_reto',
        ),
    ]

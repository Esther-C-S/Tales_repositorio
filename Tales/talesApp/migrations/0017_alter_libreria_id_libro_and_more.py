# Generated by Django 5.0.6 on 2024-05-27 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talesApp', '0016_usuario_sigue_a'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libreria',
            name='id_libro',
            field=models.ManyToManyField(blank=True, to='talesApp.libro'),
        ),
        migrations.AlterField(
            model_name='libreria',
            name='n_libros_estanteria',
            field=models.IntegerField(default=0),
        ),
    ]
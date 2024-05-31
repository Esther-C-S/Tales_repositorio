# Generated by Django 5.0.6 on 2024-05-26 11:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talesApp', '0011_alter_objetivo_lectura_id_usuario'),
    ]

    operations = [
        migrations.CreateModel(
            name='sesion_lectura',
            fields=[
                ('id_sesion_lectura', models.AutoField(primary_key=True, serialize=False)),
                ('paginas_leidas', models.IntegerField()),
                ('tiempo_sesion', models.IntegerField()),
                ('id_usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talesApp.usuario')),
            ],
        ),
    ]
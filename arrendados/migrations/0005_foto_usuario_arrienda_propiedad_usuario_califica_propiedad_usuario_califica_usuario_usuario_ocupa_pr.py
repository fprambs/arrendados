# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-25 02:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('arrendados', '0004_auto_20161225_0244'),
    ]

    operations = [
        migrations.CreateModel(
            name='Foto',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ruta', models.CharField(max_length=200)),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arrendados.Propiedad')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Arrienda_Propiedad',
            fields=[
                ('fecha_inicio', models.DateTimeField(primary_key=True, serialize=False)),
                ('fecha_termino', models.DateTimeField(null=True)),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arrendados.Propiedad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arrendados.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Califica_Propiedad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('calificacion', models.IntegerField()),
                ('comentario', models.CharField(max_length=500, null=True)),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arrendados.Propiedad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arrendados.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Califica_Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('calificacion', models.IntegerField()),
                ('usuario1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario1', to='arrendados.Usuario')),
                ('usuario2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='usuario2', to='arrendados.Usuario')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario_Ocupa_Propiedad',
            fields=[
                ('fecha_inicio', models.DateTimeField(primary_key=True, serialize=False)),
                ('fecha_termino', models.DateTimeField(null=True)),
                ('propiedad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arrendados.Propiedad')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='arrendados.Usuario')),
            ],
        ),
    ]

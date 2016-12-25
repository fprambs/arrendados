from __future__ import unicode_literals

from django.db import models


class Tipo_Usuario(models.Model):
    tipo = models.CharField(max_length=45)

class Usuario(models.Model):
    nombre = models.CharField(max_length=80)
    fecha_nacimiento = models.DateField()
    email= models.CharField(max_length=80, unique=True)
    password = models.CharField(max_length=15)
    telefono = models.IntegerField(null= True)
    direccion = models.CharField(max_length=80,null=True)
    check_offer = models.NullBooleanField(default=False)
    tipo_usuario = models.ForeignKey(Tipo_Usuario)

class Region(models.Model):
    region = models.CharField(max_length=30)

class Comuna(models.Model):
    comuna = models.CharField(max_length=30)
    region = models.ForeignKey(Region)

class Ciudad(models.Model):
    ciudad = models.CharField(max_length=30)
    comuna = models.ForeignKey(Comuna)


class Tipo_Propiedad(models.Model):
    tipo = models.CharField(max_length=30)

class Propiedad(models.Model):
    direccion = models.CharField(max_length=80)
    cantidad_disponible = models.IntegerField()
    cantidad = models.IntegerField()
    latitud = models.CharField(max_length=40)
    longitud = models.CharField(max_length=40)
    ciudad = models.ForeignKey(Ciudad)
    tipo_propiedad = models.ForeignKey(Tipo_Propiedad)


class Foto(models.Model):
    ruta = models.CharField(max_length=200)
    propiedad= models.ForeignKey(Propiedad)

#Arrendatario
class Usuario_Ocupa_Propiedad(models.Model):
     usuario = models.ForeignKey(Usuario)
     propiedad = models.ForeignKey(Propiedad)
     fecha_inicio = models.DateTimeField(primary_key=True)
     fecha_termino = models.DateTimeField(null=True)
#Arrendador   
class Usuario_Arrienda_Propiedad(models.Model):
     usuario = models.ForeignKey(Usuario)
     propiedad = models.ForeignKey(Propiedad)
     fecha_inicio = models.DateTimeField(primary_key=True)
     fecha_termino = models.DateTimeField(null=True)


class Usuario_Califica_Usuario(models.Model):
    usuario1 = models.ForeignKey(Usuario,related_name='usuario1')
    usuario2 = models.ForeignKey(Usuario, related_name='usuario2')
    fecha = models.DateField()
    calificacion = models.IntegerField()

class Usuario_Califica_Propiedad(models.Model):
    fecha = models.DateField()
    calificacion = models.IntegerField()
    comentario = models.CharField(max_length=500,null=True)
    usuario = models.ForeignKey(Usuario)
    propiedad = models.ForeignKey(Propiedad)
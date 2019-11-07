from django.db import models
from random import choice

from django.db.models.deletion import CASCADE
from persona.models import Profile, Persona
from _datetime import datetime


class Tipo (models.Model):
    nombre = models.CharField(max_length=50, null=True)
    def __str__(self):
        return '{}'.format(self.nombre)
    class Meta:
        verbose_name = "Tipo"
        verbose_name_plural = "Tipos"



# Create your models here

#===============================================================================
# class Tipo(models.Model):
#     nombre = models.CharField(max_length=50, null=True)
#     ropa = models.ForeignKey(Ropa, on_delete = models.CASCADE , null=True)
#     
#     def __str__(self):
#         return '{}'.format(self.nombre)
#         
#===============================================================================
from django.conf import settings
class Donacion(models.Model):
    TIPO_ACTIVO = 1
    TIPO_INACTIVO = 0
    TIPO_CHOICES = {
             (TIPO_ACTIVO, 'Activo'),
             (TIPO_INACTIVO, 'Inactivo'),             
         }
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    nombres = models.CharField(max_length=100, null=True)
    apellido_paterno = models.CharField(max_length=100, null=True)
    #producto = models.ManyToManyField(Producto) 
    estado = models.SmallIntegerField(choices = TIPO_CHOICES, null=True, default=True) 
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True) 

    
    
    def __str__(self):
        return '{}/{}, {}'.format(self.id, self.persona, self.created)
    class Meta:
        
        verbose_name = "Donacion"
        verbose_name_plural = "Donaciones"






class Categoria (models.Model):
    categoria = models.CharField(max_length=50, null=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    
    def __str__(self):
        return '{}'.format(self.categoria)
    class Meta:
        
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"




class Producto (models.Model):
    TIPO_ACTIVO = 0
    TIPO_INACTIVO = 1
    # TIPO_DESCOMPUESTO = 2
    TIPO_CHOICES = {
             (TIPO_ACTIVO, 'Activo'),
             (TIPO_INACTIVO, 'Inactivo'),
             # (TIPO_DESCOMPUESTO, 'Descompuesto'),             
         }

    TIPO_VALIDA = 0
    TIPO_DESCOMPUESTO = 1
    CONDICION_CHOICES = {
             
             (TIPO_VALIDA, 'Valida'),
             (TIPO_DESCOMPUESTO, 'Descompuesto'),             
         }
    tipo  = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True)
    descripcion = models.CharField(max_length=100, null=True)
   
    fecha_expiracion = models.DateField(null=True, blank = True, default='12/12/2020')
    cantidad = models.PositiveIntegerField(null=True)
    estado = models.SmallIntegerField(choices = TIPO_CHOICES, null=True, default=TIPO_ACTIVO, blank=True)
    stock = models.IntegerField(null=True, blank=True, default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, null=True, blank=True)
    condicion = models.SmallIntegerField(choices = CONDICION_CHOICES, null=True, default=TIPO_VALIDA, blank=True)

    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)

    
    
    donacion = models.ForeignKey(Donacion, on_delete=models.CASCADE, null=True)
    #programa = models.ForeignKey(Programa, models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '{}'.format(self.descripcion )

    class Meta:
        
        verbose_name = "Producto"
        verbose_name_plural = "Productos"


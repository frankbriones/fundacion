from django.db import models
from random import choice
from django.urls.base import reverse

from django.db.models.deletion import CASCADE

from persona.models import Profile, Persona
from _datetime import datetime
from donacion.models import Producto, Donacion, Tipo

# Create your models here.

class Evento(models.Model):
    ESTADO_ACTIVO = 0
    ESTADO_INACTIVO = 1
    ESTADO_CHOICES = {
            (ESTADO_ACTIVO, 'Activo'),
            (ESTADO_INACTIVO, 'Inactivo')
        }   
    nombre = models.CharField(max_length=300, null=True)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True)
    estado = models.SmallIntegerField(choices = ESTADO_CHOICES, null = True)
    imagen = models.ImageField(
        upload_to='programa/pictures',
        null=True, 
        #validators=[validate_file_extension],
        blank=True
    )



    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    
        
    def __str__(self):
        return '%s'%(self.nombre)
    class Meta:
        
        verbose_name = "Programa"
        verbose_name_plural = "Programas"
    
    
class Programa(models.Model):
    TIPO_ACTIVO = 0
    TIPO_INACTIVO = 1
    TIPO_CHOICES = {
             (TIPO_ACTIVO, 'Activo'),
             (TIPO_INACTIVO, 'Inactivo'),             
         }

    
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, null=True)
    nombre = models.CharField(max_length=300, null=True)
    fecha_programa = models.DateField(unique=True, null=True)
    fecha_culminacion = models.DateField(null=True)
    direccion = models.CharField(max_length=400, null=True)
    #capacitador, de las personas en la tabla voluntarios, es decir ya tenemos datos previos de la persona
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True)
    estado = models.SmallIntegerField(choices = TIPO_CHOICES, null=True, default=True)
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)
    
    
    def __str__(self):
        return '{}'.format(self.nombre)
    class Meta:
        
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"

    def get_absolute_url(self):
        return reverse("programa:edita" , kwargs={'programa_id': self.pk})



from django.conf import settings
class Detalle(models.Model):
    cant = models.PositiveIntegerField(null=True) 
    programa = models.ForeignKey(Programa, on_delete=models.CASCADE, null=True)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE, null=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE, null=True)
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedido')
    created = models.DateField(auto_now_add=True, null=True)
    modified = models.DateTimeField(auto_now=True, null=True)



    def __str__(self):
        return '{}/ {}/ {} '.format(self.producto.descripcion, self.tipo, self.cant)
    class Meta:
        
        verbose_name = "Detalle de Evento"
        verbose_name_plural = "Detalles del Evento"




# from django.conf import settings
# class Pedido(models.Model):
#     ESTADO_ACTIVO = 0
#     ESTADO_INACTIVO = 1
#     ESTADO_CHOICES = {
#             (ESTADO_ACTIVO, 'Activo'),
#             (ESTADO_INACTIVO, 'Inactivo')
#         }   
    
#     usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='pedido')
#     estado = models.SmallIntegerField(choices = ESTADO_CHOICES, null = True, default=0)
#     created = models.DateField(auto_now_add=True, null=True)
#     modified = models.DateTimeField(auto_now=True, null=True)
    
        
#     def __str__(self):
#         return '%s'%(self.nombre)
#     class Meta:
        
#         verbose_name = "Programa"
#         verbose_name_plural = "Programas"
#-*- coding: UTF-8 -*-
from django.db import models
from persona.models import Persona, Tipo_persona
from random import choice
from _datetime import datetime
from django.db.models.deletion import CASCADE

from django.urls.base import reverse, reverse_lazy


from django.contrib.auth.models import User, AbstractUser, BaseUserManager

# Create your models here.


class Horario(models.Model):
    hora = models.CharField(max_length=100,  null=True, blank=True)
    
    def __str__(self):
        return '{}'.format(self.hora)

class Categoria_taller(models.Model):
    name = models.CharField(max_length=100,  null=True)
    
    def __str__(self):
        return '{}'.format(self.name)





class ActiveManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset()



class Taller(models.Model):

   

    CATEGORIA_ARTESANIAS = 0
    CATEGORIA_BELLEZA = 1
    CATEGORIA_REPOSTERIA = 2
    CATEGORIA_SALUD = 3
    CATEGORIA_TECNOLOGIA = 4
    CATEGORIA_CHOICES = (
            (CATEGORIA_ARTESANIAS, 'ARTESANIAS'),
            (CATEGORIA_BELLEZA, 'BELLEZA'),
            (CATEGORIA_REPOSTERIA, 'REPOSTERIA'),
            (CATEGORIA_SALUD, 'SALUD'),
           (CATEGORIA_TECNOLOGIA, 'TECNOLOGIA'),
        )


    TIPO_ACTIVO = 0
    TIPO_INACTIVO = 1
    TIPO_CHOICES = {
             (TIPO_ACTIVO, 'Activo'),
             (TIPO_INACTIVO, 'Inactivo'),             
    }
    descripcion = models.CharField(max_length=50, null=True)
    detalle = models.CharField(max_length=800, null=True)
    estado = models.SmallIntegerField(choices = TIPO_CHOICES, default = 0)
    #tallersista
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, null=True)
    fecha_inicio = models.DateField( null=True)
    fecha_culmina = models.DateField(null=True)
    categoria = models.SmallIntegerField(choices = CATEGORIA_CHOICES, default = 0)
    created = models.DateField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    limite = models.PositiveSmallIntegerField(null=True, blank=True, default=8)
    # inscritos = models.PositiveSmallIntegerField(null=True, blank=True, default=0)
    precio = models.PositiveSmallIntegerField(blank=True, default= 0)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE, null=True, related_name='tracks')
    
    active = models.BooleanField(default=True)
    active_manager = ActiveManager()
    objects = models.Manager()
#    categoria = models.ForeignKey(Categoria_taller, on_delete=models.CASCADE, null=True)

    class Meta:
        app_label = 'talleres'

    def get_absolute_url(self):
        return reverse("talleres:edit" , kwargs={'taller_id': self.pk})
    
    def __str__(self):
        return '{}'.format(self.descripcion)

    




from persona.models import Profile



from django.utils.translation import ugettext_lazy as _

from django.conf import settings


class Estudiante(models.Model):
    class Meta:
        permissions = [
        ("add_persona", "Can change the status of tasks"),
    ]



    usuario = models.OneToOneField(Profile, null=True, blank=True, related_name='usuar', on_delete=models.CASCADE)
    contador_taller = models.IntegerField(null=True)

    def as_dict(self):
        dic =self.__dict__
        dic['email']= self.usuario.email
        return dic

    def get_absolute_url(self):
        return reverse("talleres:detalle_estudiante" , kwargs={'estudiante_id': self.pk})

    def __str__(self):
        return '{} {}'.format(self.usuario.nombres, self.usuario.apellidos) 









class Estado_Estudiante_taller(models.Model):
    CATEGORIA_CURSANDO = 0
    CATEGORIA_APROBADO = 1
    CATEGORIA_ABANDONO = 2

    CATEGORIA_CHOICES = (
            (CATEGORIA_CURSANDO, 'CURSANDO'),
            (CATEGORIA_APROBADO, 'APROBADO'),
            (CATEGORIA_ABANDONO, 'ABANDONO'),

        )

    
    CANCELAR_NO_PAGADO = 1
    CANCELAR_PAGADO = 0
    

    CANCELAR_CHOICES = (
            (CATEGORIA_CURSANDO, 'PAGADO'),
            (CATEGORIA_APROBADO, 'NO CANCELADO'),
            

        )
    estado = models.SmallIntegerField(choices = CATEGORIA_CHOICES)
    pago = models.SmallIntegerField(choices = CANCELAR_CHOICES, default=1)
    taller = models.ForeignKey(Taller, related_name='Estado_Estudiante_taller', on_delete=models.CASCADE, null=True, blank=True)
    estudiante = models.ForeignKey(Estudiante, related_name='Estado_Estudiante_taller', on_delete=models.CASCADE, null=True, blank=True)
    inscrito = models.DateField(auto_now_add=True)
    created = models.DateField(auto_now_add=True)
    class Meta:
        
        verbose_name = "estado estudiantil"
        verbose_name_plural = "Estado Estudiante"


    def __str__(self):
        return '{}, {}'.format(self.estudiante,self.estado)













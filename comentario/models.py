from django.db import models
from django.conf import settings
# Create your models here.



class Comentario(models.Model):
	TIPO_ACTIVO = 0
	TIPO_INACTIVO = 1
	TIPO_CHOICES = {
		(TIPO_ACTIVO, 'Activo'),
		(TIPO_INACTIVO, 'Inactivo'),
		}
	created = models.DateField(auto_now_add=True, null=True)
	modified = models.DateTimeField(auto_now=True, null=True)
	contenido = models.CharField(max_length = 50)
	autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comentarios')
	estado = models.SmallIntegerField(choices = TIPO_CHOICES, null=True, default=TIPO_ACTIVO, blank=True)

	def __str__(self):
		return "{}".format(self.autor)
	class Meta:
		ordering = ['created']




from django import forms
from comentario.models import Comentario
from collections import Counter

class ComentarioForm(forms.ModelForm):
	class Meta:
		model = Comentario
		fields = {'contenido'}
	def clean_contenido (self):
		contenido = self.cleaned_data.get("contenido")

		contador = len(contenido)
		print (contador)
		if contador >= 30 :
			raise forms.ValidationError("Maximo de Caracteres para los comentarios es de 30, tenemos({})".format(contador))
		return contenido
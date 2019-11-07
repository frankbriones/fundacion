from django import forms
from .models import Taller, Estudiante, Estado_Estudiante_taller, Horario
from django.forms.widgets import  DateInput, TextInput, Textarea, SelectMultiple, NumberInput
from django.contrib.admin import widgets
from persona.models import Persona, Tipo_persona
from datetime import datetime, date, time, timedelta
import calendar
#class EstudianteForm(forms.ModelForm):
#	class Meta:
#		model = Estudiante
#		fields = ('nombres', 'apellido_paterno', 'apellido_materno', 'correo',  'estado', 'taller')


####     ESTE CODIGO ES SIMILAR AL DE ABAJO ,
#### YA QUE REALIXAN CASI LO MISMO QUE SERIA ALMACENAR UN  TALLER PER AQUI SE USA FORMS.FORM



#class TallerForm(forms.Form):

#	descripcion = forms.CharField(max_length=50, label=u'Titulo',
#		widget=forms.TextInput(attrs={'placeholder':'Titulo'}))

#	detalle = forms.CharField(max_length=150)
#
#	persona = forms.ModelChoiceField(queryset=Persona.objects.filter(tipo__tipo__startswith = 'Capacitador'))

#	fecha_inicio = forms.DateField( label=u'Fecha Inicio')

#	fecha_culmina = forms.DateField( label=u'Fecha Culmina')

#	categoria = forms.ChoiceField(choices=Taller.CATEGORIA_CHOICES, required=True)

#	def clean_fecha_culmina (self):
#		fecha_culmina = self.cleaned_data.get("fecha_culmina")
#		fecha_inicio = self.cleaned_data.get("fecha_inicio")
#		if fecha_culmina < fecha_inicio:
#			raise forms.ValidationError("Verifique la fecha final, no puede ser menor a la primera fecha ingresada.")
#		return fecha_culmina
#
#	def save(self):
#		cleaned_data = super(TallerForm, self).clean()
#		taller = Taller()
#		taller.descripcion = cleaned_data['descripcion']
#		taller.persona = cleaned_data['persona']
#		taller.fecha_inicio = cleaned_data['fecha_inicio']
#		taller.fecha_culmina = cleaned_data['fecha_culmina']
#		taller.categoria = cleaned_data['categoria']
#		taller.detalle = cleaned_data['detalle']
#		taller.estado = 1
#		taller.save()
#		return taller





class TallerForm(forms.ModelForm):
	# Como paso inicial en esta funcion se le dice al formulario que en el campo persona traiga a los que sean de tipo capacitador que por 
	#choices seria el numero 0
	def __init__( self, *args, **kwargs ):
		super( TallerForm, self ).__init__( *args, **kwargs )
		self.fields['persona'] = forms.ModelChoiceField(queryset = Persona.objects.filter(tipo__tipo__startswith = 'Capacitador').filter(estado = 0))
		#if self.fields['fecha_culmina'] < self.fecha_inicio['fecha_inicio']:

	class Meta:
		model = Taller
		fields = ('categoria',
			'persona',
			'descripcion',
			'detalle',
			'fecha_inicio',
			'fecha_culmina',
			'horario',
			'precio',
			'limite',
			)
		widgets = {
			'persona': forms.TextInput({ 'placeholder': 'Capacitador del Taller'}),
            'descripcion':  forms.TextInput({ 'placeholder': 'Titulo de Taller'}),
            'detalle':  forms.TextInput({ 'placeholder': 'Detalla los acontecimientos del evento, No mayor a 100 palabras'}),
            'fecha_inicio':  forms.TextInput({'placeholder': 'dd/mm/aaaa'}),
            'fecha_culmina':  forms.TextInput({'placeholder': 'dd/mm/aaaa'}),
            'limite':  forms.NumberInput({'placeholder': 'limite de estudiantes..'}),
           
        }   
		labels = {
         'fecha_inicio': 'Fecha de Inicio', 
         'fecha_culmina': 'Fecha que Culmina',
         'descripcion': 'Titulo',
         'persona': 'PERSONAS',
		 'horario': 'Horario',
		 'limite': 'Limite de Estudiantes'
         }


	def clean_fecha_inicio(self):
		
		fecha_inicio = self.cleaned_data['fecha_inicio']
		formato_fecha = "%Y-%m-%d"
		fecha_limite = (datetime.strptime("2000-01-01", formato_fecha)).date()
		
		if fecha_inicio < fecha_limite:
			raise forms.ValidationError("Verifique la fecha inicial. no puede ser menor a 2000/01/01")
		
		
		return fecha_inicio


	def clean_horario(self):
		fecha_1 = self.cleaned_data.get("fecha_inicio")
		horario = self.cleaned_data['horario']
		fecha_inicio_taken = Taller.objects.filter(fecha_inicio=fecha_1)\
			.filter(horario=horario).exists()
		horario_taken = Horario.objects.filter(hora=horario)
		for hour in horario_taken:
			print(horario_taken)
			if fecha_inicio_taken:
				raise forms.ValidationError("Fecha: {} - Horario: {}. Ya existe,redefina alguno de los dos campos".format(fecha_1, hour.hora))
				print(horario_taken)
		
		return horario


	def clean_precio(self):
		precio = self.cleaned_data['precio']
		if precio is None:
			precio = 0
			print(precio)
		return precio
	
	

	

	def clean_fecha_culmina (self):
		fecha_culmina = self.cleaned_data.get("fecha_culmina")
		fecha_i = self.cleaned_data.get("fecha_inicio")
		try:
			
			if fecha_i > fecha_culmina:
				raise forms.ValidationError("Verifique la fecha final, no puede ser menor a la primera fecha ingresada.")
			
			return fecha_culmina
		except TypeError:
					raise forms.ValidationError("verfique los datos")


	

from persona.models import Persona, Profile


class EstudianteForm(forms.Form):

	usuario = forms.CharField(max_length=150, widget=forms.EmailInput(attrs={'size':'30'}))
	contraseña = forms.CharField(max_length=13, widget=forms.PasswordInput(attrs={'size':'30'}))
	nombres = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'30'}))
	apellidos = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'size':'30'}))
	celular = forms.CharField(max_length=10, widget=forms.NumberInput(attrs={'size':'30'}))
	#imagen = forms.ImageField(required=False)

	#usuario = forms.ModelChoiceField(queryset=Profile.objects.all())
	#estado = forms.ChoiceField(choices=Estudiante.TIPO_CHOICES)
	#taller = forms.ModelMultipleChoiceField(queryset=Taller.objects.all(), widget = forms.SelectMultiple)
	#taller = forms.ModelChoiceField(queryset=Taller.objects.all(), widget = forms.SelectMultiple)


	def clean_usuario(self):
		if self.cleaned_data['usuario']:
			usuario = Profile.objects.filter(email = self.cleaned_data['usuario'])
			if len(usuario) > 0:
				raise forms.ValidationError("El usuario ya existe, cambielo")
		return self.cleaned_data['usuario']
       



	def save(self, estudiante = None):
		cleaned_data = super(EstudianteForm, self).clean()
		if estudiante is None:
			usuario = Profile()
			usuario.email = cleaned_data['usuario']
			usuario.set_password(cleaned_data['contraseña'])
			usuario.nombres = cleaned_data['nombres']
			usuario.apellidos = cleaned_data['apellidos']
			usuario.celular = cleaned_data['celular']
			usuario.is_staff = False
			usuario.save()


			estudiante = Estudiante()
			estudiante.usuario = usuario
			#estudiante.estado = cleaned_data['estado']
			estudiante.save()
			#estudiante.taller = cleaned_data['taller']
			#estudiante.save()
		else:
			#estudiante.taller = cleaned_data['taller']
			#estudiante.save()
			estudiante.usuario.email = cleaned_data['usuario']
			estudiante.usuario.save()
			return estudiante



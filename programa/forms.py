
from donacion.models import Donacion, Producto, Tipo, Categoria
from programa.models import Programa, Detalle,Evento
from persona.models import Persona
from django.forms.widgets import  RadioSelect, DateInput, TextInput, SelectMultiple, Textarea, NumberInput, CheckboxSelectMultiple
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets
from datetime import datetime
import time




from django.utils.translation import ugettext as _, ugettext_noop as _noop



#https://docs.djangoproject.com/en/2.2/ref/forms/validation/
class DetalleForm(forms.Form):
    


    tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(),empty_label="--Escoger tipo--",
        widget=forms.Select(attrs={'placeholder':'Tipo', 'onChange':'getCategoria(this.value);'}))

    categoria = forms.ModelChoiceField(queryset=Categoria.objects.none(),empty_label="--Escoger Categoria--",
        widget=forms.Select(attrs={'placeholder':'Categoria', 'onChange':'getProducto(this.value);'}))

    producto = forms.ModelChoiceField(queryset=Producto.objects.none(),empty_label="---Escoger un producto---",
         widget=forms.Select(attrs={'placeholder':'Produtos'}))


    cant = forms.IntegerField(required=True, label=u'Cantidad', min_value=1)

    def clean_cant(self):
        cant = self.cleaned_data.get("cant")
        producto = self.cleaned_data.get("producto")

        if cant > producto.stock:
            #self.fields['cant'] = forms.IntegerField(max_value=producto.stock)
            raise forms.ValidationError(
                _('Asegurese que este valor sea menor o igual a : %(value)s '),
                params={'value': producto.stock}
                )

        return cant



    def modificarQuerySet(self, tipo_id, categoria_id):
        if tipo_id not in ('', None):
            categorias = Categoria.objects.filter(tipo__id = tipo_id)
            self.fields['categoria'].queryset = categorias
        if categoria_id not in ('', None):
            productos = Producto.objects.filter(categoria__id = categoria_id).filter(estado=0) 
            self.fields['producto'].queryset = productos

#        for producto in productos:
#            self.fields['cant'] = forms.IntegerField(max_value=producto.stock)






class ProgramaForm(forms.ModelForm):
    def __init__( self, *args, **kwargs ):
        super( ProgramaForm, self ).__init__( *args, **kwargs )
        self.fields['evento'] = forms.ModelChoiceField(queryset = Evento.objects.filter(estado=0).order_by('nombre'))
    class Meta:
        model = Programa
        fields = '__all__'

        labels = {
            'evento': 'Programa',
            'nombre': 'Descripcion del Evento',
            'persona': 'Ayudante',
            'fecha_programa': 'Fecha que Realiza',
            'fecha_culminacion': 'Fecha que Culmina '
        }

        widgets = {
            #'plazas_trabajo': CheckboxSelectMultiple()
            'nombre': Textarea(attrs={'cols': 5, 'rows': 3}),
            'fecha_programa':  forms.TextInput(attrs={"class": "form-control",  'placeholder': 'dd/mm/aaaa'}),
            'fecha_culminacion':  TextInput(attrs={"class": "form-control",  'placeholder': 'dd/mm/aaaa'})

        }


    

    def clean_fecha_culminacion (self):
        fecha_culminacion = self.cleaned_data.get("fecha_culminacion")
        fecha_programa = self.cleaned_data.get("fecha_programa")
        if fecha_culminacion < fecha_programa:
            raise forms.ValidationError("No puede ser menor a la fecha en que empieza.")
            print(fecha_culminacion)


        return fecha_culminacion



#class ProgramaForm(forms.Form):
#        evento = forms.CharField(min_length=4, max_length=50)
#        nombre = forms.CharField(max_length= 300)
#        fecha_programa = forms.CharField(
#        min_length=6,
#        max_length=70,
#        widget=forms.DateInput(attrs={ 'type':'date', 'class':'class-form'})
#        )
#        fecha_culminacion = forms.CharField(
#        min_length=6,
#        max_length=70,
#        widget=forms.DateInput(attrs={ 'type':'date'})
#        )
#        direccion = forms.CharField(max_length= 300)
#        persona = forms.ModelMultipleChoiceField( queryset = Persona.objects.all(), widget= forms.SelectMultiple)
#        tipo = forms.ModelMultipleChoiceField( queryset = Tipo.objects.all())
#        producto = forms.ModelMultipleChoiceField( queryset = Producto.objects.all(), widget= forms.SelectMultiple)
#        cant = forms.CharField(
#        widget=forms.DateInput(attrs={ 'type':'number'}
#        ))
        



class EventoForm(forms.ModelForm):
    class Meta:
        model = Evento
        fields = {'nombre','persona',  'estado'}
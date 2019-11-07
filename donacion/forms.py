from donacion.models import Donacion, Producto, Tipo, Categoria
from programa.models import Programa, Detalle
from persona.models import Persona
from django.forms.widgets import  RadioSelect, DateInput, TextInput, SelectMultiple, Textarea, NumberInput, CheckboxSelectMultiple
from django.forms import ModelForm
from django import forms
from django.contrib.admin import widgets
from datetime import datetime
import time
#from django.contrib.admin.widgets import AdminTextareaWidget





#FORMULARIO DONACIONNN


# class DonacionForm(forms.Form):
#     persona = forms.ModelChoiceField(queryset=Persona.objects.filter(estado=0), label='Donador')

#     def __init__(self, *args, **kwargs):
#         super(DonacionForm, self).__init__(*args, **kwargs)
#         for field in iter(self.fields):
#             self.fields[field].widget.attrs.update({
#                 'class': 'form-control'
#                 })

#     def save(self):
#         cleaned_data = super(DonacionForm, self).clean()
#         donacion = Donacion()
#         donacion.persona =cleaned_data['persona']
#         donacion.save()
#         return donacion

class DonacionForm(forms.ModelForm):
    class Meta:
        model = Donacion
        fields = {'persona'}






# class ProductoForm(forms.ModelForm):
#     class Meta:
#         model = Producto
#         fields = {'tipo', 'categoria', 'descripcion',  'cantidad', 'fecha_expiracion'}
#         widgets = {
#             #'tipo': CheckboxSelectMultiple(),
#             'descripcion': forms.TextInput({'placeholder': 'Detalla el nombre del producto'}),
                           
#             'fecha_expiracion': forms.DateInput({'placeholder': 'dd/mm/aaaa'}),
#             'cantidad': forms.NumberInput({"type": "number"}),
#             }
#     def clean_fecha_expiracion (self):
#         fecha_actual = datetime.now().isoformat()
#         fecha_expiracion = self.cleaned_data.get("fecha_expiracion").isoformat()
#         if fecha_expiracion < fecha_actual:
#             raise forms.ValidationError("No puede ser menor a la fecha actual")
        
#         return fecha_expiracion




# from django.forms.models import inlineformset_factory

# ProductoFormSet = inlineformset_factory(Donacion, Producto, form=ProductoForm, extra=2)

class ProductoForm(forms.Form):
    tipo = forms.ModelChoiceField(queryset=Tipo.objects.all(),empty_label="--Escoger tipo--",
        widget=forms.Select(attrs={'placeholder':'Tipo', 'onChange':'getCategoria(this.value);'}))

    categoria = forms.ModelChoiceField(queryset=Categoria.objects.none(),empty_label="--Escoger Categoria--",
        widget=forms.Select(attrs={'placeholder':'Categoria'}))

    descripcion = forms.CharField(required=True, label=u'Descripcion')
    fecha_expiracion = forms.CharField(required=False, label=u'Fecha Expiracion', 
        widget=forms.DateInput(attrs={'placeholder':'12-12-2020', 'value':'2020-12-12'}))
    cantidad =  forms.IntegerField(required=True, label=u'Cantidad')

    def modificarQuerySet(self, tipo_id):
        if tipo_id not in ('', None):
            categorias = Categoria.objects.filter(tipo__id = tipo_id)
            self.fields['categoria'].queryset = categorias


    def clean_fecha_expiracion (self):
        fecha_actual = datetime.now().date()
        print(fecha_actual)
        fecha_expiracion = self.cleaned_data.get("fecha_expiracion")
        print(fecha_expiracion)
        if fecha_expiracion <= fecha_actual.isoformat():
            raise forms.ValidationError("La fecha de expiracion no puede ser menor o igual a la fecha de hoy.")
        return fecha_expiracion
        



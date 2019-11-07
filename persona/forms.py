from persona.models import Persona, Profile
#from django.forms.widgets import SelectMultiple
from django.forms import ModelForm
from django import forms
from django.forms.widgets import TextInput, EmailInput, FileInput,  NumberInput, Textarea
import math

from django.utils.translation import ugettext as _, ugettext_noop as _noop
from datetime import datetime, timedelta
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
import time

class UserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _('The two password fields didn’t match.'),
    }
    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Profile
        fields = ("email",)



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self._meta.model.USERNAME_FIELD in self.fields:
            self.fields[self._meta.model.USERNAME_FIELD].widget.attrs.update({
                'autocomplete': 'username',
                'autofocus': True,
            })

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError('Password no coinciden.')
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password, self.instance)
            except forms.ValidationError as error:
                self.add_error('password2', error)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        #creao un usuario inactivo
        user.is_active = 0
        if commit:
            user.save()
        return user































class PersonaForm(forms.ModelForm):
    celular = forms.CharField(max_length=10)
    convencional = forms.CharField(max_length=9)
    cedula = forms.CharField(max_length=10)

    class Meta:
        model = Persona
        fields = {'cedula', 'nombres', 'apellido_paterno', 'apellido_materno', 'sexo', 'fecha_nacimiento', 'convencional', 'celular', 'correo',
        'direccion', 'estado', 'tipo', 'imagen'
        }

        widgets = {
            'fecha_nacimiento':  forms.TextInput( { 'placeholder':'dd/mm/aaaa', 'type': 'date'}),
            'convencional':  forms.TextInput(attrs={ 'type':'number', 'placeholder': 'convencional'}),
            'celular':  forms.TextInput({ 'type':'number','placeholder': 'celular'}),
            'correo':  forms.TextInput({'placeholder': 'correo@domain.com'}),
            'cedula':  forms.TextInput({ 'placeholder': '10 digitos', 'type':'number'}),
            'nombres':  forms.TextInput(attrs={ 'type':'mail', 'placeholder': 'Primer y Segundo Nombre'}),
            'direccion':  forms.TextInput({'placeholder': 'Especifica el lugar de vivienda'}),
            #'imagen': forms.FileInput(attrs={ 'placeholder': 'Imagenes no mayores a 2.5 MB'})

        }
    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        ##validadciones
        if len(cedula) != 10:
            raise forms.ValidationError("numero de cedula incompleto/ longitud 10 numeros")
        
        numeros = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, numeros))
        suma = int(cedula[9]) == 10 - int(str(suma)[-1:])
        if suma is False:
            raise forms.ValidationError("Numero de cedula invalido.")
        
        return cedula

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get("fecha_nacimiento")
        ##validadciones
        if (fecha_nacimiento) >= (datetime.now().date() - timedelta(days=5500)):
            raise forms.ValidationError("Ingrese una Fecha Valida.")
        return fecha_nacimiento


class VoluntarioForm(forms.ModelForm):
    celular = forms.CharField(max_length=10)
    convencional = forms.CharField(max_length=9)

    class Meta:
        model = Persona
        fields = {'cedula', 'nombres', 'apellido_paterno', 'apellido_materno', 'sexo', 'fecha_nacimiento', 'convencional', 'celular', 'correo',
        'direccion', 'estado', 'imagen'
        }

        widgets = {
            'fecha_nacimiento':  forms.TextInput( { 'placeholder':'dd/mm/aaaa', 'type': 'date'}),
            'convencional':  forms.TextInput(attrs={ 'type':'number', 'placeholder': 'convencional'}),
            'celular':  forms.TextInput({ 'type':'number','placeholder': 'celular'}),
            'correo':  forms.TextInput({'placeholder': 'correo@domain.com'}),
            'cedula':  forms.TextInput({ 'placeholder': '10 digitos', 'type':'number'}),
            'nombres':  forms.TextInput(attrs={ 'type':'mail', 'placeholder': 'Primer y Segundo Nombre'}),
            'direccion':  forms.TextInput({'placeholder': 'Especifica el lugar de vivienda'}),
            #'imagen': forms.FileInput(attrs={ 'placeholder': 'Imagenes no mayores a 2.5 MB'})

        }   






#http://www.ecualug.org/?q=2010/06/25/forums/validaci%C3%B3n_de_cedula_de_ecuador
#validar la longitud y si es real o no la cedula ingresada'
    def clean_cedula(self):
        cedula = self.cleaned_data.get("cedula")
        ##validadciones
        if len(cedula) != 10:
            raise forms.ValidationError("numero de cedula incompleto/ longitud 10 numeros")
        
        numeros = [ int(cedula[x]) * (2 - x % 2) for x in range(9) ]
        suma = sum(map(lambda x: x > 9 and x - 9 or x, numeros))
        suma = int(cedula[9]) == 10 - int(str(suma)[-1:])
        if suma is False:
            raise forms.ValidationError("Numero de cedula invalido.")
        
        return cedula

    def clean_fecha_nacimiento(self):
        fecha_nacimiento = self.cleaned_data.get("fecha_nacimiento")
        ##validadciones
        if (fecha_nacimiento) >= (datetime.now().date() - timedelta(days=5500)):
            raise forms.ValidationError("Ingrese una Fecha Valida.")
        return fecha_nacimiento
        

        






class ContactoForm(forms.Form):
    correo =  forms.EmailField()
    mensaje = forms.CharField(widget=forms.Textarea(attrs={"rows":5, "cols":20}))

    def clean_correo(self):
        correo = self.cleaned_data['correo']
        if not 'gmail.com' in correo:
            raise forms.ValidationError("Por favor utilize un correo con extension gmail.com")
        return correo






from django.conf import settings
from datetime import date, timedelta, datetime
import time
import jwt
from django.template.loader import render_to_string

from django.core.mail import EmailMultiAlternatives

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = { 'email', 'nombres', 'apellidos', 'celular','imagen', 'groups'}


        widgets = {

            'celular':  TextInput(attrs={ 'type':'tel', 'placeholder': 'Celular'}),
            'email': TextInput(attrs={ 'type':'email'}),
            #'cedula':  TextInput(attrs={ 'type':'number', 'placeholder': '10 digitos'}),
            'nombres':  TextInput(attrs={ 'type':'mail', 'placeholder': 'Primer y Segundo Nombre'}),
            'apellidos':  TextInput(attrs={ 'type':'text'}),
            #   'imagen': FileInput(attrs={'type':'file'})

        }

# Models
from django.contrib.auth.models import User


from django.utils.translation import ugettext as _, ugettext_noop as _noop





# class SignupForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = { 'email', 'password', 'nombres', 'apellidos', 'celular'}




class SignupForm(forms.Form):
   """Sign up form."""
   nombres = forms.CharField(min_length=2, max_length=50, label= 'Nombres')
   apellidos = forms.CharField(min_length=2, max_length=50, label= 'Apellidos')
   email = forms.CharField(
       min_length=6,
       max_length=70,
       widget=forms.EmailInput()
  )
   password = forms.CharField(
       max_length=70,
       widget=forms.PasswordInput(),
       help_text=password_validation.password_validators_help_text_html(),
   )
   password_confirmation = forms.CharField(
       max_length=70,
       widget=forms.PasswordInput(),
       label='Confirmacion de Password'
   )

   celular = forms.CharField(
       widget=forms.TextInput(),
       max_length=10,
       label='Movil'
   )
      


   def clean_email(self):
       """Username must be unique."""
       email = self.cleaned_data['email']
       username = email
       email_taken = Profile.objects.filter(email=email).exists()
       if email_taken:
           raise forms.ValidationError('Correo se encuentra en uso.')
       return email

   def clean(self):
       """Verify password confirmation match."""
       data = super().clean()

       password = self.cleaned_data['password']
       password_confirmation = self.cleaned_data['password_confirmation']

       if password != password_confirmation:
           raise forms.ValidationError(
               _('password no coinciden')

               )
       if password:
            try:
                password_validation.validate_password(password)
            except forms.ValidationError as error:
                self.add_error('password_confirmation', error)
       return data


   def save(self):	
       """Create user and profile."""
       data = self.cleaned_data
       data.pop('password_confirmation')

       profile = Profile.objects.create_user(**data)
       from talleres.models import Estudiante
       estudiante = Estudiante.objects.create(usuario=profile)
       self.send_confirmation_email(profile)
       profile.save()
   def send_confirmation_email(self, user):
      user = Profile.objects.get(pk=user.id)
      verification_token = self.genera_token_verificado(user)
      subject  = 'Bienvenido, {} verifica tu cuenta.'.format(user.email)
      from_email = 'Tacita Caliente <primer1grupo@gmail.com>'
      content = render_to_string(
        'emails/user/account_verification.html',
        {'token': verification_token, 'user': user}
        )
      msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
      msg.attach_alternative(content, "text/html")
      msg.send()
   def genera_token_verificado(self, user):
    # return'abc'
      print(user)
      exp_date = datetime.now() + timedelta(days=3)
      payload = {
      'user': user.id,
      'exp': int(exp_date.timestamp()),
      'type': 'email_confirmation'
      }
      token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
      return token.decode()

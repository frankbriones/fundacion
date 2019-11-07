# -*- coding: utf-8 -*-
from rest_framework import serializers
from django.contrib.auth import authenticate, password_validation
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives


from rest_framework.validators import UniqueValidator


from rest_framework.authtoken.models import Token
from persona.models import UserManager, Profile

from persona.models import Persona
from programa.models import Evento


class PersonaSerializer(serializers.ModelSerializer):
	#encargado = serializers.StringRelatedField(many=False, source='nombres')
	class Meta:
		model = Persona
		fields = (
			'id',
			'nombres',
			'imagen',
			)
	def get_imagen(self, persona):
		request = self.context.get('request')
		imagen = persona.imagen.url		
		return request.build_absolute_uri(imagen)



class ProgramaSerializer(serializers.ModelSerializer):
	#encargado = serializers.StringRelatedField(many=False, source='nombres')
	class Meta:
		model = Evento
		fields = (
			'id',
			'nombre',
			'imagen',
			)
	def get_imagen(self, programa):
		request = self.context.get('request')
		imagen = programa.imagen.url		
		return request.build_absolute_uri(imagen)		




		

class EventoSerializer(serializers.Serializer):
	nombre = serializers.CharField()
	direccion = serializers.CharField()
	fecha_programa = serializers.DateField()
	fecha_culminacion = serializers.DateField()
	programa = ProgramaSerializer(many=False,source='evento')
	encargado = PersonaSerializer(many=False, source='persona')



class UserModelSerializer(serializers.ModelSerializer):
	"""user model serializer"""
	# email = serializers.ReadOnlyField()
	# nombres = serializers.ReadOnlyField()
	# apellidos = serializers.ReadOnlyField()
	# celular = serializers.ReadOnlyField()
	class Meta:
		model = Profile
		fields = (
			'email',
			'nombres',
			'apellidos',
			'celular',
			'imagen',


			)
	def get_imagen(self, persona):
		request = self.context.get('request')
		imagen = persona.imagen.url		
		return request.build_absolute_uri(imagen)
		

from django.conf import settings
from datetime import date, timedelta, datetime
import time
import jwt

class UserSignUpSerializer(serializers.Serializer):

	"""User signup serializers"""
	email = serializers.EmailField(
		validators=[
		UniqueValidator(queryset=	Profile.objects.all())]
		)
	nombres = serializers.CharField(max_length=15)
	password = serializers.CharField(min_length=8, max_length=64)
	password_confirmation = serializers.CharField(min_length=8, max_length=64)

	def validate(self, data):
		passwd = data['password']
		passwd_conf = data['password_confirmation']
		if passwd != passwd_conf:
			raise serializers.ValidationError("passwords no coinciden :/ ")
		"""validar la contrasenia"""
		password_validation.validate_password(passwd)
		return data
	
	def create(self, data):

		"""creacion de user y perfil"""
		data.pop('password_confirmation')
		
		"""crear un staff activo y una clave con hash, 
		caso contrario crea el usuario pero 
		staff = False y el passsword no la reconoce para el acceso
		y asi el usuario se paria el
		 middleware de perfilcompleto
		"""
		#profile = Profile.objects.create_user(**data)
		
		user = Profile.objects.create_user(**data)
		self.send_confirmation_email(user)

		return user

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


		#print("Correo Enviado")

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






class UserLoginSerializer(serializers.Serializer):
	email = serializers.EmailField()
	password = serializers.CharField(min_length=8, max_length=64)

	def validate(self, data):
		user = authenticate(username=data['email'], password=data['password'])
		if not user:
			raise serializers.ValidationError('Credenciales Invalidas')
		if user.is_active == False:
			raise serializers.ValidationError('Cuenta no esta Activa :(')
		self.context['user'] = user
		print(data)
		return(data)

	def create(self, data):
		"""generar o recuperar nuevo token"""

		token, created = Token.objects.get_or_create(user = self.context['user'])
		return self.context['user'], token.key





class AccountVerificationSerializer(serializers.Serializer):
    """Account verification serializer."""

    token = serializers.CharField()

    def validate_token(self, data):
        """Verify token is valid."""
        try:
            payload = jwt.decode(data, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise serializers.ValidationError('Link de Verificacion expiro.')
        except jwt.PyJWTError:
            raise serializers.ValidationError('Token Invalido')
        if payload['type'] != 'email_confirmation':
            raise serializers.ValidationError('Invalid token')

        self.context['payload'] = payload
        
        return data

    def save(self):
        """Update user's verified status."""
        payload = self.context['payload']
        #print(self.data)
        user = Profile.objects.get(pk=payload['user'])
        user.is_active = True
        user.save()
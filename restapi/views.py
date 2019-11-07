""" users views """




"""django_rest_framework"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from programa.models import Programa
from persona.models import Profile

from restapi.serializers import  (
	UserLoginSerializer,
	UserModelSerializer,
	UserSignUpSerializer,
	EventoSerializer,
	AccountVerificationSerializer


	) 


from rest_framework.decorators import  api_view
from rest_framework.response import  Response


@api_view(['GET'])
def list_eventos(request):
	from datetime import date
	fecha = date.today()
	eventos = Programa.objects.filter(estado=0)
	# for p in programas:
	# 	if p.fecha_programa < fecha:
	# 		p.estado = 1
	# 		p.save()
	serializer = EventoSerializer(eventos, many=True, context={'request': request})
	return Response(serializer.data)



class UserLoginAPIView(APIView):
	serializer_class = UserLoginSerializer
	
	# """user login api view"""

	# """crear un metodo post, 
	# por que tenemos una accion, en este caso haremos la creacion de un token
	# """
	def post(self, request, *args, **kwargs):
		""" Se encarga del http request"""
		serializer = UserLoginSerializer(data= request.data)
		serializer.is_valid(raise_exception=True)
		#user = serializer.validated_data['user']
		user, token = serializer.save()
		data = {
			'user': UserModelSerializer(user, context={'request': request}).data,
			'access_token': token,
			}
			
		return Response(data, status=status.HTTP_201_CREATED)

class UserSignupAPIView(APIView):
	serializer_class = UserSignUpSerializer


	def post(self, request, *args, **kwargs):
		""" Se encarga del http request"""
		serializer = UserSignUpSerializer(data= request.data)
		
		serializer.is_valid(raise_exception=True)
		user = serializer.save()
		
		data = {
			'user': UserModelSerializer(user).data,
			}			
		return Response(data, status=status.HTTP_201_CREATED)


import jwt
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
@api_view(['POST'])
def activar(request):

	try:
		serializer = AccountVerificationSerializer(data=request.data)		
		serializer.is_valid(raise_exception=True)
		serializer.save()
		data = {'message': 'Felicidades, Ahora puedes indagar en nuestra app!'}
		return Response(data, status=status.HTTP_200_OK)
	except Profile.DoesNotExist:
		data = {'message': 'token invalido, Usuario no existe!'}
		return Response(data, status=status.HTTP_400_BAD_REQUEST)

		
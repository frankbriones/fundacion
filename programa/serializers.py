""" 
programas serializers
"""


from rest_framework import serializers


from persona.models import Persona

class ProgramaSerializer(serializers.Serializer):
	nombre = serializers.CharField()
	direccion = serializers.CharField()
	fecha_programa = serializers.DateField()
	fecha_culminacion = serializers.DateField()
	evento = serializers.StringRelatedField(many=False)

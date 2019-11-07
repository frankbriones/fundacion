""" 
taller serializers
"""


from rest_framework import serializers
from talleres.models import Horario, Taller

from persona.models import Persona

class PersonaSerializer(serializers.ModelSerializer):
        class Meta:
            model = Persona
            fields = (
                'id',
                'nombres',
                'imagen',
            )

class TallerSerializer(serializers.ModelSerializer):
	# descripcion = serializers.CharField()
	# detalle = serializers.CharField()
	# fecha_inicio = serializers.DateField()
	# fecha_culmina = serializers.DateField()
	# precio = serializers.IntegerField()
	persona = PersonaSerializer(many=False)
	horario = serializers.StringRelatedField(
		many=False
	)
	class Meta:
		model = Taller
		fields=['descripcion', 'detalle', 'fecha_inicio', 'fecha_culmina', 'precio', 'horario', 'persona']
		


class CreateTallerSerializer(serializers.Serializer):

	descripcion = serializers.CharField(max_length=150)
	detalle = serializers.CharField(max_length=150)
	fecha_inicio = serializers.DateField()
	fecha_culmina = serializers.DateField()
	precio = serializers.IntegerField()





	
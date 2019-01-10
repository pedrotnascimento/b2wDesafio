from rest_framework import serializers
from starwars.models import Planet


class PlanetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Planet
        fields = ('id', 'name', 'climate', 'terrain')

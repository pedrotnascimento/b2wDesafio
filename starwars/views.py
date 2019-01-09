from starwars.models import Planet
from starwars.serializers import PlanetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class PlanetList(APIView):
    def get(self, request, format=None):
        planets = Planet.objects.all()
        # turn into primitive python object
        serializer = PlanetSerializer(planets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PlanetSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PlanetDetail(APIView):
    def get_object(self, pk):
        try:
            obj = Planet.objects.get(pk=pk)
            return obj
        except Planet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        planet = self.get_object(pk)
        serializer = PlanetSerializer(planet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        planet = self.get_object(pk)
        serializer = PlanetSerializer(planet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        planet = self.get_object(pk)
        planet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


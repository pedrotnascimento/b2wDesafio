from starwars.models import Planet
from starwars.serializers import PlanetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests


class PlanetList(APIView):
    def get(self, request, format=None):
        planets = Planet.objects.all()
        # turn into primitive python object
        serializer = PlanetSerializer(planets, many=True)

        # modify(add, change) data comming from the database
        planetAux = PlanetTransformData()
        for i, aux_dict in enumerate(serializer.data):
            serializer.data[i] = planetAux.transform(aux_dict)

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
        planetAux = PlanetTransformData()
        return Response(planetAux.transform(serializer.data))

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


class PlanetTransformData:
    def transform(self, obj):
        self.set_number_appearance(obj, obj["name"])
        return obj

    def set_number_appearance(self, obj, planet_name):
        obj["appearance_qnt"] = self.api_number_appearance(planet_name)

    def api_number_appearance(self, name):
        try:
            name = str(name)
            URL = "https://swapi.co/api/planets/?search=" + name
            r = requests.get(url=URL)
            data = r.json()
            if data["count"] == 0:
                return 0
            for p in data["results"]:
                if str(p["name"]).lower() == name.lower():
                    tam = len(p["films"])
                    return tam
            return 0
        except Exception:
            return 0

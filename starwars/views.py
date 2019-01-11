from starwars.models import Planet
from starwars.serializers import PlanetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger, InvalidPage
import requests as requestsMod


class PlanetList(APIView):
    PAGINATION_COUNT = 10
    # useful in test checking
    PAGE_ERR_MSG_COUNT_ARG = "Error: passing count parameter"
    PAGE_ERR_MSG_LOW_0 = "Error: count argument must to be integer higher than 0"

    def get(self, request, format=None):
        planets = Planet.objects.all()

        # check search filter
        if "search" in request.query_params:
            planets = self.planet_by_name(request, planets)

        # check pagination
        if "page" in request.query_params:
            try:
                if "count" in request.query_params:
                    self.set_count(request.query_params["count"])

                planets = self.get_pages(planets, request.query_params["page"])
            except EmptyPage:
                planets = self.get_pages(planets, 1)
            except InvalidPage as e:
                return Response(str(e))
            except PageNotAnInteger as e:
                return Response(str(e))

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

    def planet_by_name(self, request, planets):
        return planets.filter(name__icontains=request.query_params["search"])

    def set_count(self, count):
        """
        method used for seting and validating the count param
        the count param changes PAGINATION_COUNT which control the 
        quantity of instances comming in one page
         
        :param count: set count used for pagination 
        """
        try:
            self.PAGINATION_COUNT = int(count)
        except Exception:
            raise PageNotAnInteger(self.PAGE_ERR_MSG_COUNT_ARG)

        if self.PAGINATION_COUNT <= 0:
            raise InvalidPage(self.PAGE_ERR_MSG_LOW_0)

    def get_pages(self, planets, page):
        paginator = Paginator(planets, self.PAGINATION_COUNT)
        return paginator.page(page)



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
        """
        method for change the raw obj comming from database

        :param obj: raw object comming from database which will be customized 
        for any purpose  
        """
        self.set_number_appearance(obj, obj["name"])

        # put yours further changes here..

        return obj

    def set_number_appearance(self, obj, planet_name):
        obj["appearance_qnt"] = self.api_number_appearance(planet_name)

    def api_number_appearance(self, name):
        try:
            name = str(name)
            URL = "https://swapi.co/api/planets/?search=" + name
            r = requestsMod.get(url=URL)
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

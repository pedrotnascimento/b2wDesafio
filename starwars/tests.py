from rest_framework import status
from rest_framework.test import APITestCase
from starwars.models import Planet
from starwars.serializers import PlanetSerializer
from starwars.views import PlanetTransformData, PlanetList
import requests as reqs
import json

URL = '/planets/'
URL_ONE_TEMPL = URL + '{id}/'
URL_SEARCH = URL + "?search={s}"
URL_PAGE = URL + "?page={p}"
URL_PAGE_COUNT = URL_PAGE + "&count={c}"


class StarWarsAPITest(APITestCase):
    def setUp(self):
        self.alderaan = {"name": "Alderaan", "films_qnt": 2}
        self.starwars_api = "https://swapi.co/api/planets/?search={planet}"

    def test_get_planet(self):
        res = reqs.get(url=self.starwars_api.format(planet=self.alderaan["name"]))
        data = res.json()
        self.assertEqual(data["count"], 1)
        self.assertEqual(len(data["results"]), 1)
        self.assertEqual(len(data["results"][0]["films"]), self.alderaan["films_qnt"])


class PlanetGetTests(APITestCase):
    def setUp(self):
        self.alderaan = Planet.objects.create(
            name='Alderaan', terrain="grasslands, mountains", climate='temperate')
        self.hoth = Planet.objects.create(
            name='Hoth', terrain="tundra, ice caves, mountain ranges", climate='frozen')
        self.morty = Planet.objects.create(
            name='Morty', terrain="florest", climate='hot')
        Planet.objects.create(
            name='Rick', terrain='swamp', climate='any')

    def test_get_all_planets(self):
        # get API response
        response = self.client.get(URL)

        # get data from db
        planets = Planet.objects.all()
        serializer = PlanetSerializer(planets, many=True)

        planet_aux = PlanetTransformData()
        for i, aux_dict in enumerate(serializer.data):
            serializer.data[i] = planet_aux.transform(aux_dict)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_planet(self):
        response = self.client.get(URL_ONE_TEMPL.format(id=self.alderaan.id))
        self.assertEqual(response.data["id"], self.alderaan.id)

    def test_not_exist_planet(self):
        fake_id = "999"
        response = self.client.get(URL_ONE_TEMPL.format(id=fake_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_searched_planet(self):
        response = self.client.get(URL_SEARCH.format(s="Alderaan"))
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], self.alderaan.id)

    def test_get_multiple_searched_planets(self):
        response = self.client.get(URL_SEARCH.format(s="o"))
        self.assertTrue(len(response.data) > 1)

        # checking if all instance in response has the "o" in their name
        for i in response.data:
            if "o" not in i["name"]:
                self.assertTrue(False)

    def test_page_1(self):
        planets = Planet.objects.all()[:PlanetList.PAGINATION_COUNT]
        serializer = PlanetSerializer(planets, many=True)

        planet_aux = PlanetTransformData()
        for i, aux_dict in enumerate(serializer.data):
            serializer.data[i] = planet_aux.transform(aux_dict)

        response = self.client.get(URL_PAGE.format(p=1))
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.data, serializer.data)

    def test_page_count(self):
        new_page_count = 2
        page = 1
        planets = Planet.objects.all()[:new_page_count]
        serializer = PlanetSerializer(planets, many=True)

        planet_aux = PlanetTransformData()
        for i, aux_dict in enumerate(serializer.data):
            serializer.data[i] = planet_aux.transform(aux_dict)

        response = self.client.get(URL_PAGE_COUNT.format(p=page, c=new_page_count))
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.data, serializer.data)

    def test_page_2_count(self):
        new_page_count = 2
        page = 2
        planets = Planet.objects.all()[new_page_count:new_page_count*page]
        serializer = PlanetSerializer(planets, many=True)

        planet_aux = PlanetTransformData()
        for i, aux_dict in enumerate(serializer.data):
            serializer.data[i] = planet_aux.transform(aux_dict)

        response = self.client.get(URL_PAGE_COUNT.format(p=page, c=new_page_count))
        self.assertEqual(len(response.data), len(serializer.data))
        self.assertEqual(response.data, serializer.data)

    def test_page_count_error_param(self):
        page = 1
        err_page_count = "a"
        response = self.client.get(URL_PAGE_COUNT.format(p=page, c=err_page_count))
        self.assertEqual(response.data, PlanetList.PAGE_ERR_MSG_COUNT_ARG)

    def test_page_count_error_low_zero(self):
        page = 1
        err_page_count = -1
        response = self.client.get(URL_PAGE_COUNT.format(p=page, c=err_page_count))
        self.assertEqual(response.data, PlanetList.PAGE_ERR_MSG_LOW_0)

    def test_page_count_error_low_zero_2(self):
        page = 1
        err_page_count = 0
        response = self.client.get(URL_PAGE_COUNT.format(p=page, c=err_page_count))
        self.assertEqual(response.data, PlanetList.PAGE_ERR_MSG_LOW_0)


class CreateNewPlanetTest(APITestCase):
    def setUp(self):
        self.valid_instance = {
            'name': 'Marte',
            'climate': 'hell de janeiro',
            'terrain': 'mountains'
        }

        self.invalid_instance = {
            'name': '',
            'climate': 'hell de janeiro',
            'terrain': 'mountains'
        }

    def test_create_valid_planet(self):
        response = self.client.post(URL,
                                    data=json.dumps(self.valid_instance),
                                    content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.valid_instance["id"] = response.data["id"]
        self.assertEqual(response.data, self.valid_instance)

    def test_create_invalid_planet(self):
        response = self.client.post(URL,
                                    data=json.dumps(self.invalid_instance),
                                    content_type='application/json'
                                    )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UpdatePlanetTest(APITestCase):
    def setUp(self):
        self.planetTest = Planet.objects.create(
            name='Thanos',
            terrain="ok",
            climate='ok22')

        self.valid_instance = {
            'name': 'Nieztsche',
            'terrain': "Linguagem",
            'climate': 'tenso',
        }

        self.invalid_instance = {
            'name': '',
            'terrain': 'Linguagem2',
            'climate': 'tenso3'
        }

    def test_valid_update_planet(self):
        response = self.client.put(URL_ONE_TEMPL.format(id=self.planetTest.id),
                                   data=json.dumps(self.valid_instance),
                                   content_type='application/json'
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_planet(self):
        response = self.client.put(URL_ONE_TEMPL.format(id=self.planetTest.id),
                                   data=json.dumps(self.invalid_instance),
                                   content_type='application/json'
                                   )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_not_exist_update_planet(self):
        fake_id = "999"
        response = self.client.put(URL_ONE_TEMPL.format(id=fake_id),
                                       data=json.dumps(self.valid_instance),
                                       content_type='application/json'
                                       )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class DeletePlanetTest(APITestCase):
    def setUp(self):
        self.planetTest = Planet.objects.create(
            name='Thanos',
            terrain="ok",
            climate='ok22')

    def test_not_exist_delete_planet(self):
        fake_id = "999"
        response = self.client.delete(URL_ONE_TEMPL.format(id=fake_id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_planet(self):
        response = self.client.delete(URL_ONE_TEMPL.format(id=self.planetTest.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_already_deleted_planet(self):
        self.client.delete(URL_ONE_TEMPL.format(id=self.planetTest.id))
        response = self.client.delete(URL_ONE_TEMPL.format(id=self.planetTest.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

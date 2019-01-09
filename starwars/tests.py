from rest_framework import status
from rest_framework.test import APITestCase
from starwars.models import Planet
from starwars.serializers import PlanetSerializer
import json

URL = '/planets/'


class PlanetModelTests(APITestCase):
    def setUp(self):
        self.alderaan = Planet.objects.create(
            name='Alderaan', terrain="grasslands, mountains", climate='temperate')
        Planet.objects.create(
            name='Hoth', terrain="tundra, ice caves, mountain ranges", climate='frozen')
        Planet.objects.create(
            name='Morty', terrain="florest", climate='hot')
        Planet.objects.create(
            name='Ricky', terrain='swamp', climate='any')

    def test_get_all_planets(self):
        # get API response
        response = self.client.get(URL)

        # get data from db
        planets = Planet.objects.all()
        serializer = PlanetSerializer(planets, many=True)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_one_planet(self):
        response = self.client.get(URL + str(self.alderaan.id) + "/")
        self.assertEqual(response.data["id"], self.alderaan.id)

    def test_inexist_planet(self):
        fake_ID = "999"
        response = self.client.get(URL + fake_ID + "/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


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
        response = self.client.put(URL + str(self.planetTest.id) + "/",
                                   data=json.dumps(self.valid_instance),
                                   content_type='application/json'
                                   )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_planet(self):
        response = self.client.put(URL + str(self.planetTest.id) + "/",
                                   data=json.dumps(self.invalid_instance),
                                   content_type='application/json'
                                   )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inexist_update_planet(self):
        fake_ID = "999"
        response = self.client.delete(URL + fake_ID + "/",
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

    def test_inexist_delete_planet(self):
        fake_ID = "999"
        response = self.client.delete(URL + fake_ID + "/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_planet(self):
        response = self.client.delete(URL + str(self.planetTest.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_already_deleted_planet(self):
        self.client.delete(URL + str(self.planetTest.id) + "/")
        response = self.client.delete(URL + str(self.planetTest.id) + "/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

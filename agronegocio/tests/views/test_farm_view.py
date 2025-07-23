from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from agronegocio.models import Farm, Producer
from django.utils.translation import activate

class FarmViewSetTests(APITestCase):

    def setUp(self):
        self.producer = Producer.objects.create(name="Produtor Teste", cpf_cnpj="00000000000196")
        self.farm1 = Farm.objects.create(
            producer=self.producer, name="Fazenda 1", city="Cidade A", state="SP",
            total_area=100, arable_area=60, vegetation_area=30
        )
        self.farm2 = Farm.objects.create(
            producer=self.producer, name="Fazenda 2", city="Cidade B", state="MG",
            total_area=200, arable_area=150, vegetation_area=40
        )
        self.list_url = reverse('farm-list')

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve(self):
        url = reverse('farm-detail', args=[self.farm1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.farm1.name)

    def test_create(self):
        data = {
            "producer": self.producer.id,
            "name": "Fazenda 3",
            "city": "Cidade C",
            "state": "RS",
            "total_area": 120,
            "arable_area": 70,
            "vegetation_area": 40
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Farm.objects.filter(name="Fazenda 3").exists())

    def test_update(self):
        url = reverse('farm-detail', args=[self.farm1.id])
        data = {
            "producer": self.producer.id,
            "name": "Fazenda 1 Atualizada",
            "city": self.farm1.city,
            "state": self.farm1.state,
            "total_area": self.farm1.total_area,
            "arable_area": self.farm1.arable_area,
            "vegetation_area": self.farm1.vegetation_area,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.farm1.refresh_from_db()
        self.assertEqual(self.farm1.name, "Fazenda 1 Atualizada")

    def test_partial_update(self):
        url = reverse('farm-detail', args=[self.farm2.id])
        data = {"city": "Cidade Nova"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.farm2.refresh_from_db()
        self.assertEqual(self.farm2.city, "Cidade Nova")

    def test_delete(self):
        url = reverse('farm-detail', args=[self.farm1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Farm.objects.filter(id=self.farm1.id).exists())

    def test_validation_error_with_i18n(self):
        activate('en')

        data = {
            "producer": self.producer.id,
            "name": "Fazenda Inválida",
            "city": "Cidade X",
            "state": "XX",
            "total_area": 100,
            "arable_area": 60,
            "vegetation_area": 50,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("The sum of arable and vegetation areas cannot exceed the total area.", str(response.data))

    def test_validation_error_with_i18n_pt(self):
        activate('pt')

        data = {
            "producer": self.producer.id,
            "name": "Fazenda Inválida",
            "city": "Cidade Y",
            "state": "YY",
            "total_area": 100,
            "arable_area": 60,
            "vegetation_area": 50,
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("A soma das áreas agricultável e de vegetação não pode ultrapassar a área total.", str(response.data))

from django.utils.translation import activate
from rest_framework import status
from django.urls import reverse
from rest_framework.test import APITestCase
from agronegocio.models import Crop, Farm, Harvest, Producer

class CropViewSetTests(APITestCase):

    def setUp(self):
        self.producer = Producer.objects.create(name="Produtor", cpf_cnpj="00000000000195")
        self.farm = Farm.objects.create(
            producer=self.producer, name="Fazenda Teste", city="Cidade", state="SP",
            total_area=100, arable_area=50, vegetation_area=40
        )
        self.harvest = Harvest.objects.create(name="Safra 2022", year=2022)
        self.crop1 = Crop.objects.create(farm=self.farm, harvest=self.harvest, name="Soja")
        self.crop2 = Crop.objects.create(farm=self.farm, harvest=self.harvest, name="Milho")
        self.list_url = reverse('crop-list')

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve(self):
        url = reverse('crop-detail', args=[self.crop1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.crop1.name)

    def test_create(self):
        data = {
            "farm": self.farm.id,
            "harvest": self.harvest.id,
            "name": "Café"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Crop.objects.filter(name="Café").exists())

    def test_update(self):
        url = reverse('crop-detail', args=[self.crop1.id])
        data = {
            "farm": self.farm.id,
            "harvest": self.harvest.id,
            "name": "Soja Atualizada"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.crop1.refresh_from_db()
        self.assertEqual(self.crop1.name, "Soja Atualizada")

    def test_partial_update(self):
        url = reverse('crop-detail', args=[self.crop2.id])
        data = {"name": "Milho Patch"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.crop2.refresh_from_db()
        self.assertEqual(self.crop2.name, "Milho Patch")

    def test_delete(self):
        url = reverse('crop-detail', args=[self.crop1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Crop.objects.filter(id=self.crop1.id).exists())

    def test_create_missing_fields(self):
        data = {
            "farm": self.farm.id,
            "name": ""
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('harvest', response.data)
        self.assertIn('name', response.data)

    def test_create_unique_constraint(self):
        data = {
            "farm": self.farm.id,
            "harvest": self.harvest.id,
            "name": "Soja",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_update_invalid_farm(self):
        url = reverse('crop-detail', args=[self.crop1.id])
        data = {
            "farm": 9999,
            "harvest": self.harvest.id,
            "name": "Soja Atualizada"
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('farm', response.data)

    def test_partial_update_invalid_name(self):
        url = reverse('crop-detail', args=[self.crop1.id])
        data = {"name": ""}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_error_messages_are_translated(self):
        activate('en')

        data = {
            "farm": self.farm.id,
            "harvest": self.harvest.id,
            "name": "",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertTrue(any("This field may not be blank." in msg for msg in response.data.get('name', [])))

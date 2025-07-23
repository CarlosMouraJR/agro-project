from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils.translation import activate
from agronegocio.models import Harvest

class HarvestViewSetTests(APITestCase):

    def setUp(self):
        self.harvest1 = Harvest.objects.create(name="Safra 2021", year=2021)
        self.harvest2 = Harvest.objects.create(name="Safra 2022", year=2022)
        self.list_url = reverse('harvest-list')

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve(self):
        url = reverse('harvest-detail', args=[self.harvest1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.harvest1.name)

    def test_create(self):
        data = {"name": "Safra 2023", "year": 2023}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Harvest.objects.filter(name="Safra 2023").exists())

    def test_update(self):
        url = reverse('harvest-detail', args=[self.harvest1.id])
        data = {"name": "Safra 2021 Atualizada", "year": 2021}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.harvest1.refresh_from_db()
        self.assertEqual(self.harvest1.name, "Safra 2021 Atualizada")

    def test_partial_update(self):
        url = reverse('harvest-detail', args=[self.harvest2.id])
        data = {"year": 2025}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.harvest2.refresh_from_db()
        self.assertEqual(self.harvest2.year, 2025)

    def test_delete(self):
        url = reverse('harvest-detail', args=[self.harvest1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Harvest.objects.filter(id=self.harvest1.id).exists())

    def test_create_missing_name(self):
        data = {"year": 2023}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_missing_year(self):
        data = {"name": "Safra sem ano"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year', response.data)

    def test_create_invalid_year_type(self):
        data = {"name": "Safra inválida", "year": "invalid"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year', response.data)

    def test_update_invalid_year(self):
        url = reverse('harvest-detail', args=[self.harvest1.id])
        data = {"name": "Safra 2021", "year": "não é número"}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('year', response.data)

    def test_partial_update_invalid_name(self):
        url = reverse('harvest-detail', args=[self.harvest2.id])
        data = {"name": ""}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_error_messages_are_translated(self):
        activate('en')
        data = {"name": "", "year": ""}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(any("This field may not be blank." in msg for msg in response.data.get('name', [])))
        self.assertTrue(any("A valid integer is required." in msg for msg in response.data.get('year', [])))

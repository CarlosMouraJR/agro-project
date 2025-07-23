from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils.translation import activate
from agronegocio.models import Producer

class ProducerViewSetTests(APITestCase):

    def setUp(self):
        self.prod1 = Producer.objects.create(name="Produtor 1", cpf_cnpj="00000000000191")
        self.prod2 = Producer.objects.create(name="Produtor 2", cpf_cnpj="00000000000272")
        self.list_url = reverse('producer-list')

    def test_list(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve(self):
        url = reverse('producer-detail', args=[self.prod1.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.prod1.name)

    def test_create(self):
        data = {"name": "Produtor 3", "cpf_cnpj": "00000000000353"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Producer.objects.filter(name="Produtor 3").exists())

    def test_update(self):
        url = reverse('producer-detail', args=[self.prod1.id])
        data = {"name": "Produtor 1 Atualizado", "cpf_cnpj": self.prod1.cpf_cnpj}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.prod1.refresh_from_db()
        self.assertEqual(self.prod1.name, "Produtor 1 Atualizado")

    def test_partial_update(self):
        url = reverse('producer-detail', args=[self.prod2.id])
        data = {"name": "Produtor 2 Patch"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.prod2.refresh_from_db()
        self.assertEqual(self.prod2.name, "Produtor 2 Patch")

    def test_delete(self):
        url = reverse('producer-detail', args=[self.prod1.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Producer.objects.filter(id=self.prod1.id).exists())

    def test_create_missing_name(self):
        data = {"cpf_cnpj": "00000000000474"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('name', response.data)

    def test_create_missing_cpf_cnpj(self):
        data = {"name": "Produtor sem CPF"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cpf_cnpj', response.data)

    def test_create_invalid_cpf_cnpj(self):
        data = {"name": "Produtor Inválido", "cpf_cnpj": "invalid_cpf"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cpf_cnpj', response.data)
        self.assertTrue(any("Invalid CPF or CNPJ" in msg for msg in response.data['cpf_cnpj']))

    def test_create_duplicate_cpf_cnpj(self):
        data = {"name": "Produtor Duplicado", "cpf_cnpj": self.prod1.cpf_cnpj}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('cpf_cnpj', response.data)

    def test_error_messages_are_translated(self):
        activate('en')
        data = {"name": "", "cpf_cnpj": ""}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(any("This field may not be blank." in msg for msg in response.data.get('name', [])))
        self.assertTrue(any("Invalid CPF or CNPJ" in msg or "This field may not be blank." in msg for msg in response.data.get('cpf_cnpj', [])))

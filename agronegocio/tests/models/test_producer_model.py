from django.test import TestCase
from agronegocio.models import Producer


class ProducerModelTests(TestCase):

    def test_str_representation(self):
        producer = Producer.objects.create(name="Produtor Teste", cpf_cnpj="00000000000193")
        self.assertEqual(str(producer), "Produtor Teste (00000000000193)")

    def test_save_logs(self):
        producer = Producer(name="Produtor Log", cpf_cnpj="00000000000272")
        producer.save()
        self.assertTrue(Producer.objects.filter(cpf_cnpj="00000000000272").exists())

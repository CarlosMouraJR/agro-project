from django.test import TestCase
from agronegocio.models import Harvest


class HarvestModelTests(TestCase):

    def test_str_representation(self):
        harvest = Harvest.objects.create(name="Safra 2023", year=2023)
        self.assertEqual(str(harvest), "Safra 2023")

    def test_save_logs(self):
        harvest = Harvest(name="Safra Log", year=2024)
        harvest.save()
        self.assertTrue(Harvest.objects.filter(name="Safra Log").exists())

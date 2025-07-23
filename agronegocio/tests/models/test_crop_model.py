from django.test import TestCase
from agronegocio.models import Crop, Farm, Harvest, Producer


class CropModelTests(TestCase):

    def setUp(self):
        self.producer = Producer.objects.create(name="Produtor", cpf_cnpj="00000000000192")
        self.farm = Farm.objects.create(
            producer=self.producer,
            name="Fazenda Teste",
            city="Cidade",
            state="SP",
            total_area=100,
            arable_area=50,
            vegetation_area=40
        )
        self.harvest = Harvest.objects.create(name="Safra 2022", year=2022)

    def test_str_representation(self):
        crop = Crop.objects.create(farm=self.farm, harvest=self.harvest, name="Soja")
        self.assertEqual(str(crop), "Soja during Safra 2022")

    def test_str_representation_missing_harvest(self):
        crop = Crop(farm=self.farm, harvest=None, name="Milho")
        self.assertEqual(str(crop), "Milho (harvest id: None)")

    def test_save_logs(self):
        crop = Crop(farm=self.farm, harvest=self.harvest, name="Café")
        crop.save()
        self.assertTrue(Crop.objects.filter(name="Café").exists())

    def test_unique_together_constraint(self):
        Crop.objects.create(farm=self.farm, harvest=self.harvest, name="Soja")
        with self.assertRaises(Exception):  # IntegrityError or similar
            Crop.objects.create(farm=self.farm, harvest=self.harvest, name="Soja")

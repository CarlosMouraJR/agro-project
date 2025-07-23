from django.test import TestCase
from django.forms import ValidationError
from agronegocio.models import Farm, Producer


class FarmModelTests(TestCase):

    def setUp(self):
        self.producer = Producer.objects.create(name="Produtor Teste", cpf_cnpj="00000230000110")

    def test_str_representation(self):
        farm = Farm.objects.create(
            producer=self.producer,
            name="Fazenda A",
            city="Cidade X",
            state="SP",
            total_area=100,
            arable_area=50,
            vegetation_area=40
        )
        self.assertEqual(str(farm), "Fazenda A - Cidade X/SP")

    def test_clean_valid_areas(self):
        farm = Farm(
            producer=self.producer,
            name="Fazenda B",
            city="Cidade Y",
            state="MG",
            total_area=100,
            arable_area=30,
            vegetation_area=40
        )
        farm.clean()

    def test_clean_invalid_areas_raises_validation_error(self):
        farm = Farm(
            producer=self.producer,
            name="Fazenda C",
            city="Cidade Z",
            state="RS",
            total_area=100,
            arable_area=60,
            vegetation_area=50
        )
        with self.assertRaises(ValidationError):
            farm.clean()

    def test_save_calls_full_clean_and_saves(self):
        farm = Farm(
            producer=self.producer,
            name="Fazenda D",
            city="Cidade W",
            state="RJ",
            total_area=150,
            arable_area=70,
            vegetation_area=60
        )
        farm.save()
        self.assertTrue(Farm.objects.filter(name="Fazenda D").exists())

from django.test import TestCase
from django.core.exceptions import ValidationError
from agronegocio.services.farm_service import FarmService

class FarmServiceTests(TestCase):

    def test_validate_area_constraints_valid(self):
        try:
            FarmService.validate_area_constraints(100, 40, 50)
        except ValidationError:
            self.fail("ValidationError raised unexpectedly!")

    def test_validate_area_constraints_invalid(self):
        with self.assertRaises(ValidationError) as context:
            FarmService.validate_area_constraints(100, 60, 50)

        errors = context.exception.message_dict
        self.assertIn('arable_area', errors)
        self.assertIn('vegetation_area', errors)

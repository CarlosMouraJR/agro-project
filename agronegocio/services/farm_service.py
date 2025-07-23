import logging

from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class FarmService:
    @staticmethod
    def validate_area_constraints(total_area, arable_area, vegetation_area):
        if (arable_area + vegetation_area) > total_area:
            logger.error(f'Área inválida: total={total_area}, arável={arable_area}, vegetação={vegetation_area}')
            raise ValidationError({
                'arable_area': _('The sum of arable and vegetation areas cannot exceed the total area.'),
                'vegetation_area': _('The sum of arable and vegetation areas cannot exceed the total area.'),
            })
        logger.debug(f'Áreas validadas com sucesso: total={total_area}, arável={arable_area}, vegetação={vegetation_area}')

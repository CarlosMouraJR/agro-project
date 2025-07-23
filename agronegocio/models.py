import logging
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from agronegocio.services.farm_service import FarmService

logger = logging.getLogger(__name__)

class Producer(models.Model):
    cpf_cnpj = models.CharField(max_length=18, unique=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.name} ({self.cpf_cnpj})"

    def save(self, *args, **kwargs):
        logger.info(f"Tentando salvar Producer: {self}")
        try:
            super().save(*args, **kwargs)
            logger.info(f"Producer salvo com sucesso: {self}")
        except Exception as e:
            logger.error(f"Erro ao salvar Producer {self}: {e}")
            raise


class Farm(models.Model):
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE, related_name='farms')
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=2)
    total_area = models.DecimalField(max_digits=10, decimal_places=2)
    arable_area = models.DecimalField(max_digits=10, decimal_places=2)
    vegetation_area = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        super().clean()
        logger.info(f"Validando áreas da Farm: {self.name}")
        try:
            FarmService.validate_area_constraints(self.total_area, self.arable_area, self.vegetation_area)
            logger.info(f"Validação das áreas passou para a Farm: {self.name}")
        except ValidationError as e:
            logger.error(f"Validação falhou para a Farm {self.name}: {e}")
            raise

    def save(self, *args, **kwargs):
        logger.info(f"Tentando salvar Farm: {self}")
        self.full_clean()
        try:
            super().save(*args, **kwargs)
            logger.info(f"Farm salva com sucesso: {self}")
        except Exception as e:
            logger.error(f"Erro ao salvar Farm {self}: {e}")
            raise

    def __str__(self):
        return f"{self.name} - {self.city}/{self.state}"


class Harvest(models.Model):
    name = models.CharField(max_length=100)
    year = models.PositiveIntegerField()

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        logger.info(f"Tentando salvar Harvest: {self}")
        try:
            super().save(*args, **kwargs)
            logger.info(f"Harvest salva com sucesso: {self}")
        except Exception as e:
            logger.error(f"Erro ao salvar Harvest {self}: {e}")
            raise


class Crop(models.Model):
    farm = models.ForeignKey(Farm, on_delete=models.CASCADE, related_name='crops')
    harvest = models.ForeignKey(Harvest, on_delete=models.CASCADE, related_name='crops')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('farm', 'harvest', 'name')
        verbose_name = _('Crop')
        verbose_name_plural = _('Crops')

    def __str__(self):
        try:
            return f"{self.name} during {self.harvest.name}"
        except AttributeError:
            return f"{self.name} (harvest id: {self.harvest_id})"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f"Crop salvo: {self}")

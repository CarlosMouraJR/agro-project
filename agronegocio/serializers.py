import logging
from django.forms import ValidationError
from rest_framework import serializers

from agronegocio.services.farm_service import FarmService
from agronegocio.validators import validate_cpf_cnpj
from .models import Producer, Farm, Harvest, Crop
from django.utils.translation import gettext_lazy as _

logger = logging.getLogger(__name__)

class CropSerializer(serializers.ModelSerializer):
    farm = serializers.PrimaryKeyRelatedField(queryset=Farm.objects.all())
    harvest = serializers.PrimaryKeyRelatedField(queryset=Harvest.objects.all())

    class Meta:
        model = Crop
        fields = ['id', 'name', 'farm', 'harvest']

class FarmSerializer(serializers.ModelSerializer):
    crops = CropSerializer(many=True, read_only=True)
    producer = serializers.PrimaryKeyRelatedField(queryset=Producer.objects.all())

    class Meta:
        model = Farm
        fields = ['id', 'producer', 'name', 'city', 'state', 'total_area', 'arable_area', 'vegetation_area', 'crops']

    def validate(self, data):
        FarmService.validate_area_constraints(
            data.get('total_area'),
            data.get('arable_area'),
            data.get('vegetation_area')
        )
        return data

    def validate(self, data):
        total_area = data.get('total_area')
        arable_area = data.get('arable_area')
        vegetation_area = data.get('vegetation_area')

        if self.instance:
            total_area = total_area if total_area is not None else self.instance.total_area
            arable_area = arable_area if arable_area is not None else self.instance.arable_area
            vegetation_area = vegetation_area if vegetation_area is not None else self.instance.vegetation_area

        try:
            FarmService.validate_area_constraints(total_area, arable_area, vegetation_area)
            logger.info(f"Validação de área válida: total {total_area}, arável {arable_area}, vegetação {vegetation_area}")
        except ValidationError as e:
            logger.error(f"Validação de área falhou: {e.message_dict}")
            raise serializers.ValidationError(e.message_dict)

        return data

class ProducerSerializer(serializers.ModelSerializer):
    farms = FarmSerializer(many=True, read_only=True)

    class Meta:
        model = Producer
        fields = ['id', 'name', 'cpf_cnpj', 'farms']

    def validate_cpf_cnpj(self, value):
        try:
            validate_cpf_cnpj(value)
            logger.info(f"Valid CPF/CNPJ: {value}")
        except ValidationError:
            logger.error(f"Invalid CPF/CNPJ detected: {value}")
            raise serializers.ValidationError(
                _("Invalid CPF or CNPJ. Please check and try again.")
            )
        return value

class HarvestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Harvest
        fields = ['id', 'name', 'year']

import logging
from rest_framework import viewsets
from .models import Producer, Farm, Harvest, Crop
from .serializers import ProducerSerializer, FarmSerializer, HarvestSerializer, CropSerializer

logger = logging.getLogger(__name__)

class ProducerViewSet(viewsets.ModelViewSet):
    queryset = Producer.objects.all()
    serializer_class = ProducerSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f"Listando produtores - usuário: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Recuperando produtor id={kwargs.get('pk')} - usuário: {request.user}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Criando produtor - dados: {request.data} - usuário: {request.user}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Atualizando produtor id={kwargs.get('pk')} - dados: {request.data} - usuário: {request.user}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Patch no produtor id={kwargs.get('pk')} - dados: {request.data} - usuário: {request.user}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deletando produtor id={kwargs.get('pk')} - usuário: {request.user}")
        return super().destroy(request, *args, **kwargs)


class FarmViewSet(viewsets.ModelViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f"Listando fazendas - usuário: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Recuperando fazenda id={kwargs.get('pk')} - usuário: {request.user}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Criando fazenda - dados: {request.data} - usuário: {request.user}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Atualizando fazenda id={kwargs.get('pk')} - dados: {request.data} - usuário: {request.user}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Patch na fazenda id={kwargs.get('pk')} - dados: {request.data} - usuário: {request.user}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deletando fazenda id={kwargs.get('pk')} - usuário: {request.user}")
        return super().destroy(request, *args, **kwargs)


class HarvestViewSet(viewsets.ModelViewSet):
    queryset = Harvest.objects.all()
    serializer_class = HarvestSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f"Listando safras - usuário: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Recuperando safra id={kwargs.get('pk')} - usuário: {request.user}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Criando safra - dados: {request.data} - usuário: {request.user}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Atualizando safra id={kwargs.get('pk')} - dados: {request.data} - usuário: {request.user}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Patch na safra id={kwargs.get('pk')} - dados: {request.data} - usuário: {request.user}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deletando safra id={kwargs.get('pk')} - usuário: {request.user}")
        return super().destroy(request, *args, **kwargs)


class CropViewSet(viewsets.ModelViewSet):
    queryset = Crop.objects.all()
    serializer_class = CropSerializer

    def list(self, request, *args, **kwargs):
        logger.info(f"Listando culturas - usuário: {request.user}")
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        logger.info(f"Recuperando cultura id={kwargs.get('pk')} - usuário: {request.user}")
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        logger.info(f"Criando cultura - dados: {request.data} - usuário: {request.user}")
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        logger.info(f"Atualizando cultura id={kwargs.get('pk')} - dados: {request.data} - usuário: {request.user}")
        return super().update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        logger.info(f"Patch na cultura id={kwargs.get('pk')} - dados: {request.data} - usuário: {request.user}")
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        logger.info(f"Deletando cultura id={kwargs.get('pk')} - usuário: {request.user}")
        return super().destroy(request, *args, **kwargs)

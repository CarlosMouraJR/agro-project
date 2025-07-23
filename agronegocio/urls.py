from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProducerViewSet, FarmViewSet, HarvestViewSet, CropViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

router = DefaultRouter()
router.register(r'producers', ProducerViewSet)
router.register(r'farms', FarmViewSet)
router.register(r'harvests', HarvestViewSet)
router.register(r'crops', CropViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
]

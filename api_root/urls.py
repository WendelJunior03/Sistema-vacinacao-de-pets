from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from vacinacao import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.permissions import AllowAny

# Aqui são as rotas da API, onde cada rota corresponde a um conjunto de operações CRUD para cada modelo definido.
router = routers.DefaultRouter()
router.register(r'clinics', views.ClinicViewSet)
router.register(r'vaccines', views.VaccineViewSet)
router.register(r'vaccine-stocks', views.VaccineStockViewSet)
router.register(r'owners', views.OwnerViewSet)
router.register(r'pets', views.PetViewSet)
router.register(r'vaccination-records', views.VaccinationPetRecordViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(permission_classes=[AllowAny]), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema', permission_classes=[AllowAny]), name='swagger-ui'),
]

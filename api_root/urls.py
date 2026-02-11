from django.contrib import admin
from django.urls import path, include

from rest_framework import routers
from vacinacao import views

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
]

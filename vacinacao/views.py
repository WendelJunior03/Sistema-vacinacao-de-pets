from django.shortcuts import render

from rest_framework import viewsets
from .models import Clinic, Vaccine, VaccineStock, VaccinationPetRecord, Pet, Owner
from .serializers import ClinicSerializer, OwnerSerializer, PetSerializer, VaccinationPetRecordSerializer, VaccineSerializer, VaccineStockSerializer, VaccinationPetRecord

class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer

class VaccineViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer

class VaccineStockViewSet(viewsets.ModelViewSet):
    queryset = VaccineStock.objects.all()
    serializer_class = VaccineStockSerializer

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer

class VaccinationPetRecordViewSet(viewsets.ModelViewSet):
    queryset = VaccinationPetRecord.objects.all()
    serializer_class = VaccinationPetRecordSerializer
    
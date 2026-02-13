from django.shortcuts import render

from rest_framework import viewsets
from .models import Clinic, Vaccine, VaccineStock, VaccinationPetRecord, Pet, Owner
from .serializers import ClinicSerializer, OwnerSerializer, PetSerializer, VaccinationPetRecordSerializer, VaccineSerializer, VaccineStockSerializer, VaccinationPetRecord

from rest_framework.permissions import IsAuthenticated


class ClinicViewSet(viewsets.ModelViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    permission_classes = [IsAuthenticated]

class VaccineViewSet(viewsets.ModelViewSet):
    queryset = Vaccine.objects.all()
    serializer_class = VaccineSerializer
    permission_classes = [IsAuthenticated]

class VaccineStockViewSet(viewsets.ModelViewSet):
    queryset = VaccineStock.objects.all()
    serializer_class = VaccineStockSerializer
    permission_classes = [IsAuthenticated]

class OwnerViewSet(viewsets.ModelViewSet):
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [IsAuthenticated]

class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

class VaccinationPetRecordViewSet(viewsets.ModelViewSet):
    queryset = VaccinationPetRecord.objects.all()
    serializer_class = VaccinationPetRecordSerializer
    permission_classes = [IsAuthenticated]
    
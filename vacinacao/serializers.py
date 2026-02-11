from rest_framework import serializers
from .models import Vaccine, VaccineStock, VaccinationPetRecord, Pet, Owner, Clinic

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = '__all__'

class VaccineStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineStock
        fields = '__all__'

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = '__all__'

class VaccinationPetRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationPetRecord
        fields = '__all__'
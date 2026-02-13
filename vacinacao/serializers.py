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
        fields = ['id', 'cpf_owner', 'owner_name']

class PetSerializer(serializers.ModelSerializer):
    ''' aqui eu coloquei o source para referenciar
      o campo owner_pet do modelo Pet, que é a chave estrangeira para o modelo Owner.'''
    owner = OwnerSerializer(source='owner_pet', read_only=True)
    class Meta:
        model = Pet
        fields = ['id', 'pet_name', 'pet_breed', 'pet_age', 'owner_pet', 'owner']

class VaccinationPetRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationPetRecord
        fields = '__all__'
from rest_framework import serializers
from .models import Vaccine, VaccineStock, VaccinationPetRecord, Pet, Owner, Clinic
from rest_framework.validators import UniqueTogetherValidator

class ClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Clinic.objects.all(),
                fields=['cnpj'],
                message="Clinic with this CNPJ already exists."
            )
        ]

class VaccineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vaccine
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=Vaccine.objects.all(),
                fields=['vaccine_name'],
                message="Vaccine with this name already exists."
            )
        ]


class VaccineStockSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccineStock
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=VaccineStock.objects.all(),
                fields=['vaccine', 'clinic'],
                message="VaccineStock with this Vaccine and Clinic already exists."
            )
        ]

class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = ['id', 'cpf_owner', 'owner_name']

        validators = [
            UniqueTogetherValidator(
                queryset=Owner.objects.all(),
                fields=['cpf_owner'],
                message="Owner with this CPF already exists."
            )
        ]

class PetSerializer(serializers.ModelSerializer):
    owners = OwnerSerializer(many=True, read_only=True)
    owner_ids = serializers.PrimaryKeyRelatedField(
        queryset=Owner.objects.all(),
        many=True,
        write_only=True,
        source='owners',
    )

    def validate_owner_ids(self, value):
        if not value:
            raise serializers.ValidationError("Informe pelo menos um owner.")
        return value

    class Meta:
        model = Pet
        fields = ['id', 'microchip_id', 'pet_name', 'pet_breed', 'pet_age', 'owners', 'owner_ids']

class VaccinationPetRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = VaccinationPetRecord
        fields = '__all__'

        validators = [
            UniqueTogetherValidator(
                queryset=VaccinationPetRecord.objects.all(),
                fields=['pet', 'vaccine', 'vaccination_date'],
                message="Vaccination record with this Pet, Vaccine and Vaccination Date already exists."
            )
        ]

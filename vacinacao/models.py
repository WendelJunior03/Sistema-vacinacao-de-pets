from django.db import models

class Clinic(models.Model):
    clinic_name = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=20, unique=True)
    responsible_pet_owner = models.CharField(max_length=255)


class Owner(models.Model):
    cpf_owner = models.CharField(max_length=14, unique=True)
    owner_name = models.CharField(max_length=255, default="")

class Pet(models.Model):
    pet_name = models.CharField(max_length=255, default="")
    pet_breed = models.CharField(max_length=255, default="")
    pet_age = models.IntegerField(default=0)
    owner_pet = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='pets')

# Aqui eu coloquei a restrição de unicidade para garantir que um pet seja cadastrado apenas uma vez por proprietário
    def __str__(self):
        return self.pet_name

class Vaccine(models.Model):
    vaccine_name = models.CharField(max_length=255, unique=True)


class VaccineStock(models.Model):
    vaccine_name = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='stocks')

# Aqui eu coloquei a restrição de unicidade para garantir que uma vacina seja armazenada apenas em uma clinica.
# Para não ter mais de uma vacina com o mesmo nome em diferentes clínicas, o que poderia causar confusão
    class Meta:
        unique_together = ('vaccine_name', 'clinic')

class VaccinationPetRecord(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name='vaccination')
    vaccine_name = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    vaccination_date = models.DateField()

# Aqui eu coloquei a restrição de unicidade para garantir que um pet não possa ser vacinado com a mesma vacina na mesma data mais de uma vez.
    class Meta:
        unique_together = ('pet', 'vaccine_name', 'vaccination_date')

    def __str__(self):
        return f"{self.pet} - {self.vaccine_name} - {self.vaccination_date}"
from django.db import models

# Create your models here.
from django.db import models

class HealthProgram(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    contact = models.CharField(max_length=20)

    def __str__(self):
        return self.full_name

class Enrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    program = models.ForeignKey(HealthProgram, on_delete=models.CASCADE)
    date_enrolled = models.DateField(auto_now_add=True)

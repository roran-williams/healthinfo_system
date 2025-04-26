# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class HealthProgram(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_programs',null=True)
    date_created = models.DateField(auto_now_add=True, null=True)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Client(models.Model):
    full_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    contact = models.CharField(max_length=20)
    is_deleted = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='clients',null=True)


    def __str__(self):
        return self.full_name

class Enrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    program = models.ForeignKey(HealthProgram, on_delete=models.CASCADE)
    enrolled_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='enrollments',null=True)
    date_enrolled = models.DateField(auto_now_add=True)

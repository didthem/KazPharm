# models.py
from django.contrib.auth.models import User
from django.db import models

class Doctor(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    experience = models.IntegerField()
    specialization = models.CharField(max_length=255)
    hospitals = models.ForeignKey('Hospital', on_delete=models.CASCADE, related_name='doctors', null=True)

    def str(self):
        return self.first_name + ' ' + self.last_name

class Hospital(models.Model):
    title = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)

    def str(self):
        return self.title

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hospital = models.ForeignKey('Hospital', on_delete=models.CASCADE)
    doctor = models.ForeignKey('Doctor', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()


from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms

# ─── Location Helpers ─────────────────────────────

DISTANCES = [5,10,25,50,100]

class State(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)  # CA, NY, etc.

    def __str__(self):
        return self.code

class City(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.code}"

class ZipCode(models.Model):
    id = models.AutoField(primary_key=True)
    code = models.CharField(max_length=10, unique=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.code

# ─── Users and Conditions ─────────────────────────

class User(AbstractUser):
    zip_code = models.ForeignKey(ZipCode, null=True, blank=True, on_delete=models.SET_NULL)
    conditions = models.ManyToManyField("Condition", blank=True)
    
    def __str__(self):
        return f"{self.username} : {self.conditions.all()}"
    

class Condition(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
    
class Specialty(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# ─── Doctors and Endorsements ─────────────────────

class Doctor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    suffix = models.CharField(max_length=20, blank=True, null=True)
    specialty = models.ForeignKey(Specialty, on_delete=models.SET_NULL, null=True)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    image = models.CharField(null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.SET_NULL, null=True)
    conditions_treated = models.ManyToManyField(Condition, related_name='doctors')

    def __str__(self):
        return f"{self.id} : {self.name}"

class Endorsement(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'doctor', 'condition')
        indexes = [
            models.Index(fields=['doctor', 'condition']),
        ]

    def __str__(self):
        return f"{self.id} id {self.user.username} endorsed {self.doctor.name} for {self.condition.name} on {self.created_at.date()}"


# ─── Indexing Optimization ────────────────────────

    indexes = [
        models.Index(fields=['doctor', 'condition']),
    ]


from django.contrib.auth.models import AbstractUser
from django.db import models

# ─── Location Helpers ─────────────────────────────

class State(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=2)  # CA, NY, etc.

    def __str__(self):
        return self.code

class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}, {self.state.code}"

class ZipCode(models.Model):
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

class Condition(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

# ─── Doctors and Endorsements ─────────────────────

class Doctor(models.Model):
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=100)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    image = models.CharField(null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    zip_code = models.ForeignKey(ZipCode, on_delete=models.SET_NULL, null=True)
    conditions_treated = models.ManyToManyField(Condition, related_name='doctors')

    def __str__(self):
        return self.name

class Endorsement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    condition = models.ForeignKey(Condition, on_delete=models.CASCADE)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'doctor', 'condition')

# ─── Indexing Optimization ────────────────────────

    indexes = [
        models.Index(fields=['doctor', 'condition']),
    ]

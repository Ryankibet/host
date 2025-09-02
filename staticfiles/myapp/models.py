from django.db import models
from django.core.validators import RegexValidator


# Create your models here.

class Appointment(models.Model):
    phone_validator = RegexValidator(r'^\d{10}$', 'Phone number must be 10 digits.')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=10, validators=[phone_validator])
    date = models.DateField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"

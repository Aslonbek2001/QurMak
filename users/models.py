from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

class ClientModel(AbstractUser):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    phone = models.CharField(verbose_name="Client phone", db_index=True, max_length=20, unique=True, null=True)
    devise = models.CharField(max_length=100, blank=True, null=True)
    date_start = models.DateTimeField(verbose_name="Active Start", null=True, blank=True)
    date_end = models.DateTimeField(verbose_name="Active End", blank=True, null=True)

    def __str__(self):
        return f"{self.username} - {self.phone}"




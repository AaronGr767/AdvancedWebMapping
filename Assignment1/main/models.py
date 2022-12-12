from django.contrib import admin
from django.contrib.gis.db import models
from django.contrib.auth import get_user_model
# Register your models here.
from django.contrib.auth.models import AbstractUser, BaseUserManager


User = get_user_model()


class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, primary_key=True)
    locations = models.CharField(max_length=350, null=True)

    def __str__(self):
        return f"{self.user}"

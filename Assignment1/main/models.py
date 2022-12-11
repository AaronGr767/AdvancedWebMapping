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
    # loc0 = models.PointField(null=True)
    # loc1 = models.PointField(null=True)
    # loc2 = models.PointField(null=True)
    # loc3 = models.PointField(null=True)
    # loc4 = models.PointField(null=True)
    # loc5 = models.PointField(null=True)

    def __str__(self):
        return f"{self.user}"

# class TripRoute(models.Model):
#     user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
#     username = models.CharField(max_length=150, primary_key=True)
#     loc0 = models.PointField(null=True)
#     loc1 = models.PointField(null=True)
#     loc2 = models.PointField(null=True)
#     loc3 = models.PointField(null=True)
#     loc4 = models.PointField(null=True)
#     loc5 = models.PointField(null=True)
#
#     def __str__(self):
#         return f"{self.user}"

# class UserManager(BaseUserManager):
#     use_in_migration = True
#
#     def create_user(self, username, email, password=None, **extra_fields):
#         if not email:
#             raise ValueError('Email is Required')
#         user = self.model(email=self.normalize_email(email), **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#         extra_fields.setdefault('is_active', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff = True')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser = True')
#
#         return self.create_user(email, password, **extra_fields)
#
#
# class UserData(AbstractUser):
#     username = None
#     name = models.CharField(max_length=100, unique=True)
#     email = models.EmailField(max_length=100, unique=True)
#     date_joined = models.DateTimeField(auto_now_add=True)
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     objects = UserManager()
#
#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['name']
#
#     def __str__(self):
#         return self.name
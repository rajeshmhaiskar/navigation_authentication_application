# GenesysUserApp.models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import CustomUserManager
from .constants import DESIGNATION_CHOICES


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class MasterDatabase(BaseModel):
    database_name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    server_ip = models.GenericIPAddressField(null=False, blank=False)
    port = models.PositiveIntegerField(null=False, blank=False)
    username = models.CharField(max_length=255, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.database_name


class UserDetails(AbstractBaseUser, PermissionsMixin, BaseModel):
    emp_id = models.CharField(max_length=10, unique=True, null=False, blank=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    password = models.CharField(max_length=255, null=False, blank=False)
    designation = models.CharField(max_length=255, choices=DESIGNATION_CHOICES, null=False, blank=False)
    selected_databases = models.ManyToManyField(MasterDatabase, blank=False)
    is_active = models.BooleanField(default=True)
    has_resigned = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'emp_id'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.emp_id

# Add other models as needed...

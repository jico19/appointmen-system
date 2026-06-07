from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class RoleChoices(models.TextChoices):
        USER = "USER", "User"
        STAFF = "STAFF", "Staff"
        ADMIN = "ADMIN", "Admin"
    
    
    phone_no = models.CharField(max_length=11, blank=True)
    role = models.CharField(max_length=20, choices=RoleChoices, default=RoleChoices.USER)



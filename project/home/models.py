from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    is_owner=models.BooleanField('Is owner', default=False)
    is_customer=models.BooleanField('Is customer', default=False)

from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):

    class Meta:
        default_related_name = 'users'
# Define a custom User class to work with django-social-auth
from django.contrib.auth.models import AbstractUser, UserManager


class CustomUser(AbstractUser):
    objects = UserManager()

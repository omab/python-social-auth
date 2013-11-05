from mongoengine.fields import ListField
from mongoengine.django.auth import User


class User(User):
    """Extend Mongo Engine User model"""
    foo = ListField(default=[])

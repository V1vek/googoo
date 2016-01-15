from django.db import models
from django.conf import settings


class Customer(models.Model):
    profile = models.OneToOneField(settings.AUTH_USER_MODEL, unique=True)
    contact_number = models.CharField(max_length=20, null=True)
    email = models.EmailField(max_length=50, null=True)
    address = models.TextField(null=True)
    address1 = models.TextField(null=True)
    state = models.CharField(max_length=20, null=True)
    city = models.CharField(max_length=20, null=True)
    zip_code = models.IntegerField(null=True)




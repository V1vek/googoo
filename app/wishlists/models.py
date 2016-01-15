from django.db import models
from django.contrib import admin
from django.utils import timezone
from django.conf import settings


class Wishlist(models.Model):
    products = models.ForeignKey('products.Product')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)

admin.site.register(Wishlist)

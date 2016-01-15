from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey('products.Product')
    quantity = models.IntegerField(default=0)
    price = models.IntegerField(null=True)
    is_ordered = models.BooleanField(default=False)




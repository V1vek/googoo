from django.db import models
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    product = models.ForeignKey('products.Product')
    size = models.CharField(max_length=3, blank=False)
    quantity = models.IntegerField(default=1)
    price = models.FloatField(null=True)
    is_ordered = models.BooleanField(default=False)




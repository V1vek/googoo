from datetime import datetime

from django.db import models
from django.conf import settings

from app.orders.models import Order


class OrderShippingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    order = models.ForeignKey(Order, related_name="order")
    name = models.CharField(max_length=50, null=True)
    address = models.CharField(max_length=200, null=True)
    address1 = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=50, null=True)
    zip_code = models.CharField(max_length=10, null=True)
    contact_number = models.CharField(max_length=20, null=True)
    ordered_date = models.DateTimeField(default=datetime.now(), blank=True)
    is_default = models.BooleanField(default=False)







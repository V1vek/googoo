from datetime import datetime

from django.db import models
from django.conf import settings

from app.discount_coupon.models import Discount


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    ordered_date = models.DateTimeField(default=datetime.now(), blank=True)
    order_total = models.FloatField(default=0)
    shipping_price = models.FloatField(default=0)
    cart_total = models.FloatField(default=0)
    complete_total = models.FloatField(default=0)
    discount_price = models.FloatField(default=0)
    discount_id = models.ForeignKey(Discount, null=True)

    INITIATED = '1'
    PLACED = '2'
    CANCELLED = '3'
    ORDER_OPTIONS = (
        (INITIATED, 'Initiated'),
        (PLACED, 'Placed'),
        (CANCELLED, 'Cancelled')
    )

    order_options = models.CharField(max_length=2, choices=ORDER_OPTIONS, default=INITIATED)

    PENDING = '1'
    CANCELLED = '2'
    PAID = '3'
    COD = '4'
    PAYMENT_STATUS = (
        (PENDING, 'Pending'),
        (CANCELLED, 'Cancelled'),
        (PAID, 'Paid'),
        (COD, 'Cod')
    )

    payment_status = models.CharField(max_length=2, choices=PAYMENT_STATUS, default=PENDING)

    transaction_id = models.CharField(max_length=25, null=True)
    note = models.TextField()

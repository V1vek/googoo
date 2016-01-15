from django.db import models
from django.contrib import admin


class Discount(models.Model):
    coupon_code = models.CharField(max_length=20, blank=False, unique=True)

    RUPEES = '1'
    PERCENTAGE = '2'
    OFFER_TYPE = (
        (RUPEES, 'Rupees'),
        (PERCENTAGE, 'Percentage'),
    )

    offer_type = models.CharField(max_length=2, choices=OFFER_TYPE, default=RUPEES)
    offer_value = models.IntegerField(default=0)
    minimum_amount = models.IntegerField(default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.coupon_code

admin.site.register(Discount)

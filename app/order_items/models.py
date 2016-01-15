from django.db import models


class OrderItem(models.Model):
    order = models.ForeignKey('orders.Order')
    product = models.ForeignKey('products.Product')
    quantity = models.IntegerField(default=1)
    price = models.FloatField(default=0)
    cancel_item = models.BooleanField(default=False)
    tracking_id = models.CharField(max_length=30, null=True)
    tracking_url = models.URLField(max_length=200, null=True)

    PROCESSED = '1'
    CANCELLED = '2'
    SHIPPED = '3'
    DELIVERED = '4'
    RECEIVED = '5'
    ORDER_STATUS = (
        (PROCESSED, 'Processed'),
        (SHIPPED, 'Shipped'),
        (DELIVERED, 'Delivered'),
        (CANCELLED, 'Cancelled'),
    )

    order_status = models.CharField(max_length=2, choices=ORDER_STATUS, default=PROCESSED)






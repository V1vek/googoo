# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '__first__'),
        ('orders', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('quantity', models.IntegerField(default=1)),
                ('price', models.FloatField(default=0)),
                ('cancel_item', models.BooleanField(default=False)),
                ('tracking_id', models.CharField(max_length=30, null=True)),
                ('tracking_url', models.URLField(null=True)),
                ('order_status', models.CharField(default=b'1', max_length=2, choices=[(b'1', b'Processed'), (b'3', b'Shipped'), (b'4', b'Delivered'), (b'2', b'Cancelled')])),
                ('order', models.ForeignKey(to='orders.Order')),
                ('product', models.ForeignKey(to='products.Product')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

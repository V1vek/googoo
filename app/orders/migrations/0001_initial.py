# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('discount_coupon', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ordered_date', models.DateTimeField(default=datetime.datetime(2016, 1, 14, 15, 1, 26, 670000), blank=True)),
                ('order_total', models.FloatField(default=0)),
                ('shipping_price', models.FloatField(default=0)),
                ('cart_total', models.FloatField(default=0)),
                ('complete_total', models.FloatField(default=0)),
                ('discount_price', models.FloatField(default=0)),
                ('order_options', models.CharField(default=b'1', max_length=2, choices=[(b'1', b'Initiated'), (b'2', b'Placed'), (b'3', b'Cancelled')])),
                ('payment_status', models.CharField(default=b'1', max_length=2, choices=[(b'1', b'Pending'), (b'2', b'Cancelled'), (b'3', b'Paid'), (b'4', b'Cod')])),
                ('transaction_id', models.CharField(max_length=25, null=True)),
                ('note', models.TextField()),
                ('discount_id', models.ForeignKey(to='discount_coupon.Discount', null=True)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Discount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coupon_code', models.CharField(unique=True, max_length=b'20')),
                ('offer_type', models.CharField(default=b'1', max_length=2, choices=[(b'1', b'Rupees'), (b'2', b'Percentage')])),
                ('offer_value', models.IntegerField(default=0)),
                ('minimum_amount', models.IntegerField(default=0)),
                ('start_date', models.DateField(null=True, blank=True)),
                ('end_date', models.DateField(null=True, blank=True)),
                ('is_active', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

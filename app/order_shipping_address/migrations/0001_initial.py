# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '__first__'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderShippingAddress',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=50, null=True)),
                ('address', models.CharField(max_length=200, null=True)),
                ('address1', models.CharField(max_length=200, null=True)),
                ('city', models.CharField(max_length=50, null=True)),
                ('state', models.CharField(max_length=50, null=True)),
                ('zip_code', models.CharField(max_length=10, null=True)),
                ('contact_number', models.CharField(max_length=20, null=True)),
                ('ordered_date', models.DateTimeField(default=datetime.datetime(2016, 1, 14, 15, 1, 20, 944000), blank=True)),
                ('is_default', models.BooleanField(default=False)),
                ('order', models.ForeignKey(related_name=b'order', to='orders.Order')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

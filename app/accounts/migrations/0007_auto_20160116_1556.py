# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-16 15:56
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20160116_0719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 16, 15, 56, 40, 285034)),
        ),
    ]
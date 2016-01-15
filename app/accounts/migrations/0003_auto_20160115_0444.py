# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-01-15 04:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20160115_0425'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='user',
            name='key_expires',
            field=models.DateTimeField(default=datetime.datetime(2016, 1, 15, 4, 44, 55, 571070)),
        ),
    ]
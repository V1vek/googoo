# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('contact_number', models.CharField(max_length=20, null=True)),
                ('email', models.EmailField(max_length=50, null=True)),
                ('address', models.TextField(null=True)),
                ('address1', models.TextField(null=True)),
                ('state', models.CharField(max_length=20, null=True)),
                ('city', models.CharField(max_length=20, null=True)),
                ('zip_code', models.IntegerField(null=True)),
                ('profile', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

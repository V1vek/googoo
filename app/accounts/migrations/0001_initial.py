# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import datetime
import re
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('username', models.CharField(unique=True, max_length=30, verbose_name='username', validators=[django.core.validators.RegexValidator(re.compile(b'^[\\w.@+-]+$'), 'Enter a valid username.', 'invalid')])),
                ('first_name', models.CharField(max_length=30, null=True, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, null=True, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=255, verbose_name='email address')),
                ('is_active', models.BooleanField(default=False, verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('receive_newsletter', models.BooleanField(default=False, verbose_name='receive newsletter')),
                ('activation_key', models.CharField(max_length=40, blank=b'True')),
                ('reset_password_key', models.CharField(max_length=40, blank=b'True')),
                ('key_expires', models.DateTimeField(default=datetime.datetime(2016, 1, 14, 15, 0, 29, 781000))),
                ('is_email_verified', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(related_query_name=b'user', related_name=b'tmp_user_set', verbose_name='groups', to='auth.Group', blank=True)),
                ('user_permissions', models.ManyToManyField(related_query_name=b'user', related_name=b'tmp_user_set', verbose_name='user permissions', to='auth.Permission', blank=True)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
    ]

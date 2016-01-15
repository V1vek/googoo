# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('type', models.CharField(default=b'Men', max_length=20, choices=[(b'Men', b'Men'), (b'Women', b'Women'), (b'Boys', b'Boys'), (b'Girls', b'Girls'), (b'Home_textiles', b'Home_textiles')])),
                ('sub_type', models.CharField(default=b'Clothing', max_length=20, choices=[(b'Clothing', b'Clothing'), (b'Accessories', b'Accessories'), (b'Bed', b'Bed'), (b'Bath', b'Bath'), (b'Living', b'Living')])),
                ('category_name', models.CharField(default=b'', max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]

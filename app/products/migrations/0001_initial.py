# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('categories', '0001_initial'),
        ('sub_categories', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('img_url', models.URLField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Colour',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('product_group_number', models.IntegerField(max_length=50, null=True)),
                ('description', models.TextField()),
                ('unit_price', models.FloatField(max_length=5)),
                ('stock', models.IntegerField()),
                ('reorder_level', models.IntegerField()),
                ('product_available', models.BooleanField()),
                ('img_url', models.URLField()),
                ('img_url2', models.URLField(blank=True)),
                ('img_url3', models.URLField(blank=True)),
                ('img_url4', models.URLField(blank=True)),
                ('discount', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brand', models.ForeignKey(to='products.Brand')),
                ('category', models.OneToOneField(null=True, to='categories.Category')),
                ('colour', models.ForeignKey(to='products.Colour')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=10)),
                ('category', models.ForeignKey(to='categories.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='product',
            name='size',
            field=models.ManyToManyField(to='products.Size'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='product',
            name='sub_categories',
            field=models.ManyToManyField(to='sub_categories.SubCategory', null=True),
            preserve_default=True,
        ),
    ]

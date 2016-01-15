from django.db import models
from django.contrib import admin

# Create your models here.


class Colour(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField()

    def __unicode__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=10)
    category = models.ForeignKey('categories.Category')

    def __unicode__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    img_url = models.URLField(max_length=200)

    def __unicode__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    product_group_number = models.IntegerField(max_length=50, null=True)
    description = models.TextField()
    category = models.OneToOneField('categories.Category', null=True)
    sub_categories = models.ManyToManyField('sub_categories.SubCategory', null=True)
    unit_price = models.FloatField(max_length=5)
    size = models.ManyToManyField('products.Size')
    colour = models.ForeignKey('products.Colour')
    stock = models.IntegerField()
    reorder_level = models.IntegerField()
    product_available = models.BooleanField(default=True)
    img_url = models.URLField(max_length=200, blank=False)
    img_url2 = models.URLField(max_length=200, blank=True)
    img_url3 = models.URLField(max_length=200, blank=True)
    img_url4 = models.URLField(max_length=200, blank=True)
    brand = models.ForeignKey('products.Brand')
    discount = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.name

admin.site.register(Colour)
admin.site.register(Size)
admin.site.register(Brand)
admin.site.register(Product)

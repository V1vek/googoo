from django.db import models
from django.contrib import admin

# Create your models here.


class SubCategory(models.Model):
    type = models.CharField(max_length=100)
    sub_type = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey('categories.Category', related_name='sub_categories')

    def __unicode__(self):
        return self.sub_type

admin.site.register(SubCategory)

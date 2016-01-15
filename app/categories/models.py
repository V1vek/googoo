from django.db import models
from django.contrib import admin

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    MEN = 'Men'
    WOMEN = 'Women'
    BOYS = 'Boys'
    GIRLS = 'Girls'
    HOME_TEXTILES = 'Home_textiles'
    TYPE_CHOICES = (
        (MEN, 'Men'),
        (WOMEN, 'Women'),
        (BOYS, 'Boys'),
        (GIRLS, 'Girls'),
        (HOME_TEXTILES, 'Home_textiles'),
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default=MEN)

    CLOTHING = 'Clothing'
    ACCESSORIES = 'Accessories'
    BED = 'Bed'
    BATH = 'Bath'
    LIVING = 'Living'
    SUB_TYPE_CHOICES = (
        (CLOTHING, 'Clothing'),
        (ACCESSORIES, 'Accessories'),
        (BED, 'Bed'),
        (BATH, 'Bath'),
        (LIVING, 'Living'),
    )

    sub_type = models.CharField(max_length=20, choices=SUB_TYPE_CHOICES, default=CLOTHING)

    category_name = models.CharField(max_length=100, default='')

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        self.category_name = '{0} {1}'.format(self.name, self.type)
        super(Category, self).save(force_insert, force_update)

    def __unicode__(self):
        return self.category_name



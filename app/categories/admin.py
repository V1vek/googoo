from django.contrib import admin
from app.categories.models import Category

# Register your models here.


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'type', 'sub_type']


admin.site.register(Category, CategoryAdmin)
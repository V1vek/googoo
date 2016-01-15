from django.contrib import admin
from app.carts.models import Cart

# Register your models here.


class CartAdmin(admin.ModelAdmin):
    fields = ['user', 'product', 'quantity', 'price', 'is_ordered']


admin.site.register(Cart, CartAdmin)
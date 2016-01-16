from rest_framework import serializers
from app.carts.models import Cart
from app.products.serializers import ProductSerializer


class CartSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = Cart
        fields = ('user', 'product', 'size', 'quantity', 'price')

from rest_framework import serializers

from app.wishlists.models import Wishlist
# ----------------- change this -----------------
from app.products.serializers import ProductSerializer


class WishlistSerializer(serializers.ModelSerializer):
    # ----------------- change this -----------------
    products = ProductSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = ('id', 'products')



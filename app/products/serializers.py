from rest_framework import serializers
from app.products.models import Product, Colour, Size, Brand
from app.sub_categories.serializers import SubCategorySerializer


class BrandSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brand
        fields = ('name',)

class ProductBrandSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Product
        fields = ('brand',)

class ColourSerializer(serializers.ModelSerializer):

    class Meta:
        model = Colour
        fields = ('name',)

class ProductColourSerializer(serializers.ModelSerializer):
    colour = ColourSerializer()

    class Meta:
        model = Colour
        fields = ('colour',)

class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = ('name',)

class ProductsListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('id', 'name', 'sub_categories', 'unit_price', 'img_url')


class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    colour = ColourSerializer()
    size = SizeSerializer(many=True)
    sub_categories = SubCategorySerializer(many=True)

    class Meta:
        model = Product
        fields = ('name', 'sub_categories', 'unit_price', 'colour', 'size', 'brand', 'stock', 'img_url')



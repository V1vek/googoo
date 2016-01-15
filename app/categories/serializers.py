from rest_framework import serializers
from app.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'type', 'sub_type')

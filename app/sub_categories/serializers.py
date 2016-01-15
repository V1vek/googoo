from rest_framework import serializers
from app.sub_categories.models import SubCategory


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubCategory
        fields = ('type', 'sub_type', 'category')
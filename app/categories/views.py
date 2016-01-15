from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.categories.models import Category
from app.categories.serializers import CategorySerializer

# Create your views here.


@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.all()
    categories_serializer = CategorySerializer(categories, many=True)
    return Response(categories_serializer.data)


@api_view(['GET'])
def category_details(request, category_type, category):
    if category is None:
        category_detail = Category.objects.filter(type=category_type)
        category_serializer = CategorySerializer(category_detail, many=True)
    else:
        category_detail = Category.objects.get(name=category, type=category_type)
        category_serializer = CategorySerializer(category_detail)
    return Response(category_serializer.data)

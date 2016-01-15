from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.categories.models import Category
from app.categories.serializers import CategorySerializer

# Create your views here.


@api_view(['GET'])
def categories_list(request):
    categories = Category.objects.all()
    context = {}
    for category in categories:
        if not str(category.type) in context.keys():
            context[str(category.type)] = {}
        if not str(category.sub_type) in context[str(category.type)].keys():
            context[str(category.type)][str(category.sub_type)] = []

        context[str(category.type)][str(category.sub_type)].append(category.name)

        if category.sub_type == 'Accessories':
            if not str(category.sub_type) in context.keys():
                context[str(category.sub_type)] = {}
            if not str(category.type) in context[str(category.sub_type)].keys():
                context[str(category.sub_type)][str(category.type)] = []

            context[str(category.sub_type)][str(category.type)].append(category.name)
    return Response(context)


@api_view(['GET'])
def category_details(request, category_type, category):
    if category is None:
        category_detail = Category.objects.filter(type=category_type)
        category_serializer = CategorySerializer(category_detail, many=True)
    else:
        category_detail = Category.objects.get(name=category, type=category_type)
        category_serializer = CategorySerializer(category_detail)
    return Response(category_serializer.data)

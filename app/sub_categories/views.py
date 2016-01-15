from rest_framework.decorators import api_view
from rest_framework.response import Response
from app.sub_categories.models import SubCategory
from app.sub_categories.serializers import SubCategorySerializer

# Create your views here.


@api_view(['GET'])
def sub_category_list(request, type, category):
    category = '{0} {1}'.format(category, type)
    sub_category = SubCategory.objects.filter(category=category)
    sub_category_serializer = SubCategorySerializer(sub_category, many=True)
    return Response(sub_category_serializer.data)

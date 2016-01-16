import json

from collections import defaultdict

from django.http import HttpResponse

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from app.categories.models import Category
from app.products.models import Product, Size, Brand, Colour
from app.products.serializers import ProductsListSerializer, ProductSerializer, SizeSerializer, BrandSerializer, ColourSerializer
from app.sub_categories.models import SubCategory
from app.sub_categories.serializers import SubCategorySerializer
from app.categories.serializers import CategorySerializer


# Create your views here.
@permission_classes((AllowAny,))
@api_view(['GET', 'POST'])
def products_list(request, product_type, product_category):
    if request.method == 'GET':
        try:
            category = '{0} {1}'.format(product_category, product_type)
            products = Product.objects.filter(category__category_name=category)
        except Product.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        products_serializer = ProductsListSerializer(products, many=True)
        return Response(products_serializer.data)

    if request.method == 'POST':
        filters = request.body
        filters = json.loads(filters)
        print filters
        filter_dict = defaultdict(list)
        category = '{0} {1}'.format(product_category, product_type)
        filter_dict['category__category_name'] = category
        for f in filters:
            print "jjkhhhkj"
            if f is not None:
                if f['key'] == 'sub_categories':
                    key = '{0}__sub_type__in'.format(f['key'].lower())
                    filter_dict[key].append(f['value'])

                else:
                    key = '{0}__name__in'.format(f['key'].lower())
                    filter_dict[key].append(f['value'])
        print filter_dict
        try:
            products = Product.objects.filter(**filter_dict).distinct()
        except Product.DoesNotExist:
            return Response("Not Found")
        print products
        product_serialized = ProductsListSerializer(products, many=True)
        return Response(product_serialized.data)


@permission_classes((AllowAny,))
@api_view(['GET'])
def product_details(request, product_type, product_category, product_id):
    try:
        product_detail = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    product_serializer = ProductSerializer(product_detail)
    return Response(product_serializer.data)

@permission_classes((AllowAny,))
@api_view(['GET'])
def filter_list(request, product_type, category):
    try:
        catg = '{0} {1}'.format(category, product_type)
        brand = Brand.objects.all()
        color = Colour.objects.all()

        size = Size.objects.filter(category__category_name=catg)
        categories = Category.objects.filter(type=product_type)

        sub_catg = SubCategory.objects.filter(category__category_name=catg).values_list('type').distinct()
        #sub_catg1 = SubCategory.objects.filter(category__category_name=catg)
        #print sub_catg1
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    size = SizeSerializer(size, many=True)
    sub_catg_serializer = SubCategorySerializer(sub_catg, many=True)
    color = ColourSerializer(color, many=True)
    brand = BrandSerializer(brand, many=True)
    categories = CategorySerializer(categories, many=True)
    print color.data
    print brand.data[0]
    context = {}
    context['Brand'] = brand.data
    context['Colour'] = color.data
    context['Size'] = size.data
    context['Category'] = categories.data
    for sub in sub_catg:
        sub_type = SubCategory.objects.filter(category__category_name=catg, type=sub[0])
        context[sub[0]] = SubCategorySerializer(sub_type, many=True).data

    return Response(context)

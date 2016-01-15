import json

from collections import defaultdict

from django.http import HttpResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from app.products.models import Product, Size
from app.products.serializers import ProductsListSerializer, ProductSerializer, SizeSerializer, ProductBrandSerializer, ProductColourSerializer
from app.sub_categories.models import SubCategory
from app.sub_categories.serializers import SubCategorySerializer


# Create your views here.


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



@api_view(['GET'])
def product_details(request, product_type, product_category, product_id):
    try:
        product_detail = Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    product_serializer = ProductSerializer(product_detail)
    return Response(product_serializer.data)


@api_view(['GET'])
def filter_list(request, product_type, category):
    try:
        catg = '{0} {1}'.format(category, product_type)
        brand = Product.objects.filter(category__category_name=catg)
        size = Size.objects.filter(category__category_name=catg)
        print size

        sub_catg = SubCategory.objects.filter(category__category_name=catg).values_list('type').distinct()
        sub_catg1 = SubCategory.objects.filter(category__category_name=catg)
        print sub_catg1
    except Product.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND)

    size = SizeSerializer(size, many=True)
    sub_catg_serializer = SubCategorySerializer(sub_catg, many=True)
    color = ProductColourSerializer(brand, many=True)
    brand = ProductBrandSerializer(brand, many=True)
    print brand.data
    context = {}
    context['Brand'] = brand.data[0]
    context['Colour'] = color.data[0]
    context['Size'] = size.data
    for sub in sub_catg:
        print sub[0]
        sub_type = SubCategory.objects.filter(category__category_name=catg, type=sub[0])
        print sub_type
        context[sub[0]] = SubCategorySerializer(sub_type, many=True).data

    return Response(context)

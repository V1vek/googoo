import logging

from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

from app.wishlists.models import Wishlist
from app.products.models import Product
from app.categories.models import Category
from app.customer.models import Customer
from app.retailer.models import Retailer
from app.products.serializers import ProductSerializer
from app.wishlists.serializers import WishlistSerializer

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


@login_required
def index(request):
    context = {}
    context['request'] = request
    context['user'] = request.user
    user_id = request.user.id
    wishlists = Wishlist.objects.filter(user_id=user_id)

    context['books'] = Products.objects.filter(id__in=[wishlist.book_id for wishlist in wishlists])
    context['count'] = len(context['books'])
    context['categories_all'] = Category.objects.all()  # categories data for menu

    try:
        context['customer'] = Customer.objects.get(profile=request.user)
    except Customer.DoesNotExist:
        context['customer'] = None

    try:
        context['retailer'] = Retailer.objects.get(profile=request.user)
    except Customer.DoesNotExist:
        context['retailer'] = None

    return render(request, 'wishlists/index.html', context)


@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['GET'])
def wishlists_list(request):
    if request.method == 'GET':
        wishlists = Wishlist.objects.all()
        wishlists_serializer = WishlistSerializer(wishlists, many=True)
        return Response(wishlists_serializer.data)


@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def add_to_wishlist(request):
    if request.method == 'POST':
        if request.user.is_authenticated():
            data = JSONParser().parse(request)
            if data['book_id'] is not None:
                book_id = int(data['book_id'])
                try:
                    book = Products.objects.get(id=book_id)
                except Wishlist.DoesNotExist:
                    return HttpResponse(status=status.HTTP_404_NOT_FOUND)

                wishlist, created = Wishlist.objects.update_or_create(book=book, user=request.user)
                book_serializer = BookSerializer(book)
                if wishlist.id is not None:
                    return Response({'wishlist_id': wishlist.id, 'created': created,'book':book_serializer.data}, status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Authentication Failed'})


@login_required
@authentication_classes((JSONWebTokenAuthentication,))
@permission_classes((IsAuthenticated,))
@api_view(['POST'])
def remove_from_wishlist(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        book_id = int(data['book_id'])
        user_id = int(data['user_id'])

        try:
            wishlist = Wishlist.objects.get(book_id=book_id, user_id=user_id)
        except Wishlist.DoesNotExist:
            return HttpResponse(status=status.HTTP_404_NOT_FOUND)

        if wishlist is not None:
            wishlist.delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)

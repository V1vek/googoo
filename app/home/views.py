import logging

from django.shortcuts import render
from django.http import HttpResponse

from app.categories.models import Category

log = logging.getLogger(__name__)


def index(request):
    context = {}
    context['request'] = request
    context['user'] = request.user
    return HttpResponse("Hello, world. You're at the polls index.")
    # return render(request, 'home/index.html', {'context': context})


def faq(request):
    context = {}
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()  # categories data for menu
    return render(request, 'home/faq.html', {'context': context})


def about(request):
    context = {}
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()  # categories data for menu
    log.info(context['categories_all'])
    return render(request, 'home/about.html', {'context': context})


def terms_and_conditions(request):
    context = {}
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()  # categories data for menu
    return render(request, 'home/terms_and_conditions.html', {'context': context})

import os
import json
import logging
import hashlib
import datetime
import random
from django.views.decorators.csrf import csrf_exempt,csrf_protect

from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from django.db import IntegrityError
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.shortcuts import redirect

from django.template.loader import render_to_string

from models import User
from app.customer.models import Customer
from app.retailer.models import Retailer
from app.categories.models import Category
from app.order_items.models import OrderItem
from app.orders.helpers import get_cart_details
from jwt_helper import get_json_web_token

log = logging.getLogger(__name__)


@login_required
def profile(request):
    context = {}
    str_title=""
    context['request'] = request
    context['user'] = request.user
    context['categories_all'] = Category.objects.all()
    context['is_current_user'] = True
    context = get_cart_details(request, context)
    str_title= "Profile-"+context['user'].first_name+" "+context['user'].last_name
    context['page_title'] = str_title

    try:
        context['customer'] = Customer.objects.get(profile=context['user'].id)
    except Customer.DoesNotExist:
        context['customer'] = None

    try:
        context['retailer'] = Retailer.objects.get(profile=context['user'].id)
    except Retailer.DoesNotExist:
        context['retailer'] = None

    if request.GET.get('created_profile') and context['customer'] and context['retailer'] is None:
        context['show_buyer_profile_warning'] = True

    try:
        products_bought = OrderItem.objects.filter(order__user=request.user, order_status=3)
        context['products_bought'] = len(products_bought)
    except Exception as e:
        log.info("Exception : {0}".format(e))
        context['products_bought'] = 0

    return render(request, 'accounts/profile.html', context)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
def change_password(request):
    if request.method == 'POST':
        data = JSONParser().parse(request)

        old_password = data['old_password']
        new_password = data['new_password']
        new_password1 = data['new_password1']
        if old_password is None:
            return Response({"validation": "password is not valid ", "status": "error"})

        if new_password != new_password1:
            return Response({"validation": "passwords doesn't match", "status": "error"})

        user = authenticate(username=request.user.username, password=old_password)
        if user is not None:
            user.set_password(new_password)
            user.save()
            email_subject = 'Password changed for your account!'
            message = render_to_string('email/password_changed.html', {'user': user})
            msg = EmailMultiAlternatives(subject=email_subject, body=message,
                                         from_email="admin@textnook.com", to=[user.email])
            # --------------------------------------------- change this --------------------------------
            msg.attach_alternative(message, "text/html")
            msg.send()
            return Response({"message": "password changed successfully", "status": "success"})
        else:
            return Response({"validation": "password is not valid ", "status": "error"})


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
def get_token(request):
    token = None
    if request.method == 'GET':
        if request.user is not None:
            token = get_json_web_token(request.user)
    return Response({'token': token})


@csrf_protect
@api_view(['POST'])
@permission_classes((AllowAny,))
def signup_user(request):
    print request
    if request.method == 'POST':
        print request.POST
        email = request.POST.get('email')
        username = email
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        is_retailer = request.POST.get('is_retailer')

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if email is None:
            return HttpResponse(json.dumps([{"validation": "Email cannot be empty"}]),
                                content_type="application/json")

        if password != confirm_password:
            return HttpResponse(json.dumps([{"validation": "passwords doesn't match"}]),
                                content_type="application/json")
        try:
            user = User.objects.create_user(username, email, first_name, last_name, password, is_retailer)
        except IntegrityError:
            message = {}
            message['validation'] = "Email Id already exist."
            return Response({'message': message})

        if user is not None and user.is_active:
            user = authenticate(username=email, password=password)
            verify_email(user)
            message = {
                'status': 'success',
                'validation': 'Verification email has been sent to your email. Please verify your account.'
            }
            return Response({'message': message})
        else:
            message={}
            message['validation'] = "something went wrong"

            return Response({'message': message})
            # return render(request, 'accounts/signup.html', {'message': message})


def verify_email(user):
    email = user.email

    salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
    activation_key = hashlib.sha1(email+salt).hexdigest()

    user.activation_key = activation_key
    user.key_expires = timezone.now()
    user.save()
    email_subject = 'Activate your account.'
    activation_url = "{1}/accounts/confirm_email/{0}".format(activation_key, os.environ.get('HOST_NAME'))

    render = render_to_string('email/verify_email.html', {'user': user, 'activation_url': activation_url})
    msg = EmailMultiAlternatives(subject=email_subject, body=render,
                                 from_email="nivethithav11@gmail.com", to=[email])
    # ------------------ change this --------------------------------------------------------
    msg.attach_alternative(render, "text/html")
    msg.send()
    response = msg.mandrill_response[0]
    mandrill_status = response['status']
    return mandrill_status


@api_view(['POST'])
@permission_classes((AllowAny,))
def verify_email_api(request):
    # data = JSONParser().parse(request)
    email = request.POST.get('email')

    try:
        user = User.objects.get(email=email)
        verify_email(user)
        message = {'status': 'success',
                   'validation': 'Verification Email is sent to your email.'}
        return Response({'message': message})
    except User.DoesNotExist:
        message = {'status': 'error',
                   'validation': 'Email id is not registered. Please enter the valid email id.'}
        return Response({'message': message})


@api_view(['POST'])
@permission_classes((AllowAny,))
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)

        if user is not None and user.is_active:
            if not user.is_email_verified:
                message = {'status': 'error',
                           'validation': 'Email not verified. Please check your email.'}
                return Response({'message': message})

            auth_login(request, user)
            token = get_json_web_token(user)
            return Response({'token': token})
        else:
            message={}
            message['validation'] = "Incorrect Email or Password"
            return Response({'message': message})


def resend_verification_email(request):
    return render(request, 'accounts/resend_verification_email.html')


def confirm_email(request, key):
    try:
        user = User.objects.get(activation_key=key)
    except User.DoesNotExist:
        return render(request, 'accounts/invalid_url.html')

    if (user.key_expires + datetime.timedelta(days=2)) < timezone.now():
        return render(request, 'accounts/confirm_expired.html')

    user.is_email_verified = 1
    user.is_active = True
    user.save()
    email_subject = 'Welcome !'
    message = render_to_string('email/email_verified.html', {'user': user})
    msg = EmailMultiAlternatives(subject=email_subject, body=message,
                                 from_email="admin@textnook.com", to=[user.email,"service@textnook.in"])
    # -------------------------------- change -----------------------------------
    msg.attach_alternative(message, "text/html")
    msg.send()
    response = msg.mandrill_response[0]
    return redirect('/?email_verified=true')


@api_view(['POST'])
@permission_classes((AllowAny,))
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(email+salt).hexdigest()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': "Email Id Doesn't exist"})
        user.reset_password_key = activation_key
        user.save()

        email_subject = 'Reset Password.'
        activation_url = "{1}/accounts/reset_password/{0}".format(activation_key, os.environ.get('HOST_NAME'))

        render = render_to_string('email/reset_password.html', {'user': user, 'activation_url': activation_url})
        msg = EmailMultiAlternatives(subject=email_subject, body=render,
                                     from_email="admin@textnook.com", to=[email])
        #  ------------------------------- change this -----------------------------------------------------
        msg.attach_alternative(render, "text/html")
        msg.send()
        response = msg.mandrill_response[0]
        mandrill_status = response['status']
        return Response({'status': 'success', 'message': "Email has been sent with the details for resetting password"})


@api_view(['POST'])
@permission_classes((AllowAny,))
def update_new_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        key = request.POST.get('key')

        if password != confirm_password:
            return Response({"message": "passwords doesn't match", "status": "error"})

        try:
            user = User.objects.get(reset_password_key=key)
        except User.DoesNotExist:
            return Response({'status': 'error', 'message': "Invalid URL"})

        if user is not None:
            user.set_password(password)
            user.reset_password_key = ''
            user.save()
            email_subject = 'Password changed for your account!'
            message = render_to_string('email/password_changed.html', {'user': user})
            msg = EmailMultiAlternatives(subject=email_subject, body=message,
                                         from_email="admin@textnook.com", to=[user.email])
            # ----------------------------- change this -------------------------------------
            msg.attach_alternative(message, "text/html")
            msg.send()
            return Response({"message": "password updated successfully", "status": "success"})

        else:
            return Response({"message": "password is not valid ", "status": "error"})


def reset_password(request, key):
    context = {}
    context['key'] = key
    return render(request, 'accounts/reset_password.html', context)



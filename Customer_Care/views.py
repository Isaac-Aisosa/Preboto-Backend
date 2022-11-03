from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics
from django.contrib.auth.models import User
from rest_framework import status
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_customer_service(request):
    mobile = Contact.objects.get(active=True)
    whatsapp = Whatsapp.objects.get(active=True)
    email = Email.objects.get(active=True)
    social = Social.objects.get(active=True)
    return Response({
        'mobile1': mobile.customerLine1,
        'mobile2': mobile.customerLine2,
        'whatsapp': whatsapp.customerCare,
        'email': email.customerEmail1,
        'facebook': social.facebook,
        'instagram': social.instagram,
        'youtube': social.youtube,
        'twitter': social.twitter,
        'tiktok': social.tiktok,

    })

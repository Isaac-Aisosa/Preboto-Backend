from django.contrib.auth import authenticate, login
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.authentication import SessionAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.exceptions import NotAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated

from .models import UserProfile
from .serializers import UserProfileSerializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions, generics
from django.contrib.auth.models import User
from rest_framework import status
from django.http import Http404
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import UserSerializer


# Create your views here.

class UserCreate(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class Email_check(ObtainAuthToken):
   
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        users = User.objects.filter(email=email)
        if users.exists():
            return Response(status=status.HTTP_409_CONFLICT)
        else:
            # print('no current trade is opened')
            return Response(status=status.HTTP_200_OK)


class AuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'username': user.username,
            'firstname': user.first_name,
            'lastname': user.last_name
        })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    userprofile = UserProfile.objects.get(user=request.user)
    serializer = UserProfileSerializers(userprofile, many=False)
    return Response(serializer.data)


class UpdateProfile(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        phone = request.data['phone']
        profile = UserProfile.objects.get(user=request.user)
        profile.Phone = phone
        profile.save()
        return Response(status=status.HTTP_201_CREATED)

from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token


# Create your views here.
class FacebookLoginView(generics.GenericAPIView):
    def post(self, request):
        username = request.data['userID']
        password = request.data['userID']
        email = request.data['email']

        if not User.objects.filter(username=username).exists():
            user = User.objects.create(username=username,
                                       password=password, email=email)
            user_token = Token.objects.create(user=user)

            return Response({'auth_token': user_token.key}, status=status.HTTP_201_CREATED)

        user = User.objects.get(username=username)
        user_token = Token.objects.get(user=user.pk)

        return Response({'auth_token': user_token.key}, status=status.HTTP_200_OK)


class ValidateUserTokenView(generics.GenericAPIView):
    def post(self, request):
        token = Token.objects.filter(key=request.data['auth_token'])

        if not token.exists():
            return Response({'error': 'Invalid user token'}, status=status.HTTP_404_NOT_FOUND)

        return Response({'auth_token': token[0].key}, status=status.HTTP_200_OK)
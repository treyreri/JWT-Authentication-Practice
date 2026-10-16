from django.shortcuts import render

from django.contrib.auth import get_user_model
from rest_framework import generics, permissions,status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from .serializers import RegisterSerializer

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class MeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        return Response({
            "id" : request.user.id ,
            "username" : request.user.username ,
        })

class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")

        if not refresh_token:
            return Response(
                { "detail" : "Refresh token is required" } ,
                status = status.HTTP_400_BAD_REQUEST, )
        try :
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {"detail" : "Logout successful"} ,
                status = status.HTTP_205_RESET_CONTENT, )
        except TokenError:
            return Response(
                {"detail" : "Invalid or expired refresh token"} ,
                status = status.HTTP_400_BAD_REQUEST,)
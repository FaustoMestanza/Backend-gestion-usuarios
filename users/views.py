from django.shortcuts import render

# Create your views here.

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import LoginSerializer, UserSerializer

class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]        # login es público
    serializer_class = LoginSerializer

class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]        # refresh es público

class MeView(APIView):
    permission_classes = [IsAuthenticated] # requiere Bearer access

    def get(self, request):
        return Response(UserSerializer(request.user).data)

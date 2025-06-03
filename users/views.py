from django.shortcuts import render
from .models import CustomUser
from .serializers import CustomUserSerializer, LoginSerializer
from rest_framework.generics import CreateAPIView,GenericAPIView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib import messages
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError


# Create your views here.

# User Registration
@method_decorator(csrf_exempt, name='dispatch')
class UserRegistrationAPIView(CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args , **kwargs):
        serializer = self.get_serializer(data = request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            password = validated_data.pop('password')
            user = CustomUser(**validated_data)
            user.set_password(password)
            user.is_active = True
            user.save()
            response_serializer = self.get_serializer(user)
            return Response({"success": "Registration successful.","user":response_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'errors':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

##User Login
@method_decorator(csrf_exempt, name='dispatch')
class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]

        user = authenticate(username=email, password=password)
        if not user:
            return Response({"error": "Invalid username or password"}, status=status.HTTP_400_BAD_REQUEST)

        response = Response({"message": "Login successful.", 
        "user":{
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "is_active": user.is_active}}
        , status=status.HTTP_200_OK)

        messages.success(request, "Login successful!")
        
        # Generate JWT tokens
        refresh  = RefreshToken.for_user(user)
        access_token = refresh.access_token

        print('access_token-', access_token)

        # Set Refresh Token in a cookie 
        response.set_cookie(
            key="refresh_token",
            value=str(refresh),
            httponly=True,  # Prevent JavaScript access
            secure=True,  # Send only over HTTPS
            samesite='Strict',  # Prevent CSRF attacks
        )
        # Set Access Token in a cookie 
        response.set_cookie(
            key="access_token",
            value=str(access_token),
            httponly=True,  # Prevent JavaScript access
            secure=True,  # Send only over HTTPS
            samesite='Strict',
        )

        return response

#User logout
class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can log out

    def post(self, request):
        # Extract tokens from cookies
        refresh_token = request.COOKIES.get("refresh_token")

        if not refresh_token:
            return Response({"error": "No refresh token found"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            # Blacklist the refresh token
            RefreshToken(refresh_token).blacklist()
        except TokenError:
            pass  # Ignore if it's already blacklisted or invalid

        # Clear cookies
        response = Response({"message": "Logged out successfully."},status=status.HTTP_200_OK)
        response.delete_cookie("access_token")
        response.delete_cookie("refresh_token")

        return response

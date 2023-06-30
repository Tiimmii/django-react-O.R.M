from django.shortcuts import render
from .models import Jwt
from customuser.models import Customuser
from .serializers import LoginSerializer, RegisterSerializer
from django.contrib.auth import authenticate
from .authentication import Get_token, Authentication
from rest_framework.response import Response
from rest_framework.views import APIView
# Create your views here.

class Registerview(APIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        Customuser.objects.create_user(**serializer.validated_data)
        user = Customuser.objects.get(email=serializer.validated_data["email"])

        access = Get_token.get_access_token({"user": user.id})
        refresh = Get_token.get_refresh_token()

        Jwt.objects.create(user=user, access_token=access, refresh_token=refresh)

        return Response({"message": "User created successfully"}, status="200")
    
class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(email=serializer.validated_data["email"], password=serializer.validated_data["password"])
        if not user:
            return Response({"message": "invalid email or password"}, status = "400")
        logged_in_user = Customuser.objects.get(email = serializer.validated_data['email'])
        try:
            active_jwt = Jwt.objects.get(user = logged_in_user)
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")
        
        if not Authentication.valid_token(active_jwt.refresh_token):
            print(Authentication.valid_token(active_jwt.refresh_token))
            access_token = Get_token.get_access_token({"user_id": active_jwt.user.id})
            refresh_token = Get_token.get_refresh_token()

            active_jwt.access_token = access_token
            active_jwt.refresh_token = refresh_token
            active_jwt.save()

            return Response({"message": "new token given"})

        return Response({"message": "Logged in successfully"})
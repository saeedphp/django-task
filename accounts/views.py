import random

from django.contrib.auth import login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from utils import send_otp_code
from .models import OtpCode, User
from .serializers import UserRegisterSerializer, UserLoginSerializer, UserVerifySerializer


# Create your views here.

class UserRegisterView(APIView):
    """
    This api view is used to register a new user,
    Should pass email, phone_number, full_name and password to create a new user
    """

    serializer_class = UserRegisterSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            data = ser_data.validated_data
            User.objects.create_user(phone_number=data['phone_number'], full_name=data['full_name'], email=data['email'], password=data['password'])
            return Response(ser_data.data, status=status.HTTP_201_CREATED)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    """
    This api view is used to login a user,
    send otp code
    """
    serializer_class = UserLoginSerializer

    def post(self, request):
        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            random_code = random.randint(1000, 9999)
            OtpCode.objects.create(phone_number=ser_data.validated_data['phone_number'], code=random_code)
            send_otp_code(phone_number=ser_data.data['phone_number'], code=random_code)
            request.session['user'] = {
                'phone_number': ser_data.data['phone_number'],
                'password': ser_data.data['password'],
            }
            return redirect('accounts:verify')
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)


class UserVerifyView(APIView):
    """
    This api view is used to verify a user
    get otp code and get user token
    """
    serializer_class = UserVerifySerializer

    def get(self, request):
        user_info = request.session.get('user')
        if not user_info:
            return Response({'message': 'Session expired or user not found'}, status=status.HTTP_400_BAD_REQUEST)

        return Response({'message': 'Enter the OTP code sent to your phone number'}, status=status.HTTP_200_OK)

    def post(self, request):
        user_info = request.session.get('user')
        if not user_info:
            return Response({'message': 'Session expired or user not found'}, status=status.HTTP_400_BAD_REQUEST)

        ser_data = self.serializer_class(data=request.data)
        if ser_data.is_valid():
            try:
                code_instance = OtpCode.objects.get(phone_number=user_info['phone_number'])
            except OtpCode.DoesNotExist:
                return Response({'message': 'OTP not found'}, status=status.HTTP_400_BAD_REQUEST)

            if ser_data.data['code'] == code_instance.code:
                user = authenticate(request, phone_number=user_info['phone_number'], password=user_info['password'])
                if user is not None:
                    login(request, user)
                    refresh = RefreshToken.for_user(user)
                    del request.session['user']
                    code_instance.delete()
                    return Response({'refresh': str(refresh), 'access': str(refresh.access_token)}, status=status.HTTP_200_OK)
                return Response({'message': 'Invalid phone number or password'}, status=status.HTTP_401_UNAUTHORIZED)
            return Response({'message': 'Code does not match'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ser_data.errors, status=status.HTTP_400_BAD_REQUEST)



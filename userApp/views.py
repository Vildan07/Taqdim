import token
from io import BytesIO

import qrcode

from django.http import FileResponse
from django.contrib.auth import authenticate

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from .permissions import IsOwnerOrReadOnly
from .models import *
from .serializers import *


# class UserRegistrationView(generics.GenericAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserRegistrationSerializer
#
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save(request.user)
#
#         return Response({
#             "user": UserSerializer(user, context=self.context).data, "message": "Пользователь успешно создан"
#         }, status=status.HTTP_201_CREATED)


def generate_jwt_token(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)

    }


class UserLoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user is not None:
            # Создайте свой токен или используйте стороннюю библиотеку
            token = generate_jwt_token(user)
            return Response({'token': token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неправильные учетные данные'}, status=status.HTTP_401_UNAUTHORIZED)


import qrcode
from io import BytesIO
from django.http import HttpResponse
from rest_framework.views import APIView
from PIL import Image, ImageDraw


class QRCodeAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, username):
        # Формируем нужную ссылку
        url = f"https://taqdim.uz/{username}/"

        # Создаем QR-код
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")


        # Добавляем логотип или текст (по желанию)
        # ... (код для добавления логотипа или текста)

        # Преобразуем изображение в байты и отправляем в ответе
        buffer = BytesIO()
        img.save(buffer, 'PNG')
        buffer.seek(0)

        return HttpResponse(buffer.getvalue(), content_type='image/png')

# class QRCodeAPIView(APIView):
#     def get(self, request, username):
#         user = get_object_or_404(User, username=username)
#         serializer = UserSerializer(user)
#         user_data = serializer.data
#
#         qr = qrcode.QRCode(
#             version=1,
#             error_correction=qrcode.constants.ERROR_CORRECT_L,
#             box_size=10,
#             border=4,
#         )
#
#         qr.add_data(user_data)
#         qr.make(fit=True)
#
#         img = qr.make_image(fill_color="black", back_color="white")
#         buffer = BytesIO()
#         img.save(buffer, 'PNG')
#         buffer.seek(0)
#
#         file_path = f"{username}_qrcode.png"
#         with open(file_path, 'wb') as f:
#             f.write(buffer.getvalue())
#
#         response = FileResponse(open(file_path, 'rb'), content_type='image/png')
#         response['Content-Disposition'] = f'attachment; filename="{file_path}"'
#
#         return response


class UserDetail(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]



from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate, login
from .serializers import UserSerializer

from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .serializers import UserSerializer

from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])

        if user:
            if user.is_active:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            else:
                return Response({'message': 'Пользователь неактивен.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'Неверные логин или пароль.'}, status=status.HTTP_400_BAD_REQUEST)


class RegisterView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        if user:
            login(request, user)
            return Response({
                'message': 'Пользователь успешно зарегистрирован.'
            }, status=status.HTTP_201_CREATED)
        return Response({
            'message': 'Ошибка регистрации.'
        }, status=status.HTTP_400_BAD_REQUEST)

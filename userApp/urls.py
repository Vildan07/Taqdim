from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token-refresh/', TokenRefreshView.as_view()),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),

    # path('register/', UserRegistrationView.as_view()),
    # path('login/', UserLoginView.as_view()),
    path('<str:username>/', QRCodeAPIView.as_view()),
    path('users/me/<int:pk>/', UserDetail.as_view()),
]

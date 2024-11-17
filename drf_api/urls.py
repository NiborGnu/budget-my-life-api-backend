from django.contrib import admin
from django.urls import path, include
from users.views import CreateUserView
from .views import root_route
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)


urlpatterns = [
    path(
        '',
        root_route
    ),
    path(
        'admin/',
        admin.site.urls
    ),
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='get_token'
    ),
    path(
        'token/refresh/',
        TokenRefreshView.as_view(),
        name='refresh_token'
    ),
    path(
        'auth/',
        include('rest_framework.urls'),
        name='auth'
    ),
    path(
        'register/',
        CreateUserView.as_view(),
        name='register'
    ),
    path(
        'users/',
        include('users.urls'),
    ),
    path(
        'transactions/',
        include('transactions.urls'),
    ),
    path(
        'categories/',
        include('categories.urls'),
    ),
    path(
        'budgets/',
        include('budgets.urls'),
    ),
]
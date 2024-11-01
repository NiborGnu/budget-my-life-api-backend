from django.contrib import admin
from django.urls import path, include
from .views import root_route


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
        'api-auth/',
        include('rest_framework.urls')
    ),
    path(
        'dj-rest-auth/',
        include('dj_rest_auth.urls')
    ),
    path(
        'dj-rest-auth/register/',
        include('dj_rest_auth.registration.urls'),
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
]
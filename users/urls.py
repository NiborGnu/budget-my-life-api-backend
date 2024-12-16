from django.urls import path
from users import views


urlpatterns = [
    path(
        'profiles/',
        views.ProfileList.as_view()
    ),
    path(
        'profiles/<int:pk>/',
        views.ProfileDetail.as_view()
    ),
    path(
        'profile/',
        views.UserProfileView.as_view(),
        name='user-profile'
    ),
    path(
        'change-password/',
        views.ChangePasswordView.as_view(),
        name='change-password'
    ),
    path(
        'check-username/',
        views.CheckUsernameView.as_view(),
        name='check-username'
    ),
    path(
        'delete-profile/',
        views.DeleteProfileView.as_view(),
        name='delete-profile'
    ),
]

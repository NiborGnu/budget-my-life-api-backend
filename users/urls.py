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
]

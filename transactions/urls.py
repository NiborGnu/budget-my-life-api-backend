from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.TransactionList.as_view(),
        name='transaction-list'
    ),
    path(
        '<int:pk>/',
        views.TransactionDetail.as_view(),
        name='transaction-detail'
    ),
]

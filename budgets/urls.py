from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.BudgetListCreate.as_view(),
        name='budget-list-create'
    ),
    path(
        '<int:pk>/',
        views.BudgetDetail.as_view(),
        name='budget-detail'
    ),
]
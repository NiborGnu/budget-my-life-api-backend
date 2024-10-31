from django.urls import path
from . import views

urlpatterns = [
    path(
        '',
        views.CategoryListCreate.as_view(),
        name='category-list-create'
    ),
    path(
        '<int:pk>/',
        views.CategoryDetail.as_view(),
        name='category-detail'
    ),
    path(
        '<str:category_type>/subcategories/',
        views.SubCategoryListCreate.as_view(),
        name='subcategory-list-create'
    ),
    path(
        'subcategories/<int:pk>/',
        views.SubCategoryDetail.as_view(),
        name='subcategory-detail'
    ),
]

from django.contrib import admin
from django.urls import path
from .views import ProductsViewSet

urlpatterns = [
    path('products', ProductsViewSet.as_view({
        'get': 'list',
        'post': 'create',
    })),
    path('products/<str:pk>', ProductsViewSet.as_view({
        'get': 'retrieve',
        'put': 'update',
        'delete': 'destroy',
    })),
]

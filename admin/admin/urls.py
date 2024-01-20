from django.contrib import admin
from django.urls import path, include
from products.views import index 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('products.urls')),
    path('index/', index, name='index'),
    path('', index, name='home'),
]

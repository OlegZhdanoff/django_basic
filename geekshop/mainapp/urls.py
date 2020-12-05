from django.urls import path
from mainapp.views import index, products

urlpatterns = [
    path('', index),
    path('products/', products),
]

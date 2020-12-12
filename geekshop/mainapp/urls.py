from django.urls import path
from mainapp.views import index, products, import_products

app_name = 'mainapp'

urlpatterns = [
    path('', index),
    path('products/', products, name='products'),
    path('import_products/', import_products, name='import_products')
]

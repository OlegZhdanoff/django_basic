from django.urls import path
from mainapp.views import index, products, import_products, get_category

app_name = 'mainapp'


urlpatterns = [
    path('', index, name='index'),
    path('products/', products, name='products'),
    path('import_products/', import_products, name='import_products'),
    # path('category/<int:category_id>/', products, name='category'),
    path('<int:category_id>/<int:page>/', products, name='page')
]

from django.urls import path
import mainapp.views as mainapp

app_name = 'mainapp'


urlpatterns = [
    path('', mainapp.index, name='index'),
    path('products/<category_id>/', mainapp.ProductListView.as_view(), name='products'),
    path('products/', mainapp.ProductListView.as_view(), name='products'),
    path('import_products/', mainapp.import_products, name='import_products'),
    # path('category/<int:category_id>/', products, name='category'),
    # path('<int:category_id>/<int:page>/', products, name='page')
]

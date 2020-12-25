from django.urls import path

import adminapp.views as adminapp

app_name = 'adminapp'

urlpatterns = [
    path('', adminapp.index, name='index'),
    path('users/', adminapp.admin_users, name='admin_users'),
    path('users/create/', adminapp.admin_users_create, name='admin_users_create'),
    path('users/update/<int:user_id>/', adminapp.admin_users_update, name='admin_users_update'),
    path('users/remove/<int:user_id>/', adminapp.admin_users_remove, name='admin_users_remove'),
    path('products/', adminapp.admin_products, name='admin_products'),
    path('products/create/', adminapp.admin_products_create, name='admin_products_create'),
    path('products/update/<int:user_id>/', adminapp.admin_products_update, name='admin_products_update'),
    path('products/remove/<int:user_id>/', adminapp.admin_products_remove, name='admin_products_remove'),
]

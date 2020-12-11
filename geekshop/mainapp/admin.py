from django.contrib import admin
from mainapp.models import ProductCategory, Products


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'short_description')
    list_display_links = ('id', 'title')
    search_fields = ('title',)


class ProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category')
    list_display_links = ('id', 'name')
    search_fields = ('name', 'category')
    list_filter = ('category',)


admin.site.register(ProductCategory, ProductCategoryAdmin)
admin.site.register(Products, ProductsAdmin)


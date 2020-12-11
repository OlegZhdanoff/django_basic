from django.shortcuts import render
from mainapp.services import load_content_from_file
from mainapp.models import Products, ProductCategory


def index(request):
    return render(request, template_name='mainapp/index.html', context=load_content_from_file('index.json'))


def products(request):
    goods = Products.objects.all()
    categories = ProductCategory.objects.all()
    content = {
        'title': '- Каталог',
        'product_list': goods,
        'categories': categories
    }
    return render(request, template_name='mainapp/products.html', context=content)


def category(request):
    return render(request, 'mainapp/products.html')

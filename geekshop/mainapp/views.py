from django.shortcuts import render
from mainapp.services import load_content_from_file


def index(request):
    return render(request, template_name='mainapp/index.html', context=load_content_from_file('index.json'))


def products(request):
    return render(request, template_name='mainapp/products.html', context=load_content_from_file('products.json'))

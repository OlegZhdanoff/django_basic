from django.shortcuts import render
from mainapp.services import load_content_from_file, load_product_to_db
from mainapp.models import Products, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def index(request):
    return render(request, template_name='mainapp/index.html', context=load_content_from_file('index.json'))


def products(request, category_id=6, page=1):
    if category_id and category_id != 6:
        goods = Products.objects.filter(is_visible=True, category=category_id).order_by('price')
    else:
        goods = Products.objects.filter(is_visible=True).order_by('price')

    categories = ProductCategory.objects.filter(is_visible=True)
    paginator = Paginator(goods, settings.PAGE_ELEMS)
    try:
        goods_paginator = paginator.page(page)
    except PageNotAnInteger:
        goods_paginator = paginator.page(1)
    except EmptyPage:
        goods_paginator = paginator.page(paginator.num_pages)

    content = {
        'title': 'Каталог',
        'product_list': goods_paginator,
        'categories': categories,
        'category_id': category_id
    }
    return render(request, template_name='mainapp/products.html', context=content)


def get_category(request, category_id):
    goods = Products.objects.filter(is_visible=True, category=category_id)
    categories = ProductCategory.objects.filter(is_visible=True)
    content = {
        'title': 'Каталог',
        'product_list': goods,
        'categories': categories
    }
    return render(request, 'mainapp/products.html', context=content)


def import_products(request):
    load_product_to_db(load_content_from_file('products.json'), Products, ProductCategory)
    return render(request, template_name='mainapp/products.html')

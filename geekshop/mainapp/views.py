from django.shortcuts import render


def index(request):
    context = {'title': 'Geekshop',
               'content': 'Новые образы и лучшие бренды на GeekShop Store.\
                    Бесплатная доставка по всему миру! Аутлет: до -70% Собственный бренд. -20% новым покупателям.'}
    return render(request, template_name='mainapp/index.html', context=context)


def products(request):
    return render(request, template_name='mainapp/products.html')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponseRedirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView

from mainapp.models import Products
from basketapp.models import Basket


@login_required
def basket_add(request, id=None):
    product = get_object_or_404(Products, id=id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        basket = Basket(user=request.user, product=product)
    else:
        basket = baskets.first()
    basket.quantity += 1
    basket.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# class BasketAdd(LoginRequiredMixin, CreateView):
#     model = Basket
#     # success_url =
#
#     def get_success_url(self):
#         return self.request.META.get('HTTP_REFERER')

# @login_required
# def basket_remove(request, id=None):
#     basket = get_object_or_404(Basket, id=id)
#     basket.delete()
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# испльзуем миксин LoginRequiredMixin - то же что и декоратор @login_required
class BasketRemove(LoginRequiredMixin, DeleteView):
    model = Basket
    success_url = reverse_lazy('auth:profile')
    login_url = reverse_lazy('auth:login')

    # чтобы не было перехода на страницу с подтверждением удаления, переопределяем метод get на post
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        quantity = int(quantity)
        basket = Basket.objects.get(id=int(id))
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets,
        }
        result = render_to_string('basketapp/basket.html', context)
        return JsonResponse({'result': result})

from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from basketapp.models import Basket
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileForm
from authapp.models import ShopUser


class UserLoginView(LoginView):
    authentication_form = ShopUserLoginForm
    # redirect_authenticated_user = True
    success_url = reverse_lazy('mainapp:products')
    template_name = 'authapp/login.html'


# def login(request):
#     if request.method == 'POST':
#         form = ShopUserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST['username']
#             password = request.POST['password']
#             user = auth.authenticate(username=username, password=password)
#             if user and user.is_active:
#                 auth.login(request, user)
#                 return HttpResponseRedirect(reverse('mainapp:index'))
#     else:
#         form = ShopUserLoginForm()
#     context = {'form': form}
#     return render(request, 'authapp/login.html', context)


class UserRegisterView(CreateView):
    model = ShopUser
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')
    form_class = ShopUserRegisterForm


# def register(request):
#     if request.method == 'POST':
#         form = ShopUserRegisterForm(request.POST, request.FILES)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Вы успешно зарегистрировались!')
#             return HttpResponseRedirect(reverse('auth:login'))
#     else:
#         form = ShopUserRegisterForm()
#     context = {'form': form}
#     return render(request, 'authapp/register.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('mainapp:index'))


def edit(request):
    title = 'Редактирование'

    if request.method == 'POST':
        form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        form = ShopUserEditForm(instance=request.user)

    content = {'title': title, 'form': form}

    return render(request, 'authapp/edit.html', content)


class UserProfileView(UpdateView):
    model = ShopUser
    form_class = ShopUserProfileForm
    success_url = reverse_lazy('mainapp:index')
    template_name = 'authapp/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        baskets = Basket.objects.filter(user=self.request.user)
        context['title'] = 'Профиль ' + self.request.user.username
        context['baskets'] = baskets
        context['total_qty'] = baskets.first().total_qty()
        context['total_sum'] = baskets.first().total_sum()
        return context

    # def __init__(self, *args, **kwargs):
    #     print(self.success_url)
    #     super().__init__(*args, **kwargs)


# def profile(request):
#
#     if request.method == 'POST':
#         form = ShopUserProfileForm(request.POST, request.FILES, instance=request.user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('auth:profile'))
#     else:
#         form = ShopUserProfileForm(instance=request.user)
#
#     baskets = Basket.objects.filter(user=request.user)
#     title = 'Профиль ' + request.user.username
#     content = {'title': title, 'form': form, 'baskets': baskets, 'total_qty': baskets.first().total_qty(), 'total_sum':
#         baskets.first().total_sum()}
#     return render(request, 'authapp/profile.html', content)


from django.conf import settings
from django.core.mail import send_mail
from django.db import transaction
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView

from basketapp.models import Basket
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileForm, \
    ShopUserProfileEditForm
from authapp.models import ShopUser, ShopUserProfile

from django.shortcuts import get_object_or_404


class UserLoginView(LoginView):
    authentication_form = ShopUserLoginForm
    # redirect_authenticated_user = True
    success_url = reverse('mainapp:products')
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


# можно ли реализовать этот контроллер через CBV?
def verify(request, email, activation_key):
    try:
        # здесь почему то не могу использовать get_object_or_404, ругается что нет такого метода
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.activation_key = None
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return render(request, 'authapp/verification.html')

    except Exception as e:
        return HttpResponseRedirect(reverse('auth:login'))


class UserRegisterView(CreateView):
    model = ShopUser
    template_name = 'authapp/register.html'
    success_url = reverse_lazy('auth:login')
    form_class = ShopUserRegisterForm

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handle POST requests: instantiate a form instance with the passed
    #     POST variables and then check if it's valid.
    #     """
    #     form = self.get_form()
    #     if form.is_valid():
    #         return self.form_valid(form)
    #     else:
    #         return self.form_invalid(form)

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        self.object = form.save()
        self.send_verify_email()
        return super().form_valid(form)

    def send_verify_email(self):
        verify_link = reverse('auth:verify', args=[self.object.email, self.object.activation_key])
        subject = f'Подтверждение учетной записи {self.object.username}'
        message = f'Для подтверждения нажмите ссылку {settings.DOMAIN}{verify_link}'

        return send_mail(subject, message, settings.EMAIL_HOST_USER, [self.object.email], fail_silently=False)

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
        context['title'] = 'Профиль ' + self.request.user.username
        if self.request.POST:
            context['profile_form'] = ShopUserProfileEditForm(self.request.POST, instance=self.request.user.shopuserprofile)
        else:
            context['profile_form'] = ShopUserProfileEditForm(instance=self.request.user.shopuserprofile)

        return context

    # def post(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     return super().post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests: instantiate a form instance with the passed
        POST variables and then check if it's valid.
        """
        # self.object = None
        # form_class = self.get_form_class()
        # form = self.get_form(form_class)
        form = ShopUserProfileForm(request.POST, request.FILES, instance=request.user)

        profile_form = ShopUserProfileEditForm(self.request.POST, instance=self.request.user.shopuserprofile)
        print(form)
        print(form.is_valid(), profile_form.is_valid())
        # print(form_class)
        form.is_valid()
        # form.errors.pop('username')
        if form.is_valid() and profile_form.is_valid():
            return self.form_valid(form, profile_form)
        else:
            return self.form_invalid(form, profile_form)

    def form_valid(self, form, profile_form):
        """
        Called if all forms are valid. Creates a Author instance along
        with associated books and then redirects to a success page.
        """
        self.object = form.save()
        # profile_form.instance = self.object.shopuserprofile
        print(self.object.shopuserprofile)
        print(self.object)
        print(self.request.user)
        # profile_form.instance.user = self.request.user
        # profile_form.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, profile_form):
        """
        Called if whether a form is invalid. Re-renders the context
        data with the data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form, profile_form=profile_form)
        )


@transaction.atomic
def profile(request):

    if request.method == 'POST':
        form = ShopUserProfileForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if form.is_valid() and profile_form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:profile'))
    else:
        form = ShopUserProfileForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)

    # baskets = Basket.objects.filter(user=request.user)
    title = 'Профиль ' + request.user.username
    content = {'title': title, 'form': form, 'profile_form': profile_form}
    return render(request, 'authapp/profile.html', content)


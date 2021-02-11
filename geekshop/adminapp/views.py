from django.db import connection
from django.db.models import F
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.shortcuts import render, HttpResponseRedirect
# from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test
from django.views.generic.base import View

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.views.generic.list import ListView
from django.utils.decorators import method_decorator

from authapp.models import ShopUser
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm

from mainapp.models import Products, ProductCategory
from mainapp.forms import ProductCreateForm, ProductCategoryForm
from django.conf import settings


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/index.html')


class UserPassesTest(View):

    @method_decorator(user_passes_test(lambda u: u.is_superuser))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class UsersCreateView(CreateView, UserPassesTest):
    model = ShopUser
    template_name = 'adminapp/admin-users-create.html'
    success_url = reverse_lazy('admin_staff:admin_users')
    form_class = UserAdminRegisterForm


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
#     # C - Create
#     if request.method == 'POST':
#         form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#         else:
#             print(form.errors)
#     else:
#         form = UserAdminRegisterForm()
#     context = {'form': form}
#     return render(request, 'adminapp/admin-users-create.html', context)


class UsersListView(ListView, UserPassesTest):
    model = ShopUser
    template_name = 'adminapp/admin-users-read.html'
    paginate_by = settings.ADMIN_PAGE_ELEMS

    def get_queryset(self):
        return ShopUser.objects.all().order_by('username').select_related()


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
#     # R - Read
#     context = {
#         'users': ShopUser.objects.all(),
#     }
#     return render(request, 'adminapp/admin-users-read.html', context)


class UsersUpdateView(UpdateView, UserPassesTest):
    model = ShopUser
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users')
    form_class = UserAdminProfileForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'GeekShop - Редактирование пользователя'
        return context


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, user_id):
#     # U - Update
#     user = ShopUser.objects.get(id=user_id)
#     if request.method == 'POST':
#         form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
#         if form.is_valid():
#             form.save()
#             return HttpResponseRedirect(reverse('admin_staff:admin_users'))
#     else:
#         form = UserAdminProfileForm(instance=user)
#
#     context = {'form': form, 'user': user}
#     return render(request, 'adminapp/admin-users-update-delete.html', context)


class UserDeleteView(DeleteView, UserPassesTest):
    model = ShopUser
    template_name = 'adminapp/admin-users-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_users')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_remove(request, user_id):
#     user = ShopUser.objects.get(id=user_id)
#     # user.delete()
#     user.is_active = False
#     user.save()
#     return HttpResponseRedirect(reverse('admin_staff:admin_users'))


class ProductListView(ListView, UserPassesTest):
    model = Products
    template_name = 'adminapp/admin-products-read.html'
    paginate_by = settings.ADMIN_PAGE_ELEMS

    def get_queryset(self):
        return Products.objects.all().order_by('name').select_related()


class ProductCreateView(CreateView, UserPassesTest):
    model = Products
    template_name = 'adminapp/admin-products-create.html'
    success_url = reverse_lazy('admin_staff:admin_products')
    form_class = ProductCreateForm


class ProductUpdateView(UpdateView, UserPassesTest):
    model = Products
    template_name = 'adminapp/admin-products-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_products')
    form_class = ProductCreateForm


class ProductDeleteView(DeleteView, UserPassesTest):
    model = Products
    template_name = 'adminapp/admin-products-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_products')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_visible = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class CategoryListView(ListView, UserPassesTest):
    model = ProductCategory
    template_name = 'adminapp/admin-product_category-read.html'
    paginate_by = settings.ADMIN_PAGE_ELEMS

    def get_queryset(self):
        return ProductCategory.objects.all().order_by('title')


class CategoryCreateView(CreateView, UserPassesTest):
    model = ProductCategory
    template_name = 'adminapp/admin-product_category-create.html'
    success_url = reverse_lazy('admin_staff:admin_product_category')
    form_class = ProductCategoryForm


class CategoryUpdateView(UpdateView, UserPassesTest):
    model = ProductCategory
    template_name = 'adminapp/admin-product_category-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_product_category')
    form_class = ProductCategoryForm

    def form_valid(self, form):
        if 'discount' in form.cleaned_data:
            discount = form.cleaned_data['discount']
            if discount:
                self.object.products_set.update(price=F('price') * (1 - discount / 100))
                db_profile_by_type(self.__class__, 'UPDATE', connection.queries)

        return super().form_valid(form)


class CategoryDeleteView(DeleteView, UserPassesTest):
    model = ProductCategory
    template_name = 'adminapp/admin-product_category-update-delete.html'
    success_url = reverse_lazy('admin_staff:admin_product_category')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_visible = False
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


def db_profile_by_type(prefix, type, queries):
    # update_queries = list(filter(lambda x: type in x['sql'], queries))
    update_queries = [query for query in queries if type in query['sql']]
    print(f'db_profile {type} for {prefix}:')
    [print(query['sql']) for query in update_queries]


@receiver(pre_save, sender=ProductCategory)
def product_is_active_update_productcategory_save(sender, instance, **kwargs):
    if instance.pk:
        instance.products_set.update(is_visible=instance.is_visible)
        # if instance.is_visible:
        #     instance.products_set.update(is_visible=True)
        # else:
        #     instance.products_set.update(is_visible=False)

        db_profile_by_type(sender, 'UPDATE', connection.queries)
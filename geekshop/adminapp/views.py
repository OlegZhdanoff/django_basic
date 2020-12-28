from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test

from authapp.models import ShopUser
from adminapp.forms import UserAdminRegisterForm, UserAdminProfileForm

from mainapp.models import Products, ProductCategory
from mainapp.forms import ProductCreateForm, ProductCategoryForm


@user_passes_test(lambda u: u.is_superuser)
def index(request):
    return render(request, 'adminapp/index.html')


# Следующие контроллеры демонстрируют принцип CRUD
@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
    # C - Create
    if request.method == 'POST':
        form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_users'))
        else:
            print(form.errors)
    else:
        form = UserAdminRegisterForm()
    context = {'form': form}
    return render(request, 'adminapp/admin-users-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
    # R - Read
    context = {
        'users': ShopUser.objects.all(),
    }
    return render(request, 'adminapp/admin-users-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, user_id):
    # U - Update
    user = ShopUser.objects.get(id=user_id)
    if request.method == 'POST':
        form = UserAdminProfileForm(data=request.POST, files=request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_users'))
    else:
        form = UserAdminProfileForm(instance=user)

    context = {'form': form, 'user': user}
    return render(request, 'adminapp/admin-users-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_users_remove(request, user_id):
    user = ShopUser.objects.get(id=user_id)
    # user.delete()
    user.is_active = False
    user.save()
    return HttpResponseRedirect(reverse('admin_staff:admin_users'))


@user_passes_test(lambda u: u.is_superuser)
def admin_products(request):
    # R - Read
    context = {
        'products': Products.objects.all(),
    }
    return render(request, 'adminapp/admin-products-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_create(request):
    # C - Create
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_products'))
        else:
            print(form.errors)
    else:
        form = ProductCreateForm()
    context = {'form': form}
    return render(request, 'adminapp/admin-products-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_update(request, product_id):
    # U - Update
    product = Products.objects.get(id=product_id)
    if request.method == 'POST':
        form = ProductCreateForm(data=request.POST, files=request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_products'))
    else:
        form = ProductCreateForm(instance=product)

    context = {'form': form, 'product': product}
    return render(request, 'adminapp/admin-products-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_products_remove(request, product_id):
    product = Products.objects.get(id=product_id)
    product.is_visible = False
    product.save()
    return HttpResponseRedirect(reverse('admin_staff:admin_products'))


@user_passes_test(lambda u: u.is_superuser)
def admin_product_category(request):
    # R - Read
    context = {
        'categories': ProductCategory.objects.all(),
    }
    return render(request, 'adminapp/admin-product_category-read.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_product_category_create(request):
    # C - Create
    if request.method == 'POST':
        form = ProductCategoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_product_category'))
        else:
            print(form.errors)
    else:
        form = ProductCategoryForm()
    context = {'form': form}
    return render(request, 'adminapp/admin-product_category-create.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_product_category_update(request, category_id):
    # U - Update
    category = ProductCategory.objects.get(id=category_id)
    if request.method == 'POST':
        form = ProductCategoryForm(data=request.POST, files=request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('admin_staff:admin_products'))
    else:
        form = ProductCategoryForm(instance=category)

    context = {'form': form, 'category': category}
    return render(request, 'adminapp/admin-product_category-update-delete.html', context)


@user_passes_test(lambda u: u.is_superuser)
def admin_product_category_remove(request, category_id):
    product_category = ProductCategory.objects.get(id=category_id)
    product_category.is_visible = False
    product_category.save()
    return HttpResponseRedirect(reverse('admin_staff:admin_product_category'))

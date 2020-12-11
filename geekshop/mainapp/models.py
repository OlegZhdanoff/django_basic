from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    short_description = models.CharField(max_length=255, verbose_name='Описание категории', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    photo = models.ImageField(upload_to='products/%Y/%m/%d/', height_field=100, blank=True, verbose_name='Фото')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

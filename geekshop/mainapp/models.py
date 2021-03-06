from django.db import models
from django.urls import reverse


class ProductCategory(models.Model):
    title = models.CharField(max_length=100, unique=True, verbose_name='Название категории')
    short_description = models.CharField(max_length=255, verbose_name='Описание категории', blank=True)
    is_visible = models.BooleanField(default=False, verbose_name='Видимость', db_index=True)

    def get_absolute_url(self):
        return reverse('mainapp:products', kwargs={'category_id': self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Products(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Название')
    photo = models.ImageField(upload_to='products/', blank=True, verbose_name='Фото')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    description = models.TextField(verbose_name='Описание')
    is_visible = models.BooleanField(default=False, verbose_name='Видимость', db_index=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, db_constraint=False, default=1)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    @staticmethod
    def get_items():
        return Products.objects.filter(is_visible=True).order_by('category', 'name').select_related()

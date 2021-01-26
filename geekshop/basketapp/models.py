from django.db import models
from authapp.models import ShopUser

from mainapp.models import Products


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for obj in self:
            obj.product.quantity += obj.quantity
            obj.product.save()

        super().delete(*args, **kwargs)


class Basket(models.Model):
     # привязываем свой менеджер объектов к модели, чтобы правильно работал метод удаления QuerySet
    # object = BasketQuerySet.as_manager()

    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0, verbose_name='Количество')
    created_timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время')

    def __str__(self):
        return f'Корзина для {self.user.username} | Продукт {self.product.name}'

    def sum(self):
        return self.quantity * self.product.price

    def get_user_baskets(self):
        return Basket.objects.filter(user=self.user)

    def total_sum(self):
        return sum([basket.sum() for basket in self.get_user_baskets()])

    def total_qty(self):
        return sum([basket.quantity for basket in self.get_user_baskets()])

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super().delete(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        return Basket.objects.filter(pk=pk).first()

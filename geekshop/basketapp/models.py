from django.db import models
from authapp.models import ShopUser

from mainapp.models import Products


class Basket(models.Model):
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

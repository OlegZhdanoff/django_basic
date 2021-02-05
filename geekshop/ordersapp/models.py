from django.conf import settings
from django.db import models

from mainapp.models import Products


class Order (models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    PROCEED = 'PRD'
    PAID = 'PD'
    READY = 'RD'
    DONE = 'DN'
    CANCEL = 'CNC'

    ORDER_STATUSES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEED, 'отправлен на обработку'),
        (PROCEED, 'обработан'),
        (PAID, 'оплачен'),
        (READY, 'готов к выдаче'),
        (DONE, 'выдан'),
        (CANCEL, 'отменен')
    )

    # подключаем модель авторизации через настройки проекта
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='обновлен')

    status = models.CharField(verbose_name='статус', choices=ORDER_STATUSES, max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активен', default=True, db_index=True)

    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ('-created_at',)

    def get_total_quantity(self):
        # выбираем все продукты нашего заказа, связанные через related в модели OrderItem
        items = self.orderitems.select_related()
        return sum([i.quantity for i in items])

    def get_total_cost(self):
        # выбираем все продукты нашего заказа, связанные через related в модели OrderItem
        items = self.orderitems.select_related()
        return sum([i.quantity * i.product.price for i in items])

    def delete(self):
        for item in self.orderitems.select_related():
            item.product.quantity += item.quantity
            item.product.save()

        self.is_active = False
        self.save()


class OrderItem(models.Model):
    # related_name='orderitems' - можем обращаться из модели Order, ко всем объектам OrderItems, привязанных к
    # данному объекту класса Order
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity

    @staticmethod
    def get_item(pk):
        return OrderItem.objects.filter(pk=pk).first().select_related()

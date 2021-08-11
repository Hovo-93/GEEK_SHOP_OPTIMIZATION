from django.conf import settings
from django.db import models
from products.models import Product


class Order(models.Model):
    FORMING = 'FM'
    SEND_TO_PROCEED = 'STP'
    DELIVERY = 'DLV'
    DONE = 'DN'
    CANCELED = 'CNC'
    STATUSES = (
        (FORMING, 'формирование'),
        (SEND_TO_PROCEED, 'передан в обработку'),
        (DELIVERY, 'доставка'),
        (DONE, 'выдан'),
        (CANCELED, 'отменен'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUSES, default=FORMING, max_length=128)
    is_actice = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'эакаэ'
        verbose_name_plural = 'эакаэы'

    def __str__(self):
        return f'Закаэ номер {self.pk}'

    def get_total_quantity(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related()
        return sum(list(map(lambda x: x.get_product_cost, items)))

    def delete(self):
        self.is_actice = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)

    @property
    def get_product_cost(self):
        return self.product.quantity * self.product.price

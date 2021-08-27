from django.db import models
from django.utils.functional import cached_property

from users.models import User
from products.models import Product


class Basket(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина для {self.user.username} | Продукт {self.product.name}"

    def summa(self):
        return self.quantity * self.product.price
    @property
    def product_cost(self):
        return self.product.price * self.quantity


    # def total_quantity(self):
    #     baskets = Basket.objects.filter(user=self.user)
    #     return sum(basket.quantity for basket in baskets)
    #
    # def total_sum(self):
    #     baskets = Basket.objects.filter(user=self.user)
    #     return sum(basket.summa() for basket in baskets)
    @cached_property
    def get_items_cached(self):
        return self.baskets.select_related()

    def get_total_quantity(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.quantity, _items)))

    def get_total_cost(self):
        _items = self.get_items_cached
        return sum(list(map(lambda x: x.product_cost, _items)))

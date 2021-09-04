from datetime import timedelta

from django.core.management import BaseCommand
from django.db.models import Q, F, When, DecimalField, IntegerField,Case

from ordersapp.models import OrderItem


class Command(BaseCommand):
    def handle(self, *args, **options):
        action_1 = 1  # 30%
        action_2 = 2  # 15%
        action_3 = 3  # 5%

        action_1_time_delta = timedelta(hours=12)
        action_2_time_delta = timedelta(days=1)

        action_1_discount = 0.3
        action_2_discount = 0.15
        action_3_discount = 0.05

        action_1_condition = Q(order__updated__lte=F('created') + action_1_time_delta)
        action_2_condition = Q(order__updated__lte=F('created') + action_2_time_delta) & \
                             Q(order__updated__gt=F('created') + action_1_time_delta)
        action_3_condition = Q(order__updated__gt=F('created') + action_2_time_delta)


        action_1_order = When(action_1_condition,then=action_1)
        action_2_order = When(action_2_condition,then=action_2)
        action_3_order = When(action_3_condition,then=action_3)

        action_1_price = When(action_1_condition, then=F('product__price') * F('quantity') * action_1_discount)
        action_2_price = When(action_2_condition, then=F('product__price') * F('quantity') * -action_2_discount)
        action_3_price = When(action_3_condition, then=F('product__price') * F('quantity') * action_3_discount)

        orders_items = OrderItem.objects.annotate(
            action_order=Case(
                action_1_order,
                action_2_order,
                action_3_order,
                output_field=IntegerField(),
            )
        ).annotate(
            total_price=Case(
                action_1_price,
                action_2_price,
                action_3_price,
                output_field=DecimalField(),
            )
        ).order_by('action_order', 'total_price').select_related()

        for item in orders_items:
            print(f'{item.action_order:2}'
                  f'order#{item.pk:3}'
                  f'{item.product.name:20}'
                  f'discount:{abs(item.total_price):6.2}'
                  f'{item.order.updated - item.order.created}')

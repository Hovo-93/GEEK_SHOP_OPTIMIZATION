from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.db import connection
from products.models import Product
from baskets.models import Basket
from django.template.loader import render_to_string
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required


# @login_required
# def basket_add(request, product_id):
#     product = Product.objects.get(id=product_id)
#     baskets = Basket.objects.filter(user=request.user, product=product)
#     if not baskets.exists():
#         Basket.objects.create(user=request.user, product=product, quantity=1)
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
#     else:
#         basket = baskets.first()
#         basket.quantity += 1
#         basket.save()
#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
@login_required
def basket_add(request, product_id):
    if 'login' in request.META.get('HTTP_REFERER'):
        return HttpResponseRedirect(reverse('products:product', args=[product_id]))

    product = get_object_or_404(Product, id=product_id)
    old_basket_item = Basket.objects.filter(user=request.user, product=product)

    # old_basket_item = Basket.get_product(user=request.user, product=product)

    if old_basket_item:
        # old_basket_item[0].quantity +=1
        old_basket_item[0].quantity = F('quantity') + 1
        old_basket_item[0].save()

        update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        print(f'query basket_add:{update_queries}')
    else:
        new_basket_item = Basket(user=request.user, product=product)
        new_basket_item.quantity += 1
        new_basket_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, id):
    basket = Basket.objects.get(id=id)
    basket.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()
        baskets = Basket.objects.filter(user=request.user)
        context = {
            'baskets': baskets
        }
        result = render_to_string('baskets/basket.html', context)
        return JsonResponse({'result': result})

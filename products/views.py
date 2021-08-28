from django.shortcuts import render
from products.models import Product, ProductCategory
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import json
import os
from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.conf import settings
from django.shortcuts import get_object_or_404

MODULE_DIR = os.path.dirname(__file__)


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.all()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.all()


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


# Create your views here.
def index(request):
    context = {
        'title': 'GeekShop Store',
        'products': [
            {'name': 'Худи черного цвета с монограммами adidas Originals'},
            {'name': 'Синяя куртка The North Face'},
            {'name': 'Коричневый спортивный oversized-топ ASOS DESIGN'},
        ]
    }
    return render(request, 'products/index.html', context)


# def products(request):
#     context = {
#         'title': 'GeekShop Products',
#         'products': Product.objects.all(),
#         'categories': ProductCategory.objects.all(),
#         'promotion': True,
#         'promotion_of_products': [
#             {'name': 'Черный рюкзак Nike Heritage',
#              'price': 2340},
#             {'name': 'Черные туфли на платформе с 3 парами люверсов Dr Martens 1461 Bex',
#              'price': 13590},
#             {'name': 'Темно-синие широкие строгие брюки ASOS DESIGN',
#              'price': 2890},
#         ],
#     }
#
#     return render(request, 'products/products.html', context)
def products(request, category_id=None, page=1):
    context = {'title': 'GeekShop Products', 'categories': ProductCategory.objects.all()}
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()
    paginator = Paginator(products, 3)
    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)
    context['products'] = products_paginator
    return render(request, 'products/products.html', context)


@login_required
def product(request, pk):
    title = 'страница продукта'
    # product: get_object_or_404(Product, pk=pk)

    product = get_product(pk)

    context = {
        'title': title,
        'product': product,
        'links_menu': get_links_menu(),
        # 'basket': get_basket(request.user),
        # 'categories': ProductCategory.objects.all(),
        'categories': ProductCategory.objects.filter().select_related()

    }

    return render(request, 'products/products.html', context)

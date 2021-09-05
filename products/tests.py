from django.test import TestCase
from django.test import Client

from products.models import ProductCategory, Product


class ProductsAppSmokeTest(TestCase):
    status_code_success = 200
    category = ProductCategory.objects.create(
        name ='cat1'
    )
    for i in range(10):
        Product.objects.create(
            category = category,
            name =f'prod{i}',
        )
    def setUp(self):
        self.client = Client()

    def test_product_app_urls(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, self.status_code_success)

    def test_products_list(self):
        for product_item in Product.objects.all():
            response = self.client.get(f'/products/{product_item.pk}/')
            self.assertEqual(response.status_code,self.status_code_success)






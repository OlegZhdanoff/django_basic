from django.test import TestCase, Client

from mainapp.models import ProductCategory, Products


class ProductsTestCase(TestCase):
    def setUp(self):
        category = ProductCategory.objects.create(
            title='Test',
            is_visible=True
        )
        self.product_1 = Products.objects.create(
            name='TestProd1',
            price=1000,
            description='description',
            is_visible=True,
            category=category
        )
        self.product_2 = Products.objects.create(
            name='TestProd2',
            price=2000,
            description='description 2',
            is_visible=False,
            category=category
        )

        self.product_3 = Products.objects.create(
            name='TestProd3',
            price=3000,
            description='description 3',
            is_visible=True,
            category=category
        )

        self.client = Client()

    def test_product_get(self):
        product_1 = Products.objects.get(name="TestProd1")
        product_2 = Products.objects.get(name="TestProd2")
        self.assertEqual(product_1, self.product_1)
        self.assertEqual(product_2, self.product_2)

    def test_product_print(self):
        product_1 = Products.objects.get(name="TestProd1")
        product_2 = Products.objects.get(name="TestProd2")
        self.assertEqual(str(product_1), 'TestProd1')
        self.assertEqual(str(product_2), 'TestProd2')

    def test_product_get_items(self):
        product_1 = Products.objects.get(name="TestProd1")
        product_3 = Products.objects.get(name="TestProd3")
        products = product_1.get_items()

        self.assertEqual(list(products), [product_1, product_3])

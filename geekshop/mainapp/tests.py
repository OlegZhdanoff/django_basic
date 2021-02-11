from django.core.management import call_command
from django.test import TestCase, Client

from mainapp.models import ProductCategory, Products


class TestMainappTestCase(TestCase):

    def setUp(self):
        category = ProductCategory.objects.create(
            title='Test',
            is_visible=True
        )
        Products.objects.create(
            name='TestProd1',
            price=1000,
            description='description',
            is_visible=True,
            category=category
        )
        Products.objects.create(
            name='TestProd2',
            price=2000,
            description='description 2',
            is_visible=True,
            category=category
        )

        self.client = Client()

    def test_mainapp_pages(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        call_command('sqlsequencereset', 'mainapp', 'authapp', 'ordersapp', 'basketapp')


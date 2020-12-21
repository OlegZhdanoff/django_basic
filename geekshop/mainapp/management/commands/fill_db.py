from django.core.management.base import BaseCommand
from mainapp.models import ProductCategory, Products
from mainapp import services
from authapp.models import ShopUser
import datetime


class Command(BaseCommand):
    def handle(self, *args, **options):
        ProductCategory.objects.all().delete()
        Products.objects.all().delete()

        services.load_product_to_db(services.load_content_from_file('products.json'), Products, ProductCategory)

        super_user = ShopUser.objects.create_superuser('admin', 'admin@mail.com', '123',
                                                       birthday=datetime.date(1980, 6, 9))

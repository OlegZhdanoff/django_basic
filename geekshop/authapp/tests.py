from datetime import datetime

from django.test import TestCase, Client

from authapp.models import ShopUser


class TestUserAuthTestCase(TestCase):

    def setUp(self):
        self.admin = ShopUser.objects.create_superuser('admin2', 'admin2@mail.com', '123',
                                                       birthday=datetime.date(1980, 6, 9))
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь')

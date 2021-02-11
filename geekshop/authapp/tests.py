import datetime

from django.test import TestCase, Client

from authapp.models import ShopUser


class TestUserAuthTestCase(TestCase):
    username = 'admin2'
    email = 'admin2@mail.com'
    password = '123'

    def setUp(self):
        self.admin = ShopUser.objects.create_superuser(self.username, self.email, self.password,
                                                       birthday=datetime.date(1980, 6, 9))
        self.client = Client()

    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['user'].is_anonymous)
        self.assertNotContains(response, 'Пользователь')

        self.client.login(username=self.username, password=self.password)

        response = self.client.get('/auth/login/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertEqual(response.context['user'], self.admin)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)
        self.assertContains(response, 'Пользователь')

    def test_user_register(self):
        response = self.client.get('/auth/register/')
        self.assertEqual(response.status_code, 200)

        new_user_data = {
            'username': self.username,
            'password1': self.password,
            'password2': self.password,
            'email': self.email,
            'birthday': datetime.date(1980, 6, 9)
        }

        response = self.client.post('/auth/register/', data=new_user_data)
        self.assertEqual(response.status_code, 302)

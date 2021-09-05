from django.test import TestCase
from django.test import Client

# Create your tests here.
from users.models import UserProfile


class UserAuthTestCase(TestCase):
    status_code_success = 200
    status_code_redirect = 302
    status_code_forbidden = 403
    username = 'django_test2'
    user_password = 'geekbrains'

    def setUp(self):
        self.client = Client()
        self.user = UserProfile.objects.create(
            username=self.username,
            password=self.user_password,
            email='django_test2@gb.local',
        )

    def test_login_user(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertTrue(response.context['user'].is_anonymous)

        # self.client.login(username = self.username,password=self.user_password)
        user_data ={
            'username':self.username,
            'password':self.user_password
        }

        response = self.client.get('/user/login/',data=user_data)
        self.assertEqual(response.status_code, self.status_code_redirect)

        response = self.client.get('/')
        self.assertEqual(response.status_code, self.status_code_success)
        self.assertFalse(response.context['user'].is_anonymous)


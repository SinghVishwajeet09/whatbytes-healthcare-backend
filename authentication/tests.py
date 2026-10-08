from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

User = get_user_model()


class AuthenticationAPITests(APITestCase):
    def setUp(self):
        self.register_url = reverse('auth-register')
        self.login_url = reverse('auth-login')
        self.me_url = reverse('auth-me')
        self.valid_payload = {
            'name': 'Dr. Alice Martin',
            'email': 'alice@example.com',
            'password': 'StrongPassword123!',
        }

    def test_register_user_success(self):
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
        self.assertEqual(response.data['user']['email'], 'alice@example.com')
        self.assertEqual(response.data['user']['name'], 'Dr. Alice Martin')
        self.assertTrue(User.objects.filter(email='alice@example.com').exists())

    def test_register_user_duplicate_email(self):
        self.client.post(self.register_url, self.valid_payload, format='json')
        response = self.client.post(self.register_url, self.valid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data)

    def test_register_user_short_password(self):
        payload = {
            'name': 'Shorty',
            'email': 'short@example.com',
            'password': '123',
        }
        response = self.client.post(self.register_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_user_success(self):
        self.client.post(self.register_url, self.valid_payload, format='json')
        login_payload = {
            'email': 'alice@example.com',
            'password': 'StrongPassword123!',
        }
        response = self.client.post(self.login_url, login_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('tokens', response.data)
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])

    def test_login_user_invalid_password(self):
        self.client.post(self.register_url, self.valid_payload, format='json')
        login_payload = {
            'email': 'alice@example.com',
            'password': 'WrongPassword!',
        }
        response = self.client.post(self.login_url, login_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_nonexistent_user(self):
        login_payload = {
            'email': 'nonexistent@example.com',
            'password': 'SomePassword123!',
        }
        response = self.client.post(self.login_url, login_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_current_user_authenticated_vs_unauthenticated(self):
        # Unauthenticated
        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # Authenticated
        reg_resp = self.client.post(self.register_url, self.valid_payload, format='json')
        token = reg_resp.data['tokens']['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

        response = self.client.get(self.me_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'alice@example.com')

from django.test import TestCase
from django.db import IntegrityError
from rest_framework.test import APIClient

from ..models import User


class TestUserView(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_creation_data = {
            'username': 'leprechawn',
            'password': 'a1b2c3d4',
            'is_staff': False,
            'is_superuser': False
        }
        self.login_data = {
            'username': 'leprechawn',
            'password': 'a1b2c3d4'
        }

    def test_user_creation(self):
        response = self.client.post(
            '/api/accounts/', self.user_creation_data, format='json')

        self.assertEqual(response.status_code, 201)

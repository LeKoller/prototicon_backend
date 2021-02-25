from django.test import TestCase
from django.db import IntegrityError

from .models import User


class TestUserModel(TestCase):
    def setUp(self):
        self.guilherme_data = {
            'username': 'gui',
            'password': 'senha123'
        }

        self.leandro_data = {
            'username': 'lekoller',
            'password': 'senha321'
        }

    def test_user_create(self):
        guilherme = User.objects.create_user(**self.guilherme_data)

        guilherme = User.objects.first()

        self.assertEqual(guilherme.username, self.guilherme_data['username'])
        self.assertEqual(len(guilherme.followers.all()), 0)
        self.assertEqual(len(guilherme.following.all()), 0)

    def test_following_user(self):
        guilherme = User.objects.create_user(**self.guilherme_data)
        leandro = User.objects.create_user(**self.leandro_data)

        leandro.following.add(guilherme)

        self.assertEqual(guilherme.followers.first(), leandro)
        self.assertEqual(leandro.following.first(), guilherme)
        self.assertEqual(len(leandro.followers.all()), 0)
        self.assertEqual(len(guilherme.following.all()), 0)

    def test_username_is_unique(self):
        User.objects.create_user(**self.guilherme_data)

        with self.assertRaises(IntegrityError):
            User.objects.create_user(**self.guilherme_data)

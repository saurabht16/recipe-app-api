from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Tests the users API (public)
    """

    def setUp(self) -> None:
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """
        Test creating user with valid payload is successful
        :return: Test Result for Pass or Fail
        """
        payload = {
            'email': 'test@djangoappdev.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """
        Tests creating user that already exists
        :return: Boolean Test Result
        """
        payload = {
            'email': 'test@djangoappdev.com',
            'password': 'testpass',
            'name': 'Test Name'
        }
        create_user(**payload)

        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """
        Test the password must be more than 5 characters
        :return: Boolean Test Result
        """
        payload = {
            'email': 'test@djangoappdev.com',
            'password': 'pw',
            'name': 'Test Name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        user_exist = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exist)

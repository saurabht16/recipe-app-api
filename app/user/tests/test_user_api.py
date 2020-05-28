from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """
    Tests the users API (public)
    """

    def setUp(self) -> None:
        self.client = APIClient()
        self.payload = {
            'email': 'test@djangoappdev.com',
            'password': 'testpass',
            'name': 'Test Name'
        }

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

    def test_create_token_for_user(self):
        """
        Test that the token is created for the User
        :return: Boolean result for Tests
        """
        create_user(**self.payload)
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """
        Test that token is not created when invalid credentials are given
        :return: Boolean Test Result
        """
        create_user(**self.payload)
        incorrect_payload = {
            'email': 'test@djangoappdev.com',
            'password': 'wrong',
            'name': 'Test Name'
        }
        res = self.client.post(TOKEN_URL, incorrect_payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """
        Test that token is not created is user does not exist
        :return: Boolean Test Result
        """
        res = self.client.post(TOKEN_URL, self.payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """
        Test that email and password are required
        :return: Boolean Test Result
        """
        res = self.client.post(TOKEN_URL, {'email': 'test', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

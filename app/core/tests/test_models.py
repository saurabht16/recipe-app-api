from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):
    """
    Test Class for Models
    """
    def test_create_user_model_with_email_successful(self):
        """
        Test for creating new user with Email is successful
        :return: Boolean
        """
        email = "test@djangote st.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalised(self):
        """
        Test email of the new user Normalised
        :return: Boolean
        """
        email = "test@DJANGOAPPDEV.COM"
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """
        Test creating user with no email raises Error
        :return: ValueError
        """
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

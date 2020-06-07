from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@djangoappdev.com', password='testpass'):
    """
    Create a sample user
    :param email: email of user
    :param password: password
    :return: new user
    """
    return get_user_model().objects.create_user(email, password)


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

    def test_create_new_superuser(self):
        """
        Test creating a new super user
        :return: Super User object
        """
        user = get_user_model().objects.create_superuser(
            'admin@djangoappdev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """
        Test the tag str representation
        :return:
        """
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )
        self.assertEqual(str(tag), tag.name)

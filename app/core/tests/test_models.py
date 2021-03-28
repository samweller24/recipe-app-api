from django.test import TestCase
from django.contrib.auth import get_user_model


from core import models


def sample_user(email='sam@weller.com', password='testpass'):
    """Create a sample_user"""
    return get_user_model().objects.create_user(email,password)


class ModelTests(TestCase):
    def test_create_user_with_email_sucessful(self):
        """Test creating new user with an email is successful"""
        email = 'test@sam.com'
        password = 'password'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email for new user is noramlize"""
        email = 'test@SAM.COM'
        user = get_user_model().objects.create_user(email, 'sam123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with inalide email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_super_user(self):
        """Test ceating a new super user"""
        user =get_user_model().objects.create_superuser(
            'sam@weller.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_tag_str(self):
        """Test the tag string"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Vegan'
        )

        self.assertEqual(str(tag),tag.name)

"""
Test for models
"""
from decimal import Decimal

from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def create_user(email='user@example.com', password='testpass123'):
    return get_user_model().objects.create_user(email, password)


class UserModelTests(TestCase):
    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )
        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com']
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'test123')
            self.assertEqual(user.email, expected)

    def test_new_user_with_email_raise_error(self):
        """Test creating user without email raise a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user("", "test123")

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)


class RecipeModelTests(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123'
        )

    def test_create_recipe_successful(self):
        """Test creating a new recipe"""
        recipe = models.Recipe.objects.create(
            user=self.user,
            title='Test Recipe',
            time_minutes=5,
            price=Decimal('10.00'),
            description='Test description for recipe'
        )
        self.assertEqual(recipe.user, self.user)
        self.assertEqual(str(recipe), recipe.title)

    def test_create_tag(self):
        """Test creating a new tag successful """
        user = create_user()
        tag = models.Tag.objects.create(
            user=user,
            name='Tag1'
        )
        self.assertEqual(str(tag), tag.name)
        self.assertEqual(tag.user, user)

    def test_create_ingredient(self):
        """Test creating a new ingredient successful"""
        user = create_user()
        ingredient = models.Ingredient.objects.create(
            user=user,
            name='Ingredient1'
        )

        self.assertEqual(str(ingredient), ingredient.name)

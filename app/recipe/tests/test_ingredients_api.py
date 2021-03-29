from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ingredient

from recipe.serializers import IngredientSerializer


INGREDIENTS_URL = reverse('recipe:ingredient-list')


class PublicIngredientsAPITests(TestCase):
    """Test pubically avialible api endpoints"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for access"""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientAPITests(TestCase):
    """Test priavte api endpoints"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'sam@weller.com',
            'testpass'
        )
        self.client.force_authenticate(self.user)

    def test_retreive_ingredient(self):
        """Test retreiving list of ingredients"""
        Ingredient.objects.create(user=self.user,name='Kale')
        Ingredient.objects.create(user=self.user,name='Salt')

        res = self.client.get(INGREDIENTS_URL)

        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data,serializer.data)

    def test_user_ingredients(self):
        """Test that only ingredients for user return"""
        user2 = get_user_model().objects.create_user(
                'other@weller.com',
                'testpass',
        )
        Ingredient.objects.create(user=user2,name='Vinegar')
        tag = Ingredient.objects.create(user=self.user,name='Pasta')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code,status.HTTP_200_OK)
        self.assertEqual(len(res.data),1)
        self.assertEqual(res.data[0]['name'],tag.name)


    def test_create_ingredient_success(self):
        """Test that we can create a new ingredient"""
        payload = {'name': 'Cabbage'}
        self.client.post(INGREDIENTS_URL, payload)

        exists = Ingredient.objects.filter(
            user=self.user,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_ingredient_invalid(self):
        """Test that error throws for invALID INGREDIENT"""
        payload = {'name': ''}
        res = self.client.post(INGREDIENTS_URL, payload)

        self.assertEqual(res.status_code,status.HTTP_400_BAD_REQUEST)

from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Profile
from categories.models import Category, SubCategory
from categories.serializers import CategorySerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.management import call_command
from django.urls import reverse


class CategoryTests(APITestCase):

    def setUp(self):
        """Set up the initial data for the tests."""
        # Populate categories and subcategories before each test
        call_command('populate_categories')

        # Create user and associated profile
        self.user = User.objects.create_user(
            username='testuser', password='strongpassword123'
        )
        self.profile = Profile.objects.get(owner=self.user)

        # Create categories and subcategory for testing
        self.category = Category.objects.create(
            name='Food', category_type='expense'
        )
        self.subcategory = SubCategory.objects.create(
            name='Groceries', category=self.category
        )

        # Get JWT token and set authentication header
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

    # --- Category Model Tests ---
    def test_category_creation(self):
        """
        Test that a new category is created correctly with valid data.
        Verifies that the new category appears in
        the database and has correct attributes.
        """
        url = '/categories/'
        data = {
            'name': 'Transportation',
            'category_type': 'expense',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Category.objects.count(), 16)
        category = Category.objects.last()
        self.assertEqual(category.name, 'Transportation')
        self.assertEqual(category.category_type, 'expense')

    def test_category_creation_invalid_type(self):
        """
        Test creating a category with an invalid category_type.
        Verifies that an invalid category type returns a 400 Bad Request.
        """
        url = '/categories/'
        data = {
            'name': 'Salary',
            'category_type': 'invalid_type',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_category_list(self):
        """
        Test listing all categories.
        Verifies that the API returns a list
        of categories with a 200 OK status.
        """
        url = '/categories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_category_detail(self):
        """
        Test retrieving the details of a specific category.
        Verifies that the correct category
        details are returned with a 200 OK status.
        """
        url = f'/categories/{self.category.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.category.name)
        self.assertEqual(
            response.data['category_type'], self.category.category_type
        )

    def test_category_update(self):
        """
        Test updating a category's details.
        Verifies that the category is updated
        successfully and returns the correct updated data.
        """
        url = f'/categories/{self.category.id}/'
        data = {
            'name': 'Updated Category Name',
            'category_type': 'income',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.category.refresh_from_db()
        self.assertEqual(self.category.name, 'Updated Category Name')
        self.assertEqual(self.category.category_type, 'income')

    def test_category_delete(self):
        """
        Test deleting a category.
        Verifies that deleting a category removes it from the database.
        """
        category_to_delete = Category.objects.first()
        initial_count = Category.objects.count()
        response = self.client.delete(
            reverse('category-detail', args=[category_to_delete.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Category.objects.count(), initial_count - 1)

    # --- SubCategory Model Tests ---
    def test_subcategory_list(self):
        """
        Test listing all subcategories under a category.
        Verifies that all subcategories for a
        given category are returned with a 200 OK status.
        """
        url = f'/categories/{self.category.id}/subcategories/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_subcategory_detail(self):
        """
        Test retrieving the details of a specific subcategory.
        Verifies that the correct subcategory
        details are returned with a 200 OK status.
        """
        subcategory = SubCategory.objects.first()
        url = reverse('subcategory-detail', args=[subcategory.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], subcategory.id)

    def test_subcategory_update(self):
        """
        Test updating a subcategory's name.
        Verifies that the subcategory name
        is updated successfully and returned correctly.
        """
        subcategory = SubCategory.objects.first()
        url = reverse('subcategory-detail', args=[subcategory.id])
        data = {'name': 'Updated Subcategory Name'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        subcategory.refresh_from_db()
        self.assertEqual(subcategory.name, 'Updated Subcategory Name')

    def test_subcategory_delete(self):
        """
        Test deleting a subcategory.
        Verifies that deleting a subcategory removes it from the database.
        """
        subcategory_to_delete = SubCategory.objects.first()
        response = self.client.delete(reverse(
            'subcategory-detail', args=[subcategory_to_delete.id])
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(
            SubCategory.objects.filter(id=subcategory_to_delete.id).count(), 0)

    # --- Category Serializer Tests ---
    def test_category_serializer_invalid_data(self):
        """
        Test the category serializer with invalid data.
        Verifies that the serializer correctly
        identifies invalid category types.
        """
        data = {
            'name': 'Salary',
            'category_type': 'invalid_type',
        }
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category_type', serializer.errors)

    def test_category_serializer_missing_required_fields(self):
        """
        Test the category serializer with missing required fields.
        Verifies that the serializer identifies missing
        required fields (e.g., category_type).
        """
        data = {
            'name': 'Salary',
        }
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category_type', serializer.errors)

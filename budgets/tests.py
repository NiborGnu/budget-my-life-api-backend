from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Profile
from categories.models import Category
from budgets.models import Budget
from budgets.serializers import BudgetSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class BudgetTests(APITestCase):

    def setUp(self):
        """Set up the initial data for the tests."""
        # Create user and associated profile
        self.user = User.objects.create_user(
            username='testuser', password='strongpassword123'
        )
        self.profile = Profile.objects.get(owner=self.user)

        # Create categories
        self.category = Category.objects.create(
            name='Food', category_type='expense'
        )

        # Create a budget for testing
        self.budget = Budget.objects.create(
            profile=self.profile,
            name='Monthly Food Budget',
            amount=500.00,
            category=self.category
        )

        # Get JWT token and set authentication header
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

    # --- Budget Model Tests ---
    def test_budget_creation(self):
        """Test creating a budget with valid data."""
        url = '/budgets/'
        data = {
            'name': 'Entertainment Budget',
            'amount': '300.00',
            'category_id': self.category.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 2)
        budget = Budget.objects.last()
        self.assertEqual(budget.name, 'Entertainment Budget')
        self.assertEqual(budget.amount, 300.00)
        self.assertEqual(budget.category, self.category)

    def test_budget_creation_without_category(self):
        """Test creating a budget without providing a category."""
        url = '/budgets/'
        data = {
            'name': 'Savings Budget',
            'amount': '1000.00',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        budget = Budget.objects.last()
        self.assertEqual(budget.name, 'Savings Budget')
        self.assertEqual(budget.amount, 1000.00)
        self.assertIsNone(budget.category)

    def test_budget_update(self):
        """Test updating a budget."""
        url = f'/budgets/{self.budget.id}/'
        data = {
            'name': 'Updated Budget Name',
            'amount': '600.00',
        }
        # Remove category_id from the data payload to avoid passing None
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.budget.refresh_from_db()
        self.assertEqual(self.budget.name, 'Updated Budget Name')
        self.assertEqual(self.budget.amount, 600.00)
        self.assertIsNone(self.budget.category)

    def test_budget_delete(self):
        """Test deleting a budget."""
        url = f'/budgets/{self.budget.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Budget.objects.count(), 0)

    # --- Budget Serializer Tests ---
    def test_budget_serializer_valid_data(self):
        """Test the budget serializer with valid data."""
        data = {
            'name': 'Vacation Budget',
            'amount': '1500.00',
            'category_id': self.category.id,
        }
        serializer = BudgetSerializer(
            data=data, context={'request': self.client}
        )
        self.assertTrue(serializer.is_valid())

    def test_budget_serializer_missing_fields(self):
        """Test the budget serializer with missing required fields."""
        data = {
            'name': 'Incomplete Budget',
        }
        serializer = BudgetSerializer(
            data=data, context={'request': self.client}
        )
        self.assertFalse(serializer.is_valid())
        self.assertIn('amount', serializer.errors)

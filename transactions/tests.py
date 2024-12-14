from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Profile
from categories.models import Category, SubCategory
from budgets.models import Budget
from transactions.models import Transaction
from transactions.serializers import TransactionSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIRequestFactory


class TransactionTests(APITestCase):

    def setUp(self):
        # Create user and associated profile
        self.user = User.objects.create_user(
            username='testuser', password='strongpassword123'
        )
        self.profile = Profile.objects.get(owner=self.user)

        # Create categories and subcategories
        self.category = Category.objects.create(name='Food')
        self.subcategory = SubCategory.objects.create(
            name='Groceries', category=self.category
        )

        # Create budget
        self.budget = Budget.objects.create(
            name='Monthly Budget', amount=1000.00, profile=self.profile
        )

        # Get JWT token and set authentication header
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}'
        )

    # --- Transaction Model Tests ---
    def test_transaction_creation(self):
        """Test that a transaction is created correctly."""
        url = '/transactions/'
        data = {
            'amount': '50.00',
            'transaction_type': 'expense',
            'category_id': self.category.id,
            'subcategory_id': self.subcategory.id,
            'budget_id': self.budget.id,
            'description': 'Grocery shopping',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Transaction.objects.count(), 1)
        transaction = Transaction.objects.first()
        self.assertEqual(transaction.amount, 50.00)
        self.assertEqual(transaction.transaction_type, 'expense')
        self.assertEqual(transaction.profile, self.profile)
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.subcategory, self.subcategory)
        self.assertEqual(transaction.budget, self.budget)
        self.assertEqual(transaction.description, 'Grocery shopping')

    def test_transaction_creation_without_budget(self):
        """Test creating a transaction without providing a budget."""
        url = '/transactions/'
        data = {
            'amount': '20.00',
            'transaction_type': 'income',
            'category_id': self.category.id,
            'subcategory_id': self.subcategory.id,
            'description': 'Freelance work',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.first()
        self.assertIsNone(transaction.budget)
        self.assertEqual(transaction.amount, 20.00)
        self.assertEqual(transaction.transaction_type, 'income')

    def test_transaction_update(self):
        """Test updating a transaction."""
        transaction = Transaction.objects.create(
            profile=self.profile,
            amount=100.00,
            transaction_type='income',
            category=self.category,
            subcategory=self.subcategory,
            budget=self.budget,
            description='Freelance work'
        )
        url = f'/transactions/{transaction.id}/'
        data = {
            'amount': '150.00',
            'transaction_type': 'expense',
            'category_id': self.category.id,
            'subcategory_id': self.subcategory.id,
            'budget_id': self.budget.id,
            'description': 'Office supplies',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        transaction.refresh_from_db()
        self.assertEqual(transaction.amount, 150.00)
        self.assertEqual(transaction.transaction_type, 'expense')
        self.assertEqual(transaction.description, 'Office supplies')

    def test_transaction_delete(self):
        """Test deleting a transaction."""
        transaction = Transaction.objects.create(
            profile=self.profile,
            amount=100.00,
            transaction_type='income',
            category=self.category,
            subcategory=self.subcategory,
            budget=self.budget,
            description='Freelance work'
        )
        url = f'/transactions/{transaction.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Transaction.objects.count(), 0)

    # --- Transaction Serializer Tests ---
    def test_transaction_serializer_invalid_data(self):
        """Test the transaction serializer with invalid data."""
        data = {
            'amount': '50.00',
            'transaction_type': 'invalid_type',
            'category_id': self.category.id,
            'subcategory_id': self.subcategory.id,
            'budget_id': self.budget.id,
            'description': 'Grocery shopping',
        }
        serializer = TransactionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('transaction_type', serializer.errors)

    def test_transaction_serializer_missing_required_fields(self):
        """Test missing required fields in transaction serializer."""
        data = {
            'amount': '50.00',
            'transaction_type': 'expense',
        }
        serializer = TransactionSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('category_id', serializer.errors)

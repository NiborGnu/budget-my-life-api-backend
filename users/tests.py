from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from users.models import Profile
from rest_framework_simplejwt.tokens import RefreshToken


class UserRegistrationTests(APITestCase):
    def test_user_registration(self):
        """Test that a new user can register successfully."""
        url = '/register/'
        data = {
            'username': 'testuser',
            'password': 'strongpassword123',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username='testuser').exists())
        self.assertTrue(Profile.objects.filter(owner__username='testuser').exists())


class TokenAuthenticationTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='strongpassword123')
        self.token_url = '/token/'

    def test_obtain_token(self):
        """Test that a valid token can be obtained with correct credentials."""
        data = {
            'username': 'testuser',
            'password': 'strongpassword123',
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_credentials(self):
        """Test that token cannot be obtained with invalid credentials."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        response = self.client.post(self.token_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn('access', response.data)
        self.assertNotIn('refresh', response.data)


class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='strongpassword123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_profile_creation(self):
        """Test that a profile is created automatically when a user is registered."""
        self.assertTrue(Profile.objects.filter(owner=self.user).exists())

    def test_profile_retrieval(self):
        """Test that the authenticated user can retrieve their profile."""
        url = f'/users/profiles/{self.user.profile.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], '')
        self.assertEqual(response.data['last_name'], '')


class ProfileSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='strongpassword123')
        self.profile = Profile.objects.get(owner=self.user)
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_retrieve_profile(self):
        """Test that an authenticated user can retrieve their profile."""
        url = f'/users/profiles/{self.profile.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], self.user.username)

    def test_update_profile(self):
        """Test that a user can update their profile details."""
        url = f'/users/profiles/{self.profile.id}/'
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            # Ensure you add any required fields for the profile update (e.g., email).
        }
        response = self.client.patch(url, data)  # Changed PUT to PATCH
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.first_name, 'John')
        self.assertEqual(self.profile.last_name, 'Doe')

    def test_unique_username_validation(self):
        """Test that the username uniqueness is validated."""
        User.objects.create_user(username='anotheruser', password='strongpassword456')
        url = f'/users/profiles/{self.profile.id}/'
        data = {
            'username': 'anotheruser'  # Try updating to an existing username
        }
        response = self.client.patch(url, data)  # Changed PUT to PATCH
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)  # Check that username validation error is returned

    def test_username_min_length(self):
        """Test that the username must be at least 3 characters long."""
        url = f'/users/profiles/{self.profile.id}/'
        data = {
            'username': 'ab'  # Try updating to a username that's too short
        }
        response = self.client.patch(url, data)  # Changed PUT to PATCH
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)  # Check that username validation error is returned


class PasswordUpdateSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='oldpassword123')
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.password_update_url = '/users/change-password/'

    def test_password_update_success(self):
        """Test that the user can successfully update their password."""
        data = {
            'old_password': 'oldpassword123',
            'new_password': 'newstrongpassword123',
            'confirm_password': 'newstrongpassword123',
        }
        response = self.client.patch(self.password_update_url, data)  # Change POST to PATCH
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify new password works
        self.client.logout()
        login_success = self.client.login(username='testuser', password='newstrongpassword123')
        self.assertTrue(login_success)

    def test_password_update_wrong_old_password(self):
        """Test that the password update fails with an incorrect old password."""
        data = {
            'old_password': 'wrongoldpassword',
            'new_password': 'newstrongpassword123',
            'confirm_password': 'newstrongpassword123',
        }
        response = self.client.patch(self.password_update_url, data)  # Change POST to PATCH
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('detail', response.data)

    def test_password_update_mismatch(self):
        """Test that the password update fails when new passwords do not match."""
        data = {
            'old_password': 'oldpassword123',
            'new_password': 'newstrongpassword123',
            'confirm_password': 'differentpassword',
        }
        response = self.client.patch(self.password_update_url, data)  # Change POST to PATCH
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('confirm_password', response.data)

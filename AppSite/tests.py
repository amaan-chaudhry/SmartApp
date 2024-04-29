from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

class LoginTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(username='testuser', password='testpassword')

    def test_login_success(self):
        # Make a POST request to the login view with valid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})

        # Check if the user is logged in (status code 302 indicates redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the expected URL after login
        self.assertRedirects(response, reverse('home'))  # Adjust 'home' to your home page URL

        # Check if the user is logged in by checking the session
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_failure(self):
        # Make a POST request to the login view with invalid credentials
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})

        # Check if the user is not logged in (status code 200 indicates success)
        self.assertEqual(response.status_code, 200)

        # Check if the user is not redirected
        self.assertEqual(response.redirect_chain, [])

        # Check if the error message is displayed in the response
        self.assertContains(response, 'Please enter a correct username and password.')

    def test_logout(self):
        # Log in the test user
        self.client.login(username='testuser', password='testpassword')

        # Make a GET request to the logout view
        response = self.client.get(reverse('logout'))

        # Check if the user is logged out (status code 302 indicates redirect)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the expected URL after logout
        self.assertRedirects(response, reverse('login'))  # Adjust 'login' to your login page URL

        # Check if the user is logged out by checking the session
        self.assertFalse('_auth_user_id' in self.client.session)
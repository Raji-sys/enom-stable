from django.test import TestCase
from django.contrib.auth.models import User
from ..models import *
from django.test import TestCase
from django.urls import reverse
from django.http import QueryDict


class IndexViewTests(TestCase):
    def test_index_view_redirect_unauthenticated_user(self):
        # Try to access the index page without logging in
        response = self.client.get(reverse('index'))

        # Check if the response status code is a redirect (302)
        self.assertEqual(response.status_code, 302)

        # Check if the user is redirected to the login page
        self.assertRedirects(response, reverse('login') + '?next=' + reverse('index'))



class CustomLoginViewTests(TestCase):
    def test_custom_login_view_redirect_authenticated_user(self):
        # Create a user and log them in
        user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')

        # Try to access the login page
        response = self.client.get(reverse('login'))

        # Check if the response status code is a redirect (302)
        self.assertEqual(response.status_code, 302)

        # Remove the 'next' parameter from the actual URL
        actual_url = response.url
        actual_url_without_next = actual_url.split('?')[0]

        # Check if the user is redirected to the home page
        expected_url = reverse('index')
        self.assertEqual(actual_url_without_next, expected_url)



class UserRegistrationViewTest(TestCase):
    def test_registration_view(self):
        # Define test data
        data = {
            'username': 'testuser',
            'first_name': 'John',
            'last_name': 'Doe',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
        }

        # Ensure the registration view is accessible
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        # Ensure a new user is created upon form submission
        response = self.client.post(reverse('register'), data)
        self.assertEqual(response.status_code, 302)  # Check for a successful status code
        print(response.content.decode())  # Print the response content for debugging

        # Check the number of user objects in the database
        print("Number of users in the database:", User.objects.count())
        self.assertEqual(User.objects.count(), 1)

        # Optionally, you can check other details like user profile creation
        user = User.objects.first()

        # Ensure that the user is now authenticated
        self.assertTrue(user.is_authenticated)

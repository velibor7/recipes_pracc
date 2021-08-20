from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')

# since we are going to use multiple users in different tests
# we need to create a helper

def create_user(**params):
	return get_user_model().objects.create_user(**params)


# we split tests int othe public and private ones
# public are not auth, private are

class PublicUserAPITests(TestCase):
	"""Test the users api public"""


	def setUp(self):
		self.client = APIClient() # one client for all of the tests

	def test_create_valid_user_success(self):
		"""Test creating user with valid bapyload is successful"""
		payload = {
			'email': 'test@email.com',
			'password': 'test123',
			'name': 'Test Name',
		}

		res = self.client.post(CREATE_USER_URL, payload)


		self.assertEqual(res.status_code, status.HTTP_201_CREATED)

		user = get_user_model().objects.get(**res.data)
		self.assertTrue(user.check_password(payload['password']))
		self.assertNotIn('password', res.data)

	def test_user_exists(self):
		"""Test creating user that already exists fails"""

		payload = {
			'email': 'test@email.com',
			'password': 'test123',
			'name': 'Test Name',
		}

		create_user(**payload)

		res = self.client.post(CREATE_USER_URL, payload)

		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_password_too_short(self):
		"""Passowrd must be more than five characters"""

		payload = {
			'email': 'test@email.com',
			'password': 'pw',
			'name': 'Test Name',
		}

		res = self.client.post(CREATE_USER_URL, payload)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

		user_exists = get_user_model().objects.filter(
			email=payload['email']
		).exists()

		self.assertFalse(user_exists)


	# token tests

	def test_create_token_for_user(self):
		"""Test that a token is created for the user"""
		payload = {
			'email': 'test@email.com',
			'password': 'test123'
		}
		
		create_user(**payload)

		res = self.client.post(TOKEN_URL, payload)

		self.assertIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_200_OK)

	
	def test_create_token_invalid_credentials(self):
		"""Test that token is not created if invalid credentials are given"""

		create_user(email="test@email.com", password="testwrong")

		payload = {
			'email': 'test@email.com',
			'password': 'test123'
		}

		res = self.client.post(TOKEN_URL, payload)

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_token_no_user(self):
		"""Test that token is not created if user doesnt exist"""

		payload = {
			'email': 'test@email.com',
			'password': 'test123'
		}

		res = self.client.post(TOKEN_URL, payload)

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

	def test_create_token_missing_field(self):
		"""Test that email and password are required"""
		res = self.client.post(TOKEN_URL, {'email': 'email@email.com', 'password': ''})

		self.assertNotIn('token', res.data)
		self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)





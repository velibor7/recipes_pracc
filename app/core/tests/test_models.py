from django.test import TestCase
from django.contrib.auth import get_user_model 

#  get_user_model easier when changing in the future


class ModelTests(TestCase):

	def test_create_user_with_email_successful(self):
		"""Test creating a new user with email"""
		email = "test@email.com"
		password = "test123"

		# calls create user on user manager for our user model
		user = get_user_model().objects.create_user(
			email=email,
			password=password
		)

		self.assertEqual(user.email, email)

		#password is encrypted
		self.assertTrue(user.check_password(password))
	
	def test_new_user_email_normalized(self):
		"""Test that email for new user is normalized"""
		email = 'test@EMaIL.com'
		user = get_user_model().objects.create_user(email, 'test123')

		self.assertEqual(user.email, email.lower())

	def test_new_user_invalid_email(self):
		"""Test creating user with no email raises an error"""
		with self.assertRaises(ValueError):
			get_user_model().objects.create_user(None, 'test123')

	def test_create_new_superuser(self):
		"""Test creating a new superuser"""
		user = get_user_model().objects.create_superuser(
			'test@email.com',
			'test123'
		)

		self.assertTrue(user.is_superuser)
		self.assertTrue(user.is_staff)







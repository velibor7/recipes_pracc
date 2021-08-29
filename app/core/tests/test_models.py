from django.test import TestCase
from django.contrib.auth import get_user_model 

from unittest.mock import patch

from core import models

#  get_user_model easier when changing in the future


def sample_user(email="test@email.com", password="test123"):
	"""Create a sample user"""
	return get_user_model().objects.create_user(email, password)

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

	def test_tag_str(self):
		"""Test the tag string representation"""
		tag = models.Tag.objects.create(
			user=sample_user(),
			name='Vegan'
		)

		self.assertEqual(str(tag), tag.name)

	def test_ingredient_str(self):
		"""Test the ingredient string representation"""
		ingredient = models.Ingredient.objects.create(
			user=sample_user(),
			name='Cucamber'
		)

		self.assertEqual(str(ingredient), ingredient.name)
	
	def test_recipe_str(self):
		"""Test the recipe string representation"""
		recipe = models.Recipe.objects.create(
			user=sample_user(),
			title="steak and mushroom sauce",
			time_minutes=50,
			price=5.00,
		)
		self.assertEqual(str(recipe), recipe.title)

	@patch('uuid.uuid4')
	def test_recipe_file_name_uuid(self, mock_uuid):
		"""Test that the iage is saved in the correct location"""
		uuid = 'test-uuid'
		mock_uuid.return_value = uuid
		file_path = models.recipe_image_file_path(None, 'myimage.jpg')

		exp_path = f'uploads/recipe/{uuid}.jpg'
		self.assertEqual(file_path, exp_path)

	

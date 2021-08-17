from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
										PermissionsMixin


class UserManager(BaseUserManager):
	
	def create_user(self, email, password=None, **extra_fields):
		"""Creates and saves new user"""

		if not email:
			raise ValueError("Users must have an email address")

		# creating new user model and assining to user
		user = self.model(email=self.normalize_email(email), **extra_fields) 
		# hashes an stuff, 
		user.set_password(password)
		# for multiple dbs
		user.save(using=self._db)
		
		# returns user model that we just created
		return user

	# no need to worry about extra field, we use it from command line
	def create_superuser(self, email, password=None, **extra_fields):
		"""Creates and saves new superuser"""
		user = self.create_user(email, password)

		user.is_superuser = True
		user.is_staff = True

		user.save(using=self._db)

		return user


class User(AbstractBaseUser, PermissionsMixin):
	"""Custom user model, using email instead of username"""
	email = models.EmailField(max_length=255, unique=True)
	name = models.CharField(max_length=255)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	objects = UserManager()

	USERNAME_FIELD = 'email'

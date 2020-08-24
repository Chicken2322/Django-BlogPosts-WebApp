from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class MyAccountManager(BaseUserManager):
	def create_user(self,email,username,password=None):
		if not email:
			raise ValueError("User must have an email id")
		if not username:
			raise ValueError("User must have an username ")

		user=self.model(
				email=self.normalize_email(email),
				username=username,
			)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self,email,username,password):
		user=self.create_user(
				email=self.normalize_email(email),
				username=username,
				password=password,
			)

		user.is_admin=True
		user.is_staff=True
		user.is_superuser=True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):

	email				=models.EmailField(verbose_name="email",unique=True,max_length=60)
	username			=models.CharField(max_length=40,unique=True)
	date_joined			=models.DateTimeField(verbose_name="date joined",auto_now_add=True)
	last_login			=models.DateTimeField(verbose_name="last login",auto_now=True)
	is_admin			=models.BooleanField(default=False)
	is_active			=models.BooleanField(default=True)
	is_staff			=models.BooleanField(default=False)
	is_superuser		=models.BooleanField(default=False)

	objects=MyAccountManager()

	USERNAME_FIELD="email"
	REQUIRED_FIELDS=["username"]

	def __str__(self):
		return self.email

	def has_perm(self,perm,obj=None):
		return self.is_admin

	def has_module_perms(self,app_level):
		return True


@receiver(post_save,sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender,instance=None,created=False,**kwargs):
	if created:
		Token.objects.create(user=instance)
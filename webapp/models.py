from django.db import models

from django.db import models

from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

from django.conf import settings

from django.db.models.signals import post_save

from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.urls import reverse
from django.conf.urls.static import static

class MyAccountManager(BaseUserManager):

	def create_user(self, email,firstname,password=None):

		if not email:

			raise ValueError('The Email must be set')

		if not firstname:

			raise ValueError('The firstname must be set')

		user=self.model(

			email=self.normalize_email(email),

			firstname=firstname,

			)

		user.set_password(password)

		user.save(using=self._db)

		return user



	def create_superuser(self, email,firstname,password):

		user=self.create_user(

			email=self.normalize_email(email),

			password=password,

			firstname=firstname,

			)

		user.is_admin=True

		user.is_staff=True

		user.is_superuser=True

		user.save(using=self._db)

		return user



class UserMaster(AbstractBaseUser):

	UserID=models.AutoField(primary_key=True)

	email=models.EmailField(max_length=255,null=True,unique=True)

	firstname=models.CharField(max_length=255)

	lastname=models.CharField(max_length=255)

	password=models.CharField(max_length=255)
	
	date_joined=models.DateTimeField(verbose_name='date joined',auto_now_add=True)

	last_login=models.DateTimeField(verbose_name='last login',auto_now=True)

	is_admin=models.BooleanField(default=False)

	is_active=models.BooleanField(default=True)

	is_staff=models.BooleanField(default=False)

	is_superuser=models.BooleanField(default=False)



	USERNAME_FIELD='email'

	REQUIRED_FIELDS=['password','firstname']



	objects=MyAccountManager()



	def __str__(self):

		return self.email



	def has_perm(self,perm,obj=None):

		return self.is_admin



	def has_module_perms(self,app_label):

		return True





@receiver(post_save,sender=settings.AUTH_USER_MODEL)

def create_auth_token(sender,instance=True,created=False,**kwargs):

	if created:

		Token.objects.create(user=instance)


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)


class ImageMaster(models.Model):
	ImageID=models.AutoField(primary_key=True)
	UserID = models.ForeignKey(UserMaster,null=True,on_delete=models.SET_NULL)
	image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

	def __str__(self):

		return self.ImageID

class LikeMaster(models.Model):
	LikeID=models.AutoField(primary_key=True)
	ImageID=models.ForeignKey(ImageMaster,null=True,on_delete=models.SET_NULL)
	UserID = models.ForeignKey(UserMaster,null=True,on_delete=models.SET_NULL)
    
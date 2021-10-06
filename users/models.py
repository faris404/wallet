from django.db import models

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
   
   def create_user(self, email, password, is_active=True,**extra_fields):
      if not email:
         raise ValueError("User must have an email")
      if not password:
         raise ValueError("User must have a password")
      user = self.model(
         email=self.normalize_email(email)
      )
      user.set_password(password)  
      user.is_superuser = False
      user.is_staff = False
      user.active = is_active
      user.save(using=self._db)
      return user
      

   def create_superuser(self, email, password, **extra_fields):
      if not email:
         raise ValueError("User must have an email")
      if not password:
         raise ValueError("User must have a password")

      user = self.model(
         email=self.normalize_email(email)
      )
      user.set_password(password)
      user.is_superuser = True
      user.is_staff = True
      user.active = True
      user.save(using=self._db)
      return user



class User(AbstractUser):
 
   USERNAME_FIELD = 'email'
   REQUIRED_FIELDS = []
   email = models.CharField(max_length=200,unique=True)
   username = None
   objects = UserManager()
   class Meta:
      db_table="user"

class Person(models.Model):
 
   mobile = models.CharField(max_length=12,unique=True)
   name = models.CharField(max_length=50,null=False)
   user_id = models.ForeignKey(User, on_delete=models.CASCADE,db_column="user_id")
   class Meta:
      db_table="person"


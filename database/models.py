import datetime
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import os 

#Managing how users are saved
class MyUserManager(BaseUserManager):
    #Manage creation of regular user
    def create_user(self, email, username,first_name,last_name,date_of_birth, password=None, avatar=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        if not first_name:
            raise ValueError("User must have a first name ")
        if not last_name:
            raise ValueError("User must have a last name")
        if not date_of_birth:
            raise ValueError("User must have a date of birth")
        #if not password:
        #   raise ValueError("User must have a password")
            
        user = self.model(
               email = self.normalize_email(email),
               username = username,
               first_name = first_name,
               last_name = last_name,
               date_of_birth = date_of_birth,
               )
        user.set_password(password)
        user.save(using=self._db)
        return user
    #Mange regular user
    def create_superuser(self, email, username,first_name,last_name,date_of_birth,password, avatar=None):
        user = self.create_user(
               email = self.normalize_email(email),
               password = password,
               username = username,
               first_name = first_name,
               last_name = last_name,
               date_of_birth = date_of_birth,
               )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
        
    
# Create your models here.
class User(AbstractBaseUser):
    #Define email to use for sign in
    email = models.EmailField(verbose_name='email',max_length=60, unique=True)
    
    #Required fields
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    
    #Custom fields
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(max_length=8)
    balance = models.DecimalField(default=1000,max_digits=11, decimal_places=2)
    avatar = models.FileField(null=True,blank=True,upload_to='static/authentication')
    
    #Defines what filed is used to log in
    USERNAME_FIELD = 'email'
    
    #Defines what fields are required to sign up
    REQUIRED_FIELDS= ['username','first_name','last_name','date_of_birth']
    
    #Define the user manager to the user model
    objects = MyUserManager()
    
    def __str__(self):
        return self.first_name + " " + self.last_name
        
    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    
    def filename(self):
        return os.path.basename(self.avatar.name)
    
class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='static/authentication')
    likes = models.ManyToManyField(User, related_name ='item_post', blank=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
        
    def total_likes(self):
        return self.likes.count()
    
    def filename(self):
        return os.path.basename(self.image.name)

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, related_name="comments", on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.text
    
class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment , related_name="replies", on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.text
    

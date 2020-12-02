import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(max_length=8)
    status = models.CharField(max_length=9)
    password = models.CharField(max_length= 50)
    email = models.EmailField()
    def __str__(self):
        return self.first_name + " " + self.last_name
    
class Item(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    image = models.ImageField()
    price = models.DecimalField(max_digits=11, decimal_places=2)
    description = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.text
    
class Reply(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment , on_delete=models.CASCADE)
    text = models.CharField(max_length=10000)
    pub_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.text
    

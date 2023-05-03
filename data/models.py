from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from datetime import date
import PIL

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255)
    about = models.TextField()
    logo = models.ImageField(upload_to='images/')
    telephone = models.CharField(max_length=16)
    email = models.EmailField()
    address = models.CharField(max_length=255)
    terms = models.TextField()
    website = models.URLField()

    def __str__(self):
        return self.name

class Faq(models.Model):
    category = models.CharField(max_length=64)
    question = models.CharField(max_length=255)
    answer = models.TextField()

    def __str__(self):
        return self.question
    
class Package(models.Model):
    name = models.CharField(max_length=255)
    credits = models.IntegerField()
    duration = models.IntegerField()
    price = models.IntegerField()

    def __str__(self):
        return self.name
    
class Customer(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    telephone = models.CharField(max_length=16)
    balance = models.IntegerField(default=0)

    def purchase(self, package):
        if (self.balance >= package.price):
            self.balance -= package.price
            self.save()
            return True
        else:
            return False
        
    def __str__(self):
        return self.user.username
    
class Space(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    size = models.IntegerField()
    photo = models.ImageField(upload_to='images/')
    credits = models.IntegerField()

    def __str__(self):
        return self.name

class Booking(models.Model):
    space = models.ForeignKey(Space, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date = models.DateField()

    class Meta:
        ordering = ["date"]
        
    def __str__(self):
        return self.customer.user.username+':'+self.space.name

class PackageDetails(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    credits = models.IntegerField()
    dueDate = models.DateField()

    class Meta:
        ordering = ['dueDate']
        
    def __str__(self):
        return self.customer.user.username+':'+self.package.name
    
class CleanUp(models.Model):
    date = models.DateField()
    credits = models.IntegerField()
    
    class Meta:
        ordering = ['-date']
        
    def __str__(self):
        return self.date.strftime("%Y-%m-%d")
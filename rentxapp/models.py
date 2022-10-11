from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['firstname']) < 2:
            errors["firstname"] = "First name should be at least 5 characters"
        if len(postData['lastname']) < 2:
            errors["lastname"] = "Last name should be at least 5 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData["password_confirm"] != postData["password"]:
            errors["password_confirm"] = "Please make sure passwords match."
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):          
            errors['email'] = "Invalid email address!"
        return errors
    
class User(models.Model):
    firstname = models.CharField(max_length=75, blank = False)
    lastname = models.CharField(max_length=75, blank = False, null = True)
    email = models.CharField(max_length=255, blank = False)
    password = models.CharField(max_length=75, blank = False)
    password_confirm = models.CharField(max_length=75, blank = False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class ProductManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['name'] == "":
            errors["name"] = "Name of the proudct is required."
        if len(postData['desc']) < 15:
            errors["desc"] = "Product Description should be at least 15 characters. "
        if postData['location'] == "":
            errors["location"] = "Product's location is required."
        if postData['price'] == "":
            errors["price"] = "Product's price is required."
        
        return errors
        
class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    offered_by= models.ForeignKey(User, related_name="products_offered", on_delete = models.CASCADE)
    #product_image=models.ImageField(upload_to='images/', default=None)
    price = models.IntegerField()
    location = models.CharField(max_length=255)
    category=  models.ForeignKey(Category, related_name="products", on_delete = models.CASCADE,null=True )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ProductManager() 

class Rental(models.Model):
    renter= models.ForeignKey(User, related_name="provider", on_delete = models.CASCADE)
    rentee= models.ForeignKey(User, related_name="taker", on_delete = models.CASCADE)
    rented_product= models.OneToOneField(Product, on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status= models.IntegerField(default=0)
    

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

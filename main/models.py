from curses import ALL_MOUSE_EVENTS
from datetime import date
from unittest.util import _MAX_LENGTH
from django.db import models
import re

class UserManager(models.Manager):
    def user_validator(self,post_data):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post_data['fname']) < 2:
            errors['fname']='First name needs to be 2 characters'
        if len(post_data['lname']) < 2:
            errors['lname']='Last name needs to be 2 characters'
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email']='Check your email'
        if len(post_data['password']) < 8:
            errors['password']='Password needs to be 8 characters'   
        return errors
    def login_validator(self,post_data):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(post_data['email']):
            errors['email']='Check your email'
        if len(post_data['password']) < 8:
            errors['password']='Password needs to be 8 characters'   
        return errors

class User(models.Model):
    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Expense(models.Model):
    expenseTitle = models.CharField(max_length=50)
    amount = models.FloatField(max_length=50)
    category = models.CharField(max_length=50)
    submitter= models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    description = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
FORM_NAME_REGEX = re.compile(r'^[a-zA-Z- ]+$')

#UserManager will be used to validate users upon login and registration.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name must be at least 2 characters."

        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name must be at least 2 characters."

        if len(postData['email']) < 5:
            errors["email"] = "Email must be at least 5 characters."

        emails = User.objects.filter(email=postData["email"])
        if emails:
            errors["email"] = "Email address already exists."

        if len(postData['password']) < 8:
            errors["password"] = "Password must be at least 8 characters."

        if postData['password'] != postData['confirm_password']:
            errors["password"] = "Password fields must match."

        return errors

class BookManager(models.Manager):
    def book_validator(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Title is required."
        if len(postData['desc']) < 5:
            errors["desc"] = "Description is required."
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=60)
    password = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
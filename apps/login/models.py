from __future__ import unicode_literals
import re
from django.db import models

ALL_LETTERS_REGEX = re.compile(r'[A-Za-z]+')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
      
        if len(postData['name']) < 2: 
            errors['name_length'] = 'Name should be more than 2 characters'
        else:
            if not postData['name'].isalpha():
                errors['name_letters'] = 'Name should be letters only'

        if len(postData['email']) == 0 or not EMAIL_REGEX.match(postData['email']):      
            errors['email'] = 'Email is required and to be in a valid format'
        
        #  checks if email is taken
        email_taken = User.objects.filter(email = postData['email'])
        if len(email_taken) > 0 :
            errors['email taken'] = 'Email already in our database'        

        if len(postData['pw']) < 8:
            errors['pw_length'] = 'Password needs to be at least 8 characters'
        else:
            if postData['pw'] != postData['pw_confirm'] :
                errors['pw_conf'] = 'Passwords do not match'
        print "ERRORS", errors

        return errors

class AuthorManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['author']) == 2: 
            errors['author_name_length'] = "Author's name should be more than 2 characters"
        return errors

class BookManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['title']) == 0: 
            errors['title_blank'] = "Title can't be blank"
        return errors


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    pw = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(Author, related_name = "books")
    objects = BookManager()

class Review(models.Model):
    rating = models.IntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name='reviews')
    book = models.ForeignKey(Book, related_name='reviews')





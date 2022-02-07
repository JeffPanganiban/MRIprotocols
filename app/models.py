from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def reg_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be at least 2 characters"
        if len(postData['facility']) < 2:
            errors['facility'] = "Facility name must be at least 2 characters"
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Enter a valid email address"
        check_user = User.objects.filter(email=postData['email'])
        if len(check_user) > 0:
            errors['email'] = "Email already registered"
        if len(postData['password']) < 8:
            errors['password'] = "Password must be at least 8 characters"
        if postData['confirm_password'] != postData['password']:
            errors['password'] = "Passwords do not match"
        return errors

    def login_validator(self, postData):
        errors = {}
        check_user = User.objects.filter(email=postData['email'])
        if len(check_user) != 1:
            errors['email'] = "Email address not registered"
        if len(postData['email']) == 0:
            errors['email'] = "Invalid e-mail address"
        if len(postData['password']) < 8:
            errors['password'] = "Invalid password"
        elif bcrypt.checkpw(postData['password'].encode(), check_user[0].password.encode()) != True:
            errors['password'] = "Invalid email and password combination"
        return errors

class ScanManager(models.Manager):
    def seq_validator(self,postData):
        errors = {}
        if len(postData['plane']) < 1:
            errors['plane'] = "Must specificy a plane"
        if len(postData['weighting']) < 1:
            errors['weighting'] = "Must specificy weighting"
        if len(postData['fat_sat']) < 1:
            errors['fat_sat'] = "Must choose a fat saturation technique"
        return errors

    def protocol_validator(self,postData):
        errors = {}
        if len(postData['name']) < 1:
            errors['name'] = "Must enter a protocol name"
        return errors

class User(models.Model):
    email = models.CharField(max_length=255)
    facility = models.CharField(max_length=255)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Category (models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Protocol(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='protocols', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ScanManager()

class Sequence(models.Model):
    plane = models.CharField(max_length=255)
    weighting = models.CharField(max_length=255)
    slice = models.CharField(max_length=255, blank=True)
    gap = models.CharField(max_length=255, blank=True)
    fat_sat = models.CharField(max_length=255)
    fov = models.CharField(max_length=255, blank=True)
    notes = models.CharField(max_length=255, blank=True)
    protocol = models.ForeignKey(Protocol, related_name='sequences', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = ScanManager()
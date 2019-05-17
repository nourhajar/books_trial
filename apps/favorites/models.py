from django.db import models
import bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['email']) < 10:
            errors["email"] = "Email should be at least 10 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 2 characters"
        if postData['password'] != postData['confirm']:
            errors["password"] = "Passwords do not match"
        return errors
    def login_validator(self, postData):
        errors = {}
        if len(postData['email']) < 10:
            errors["email"] = "Please enter email"
        if len(postData['password']) < 8:
            errors["password"] = "Please enter password"
        user = User.objects.filter(email=postData['email']).values()
        if user == {}:
            errors["email"] = "Invalid email"
        if bcrypt.checkpw(postData['password'].encode(), user[0]['password'].encode()):
            pass
        else:
            errors["password"] = "Invalid password"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Book(models.Model):
    title = models.CharField(max_length=45)
    description = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
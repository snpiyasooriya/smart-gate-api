from django.db import models
from django.core.validators import MinLengthValidator, EmailValidator
from datetime import date
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from rest_framework.exceptions import ValidationError


class Employee(models.Model):
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(3, "First Name must be at least 3 characters")])
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(3, "Last Name must be at least 3 characters")])
    email = models.EmailField(unique=True, validators=[EmailValidator("This is not a valid email.")])
    address = models.CharField(max_length=255, validators=[MinLengthValidator(4, "Please enter a valid address.")])
    nic = models.CharField(max_length=12, validators=[MinLengthValidator(10, "Please enter a valid NIC address.")])
    dob = models.DateField()
    gender = models.CharField(max_length=10, choices=[('M', 'Male'), ('F', 'Female')])  # or use other choices
    designation = models.CharField(max_length=100)
    img_url = models.ImageField(upload_to='employees/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def clean(self):
        # Ensure date of birth is in the past
        if self.dob > date.today():
            raise ValidationError("Please select a valid DOB.")

class UserManager(BaseUserManager):
    def create_user(self, email, first_name, last_name, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email), first_name=first_name, last_name=last_name)
        user.set_password(password)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100, null=False, blank=False)  # Password field handled by AbstractBaseUser
    img_url = models.ImageField(upload_to='uploads/users/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

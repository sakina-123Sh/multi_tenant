from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, **extra_fields):
        if not email or not phone_number or not password:
            raise ValueError('Email, phone number, and password are required')
        email = self.normalize_email(email)
        user = self.model(email=email, phone_number=phone_number, **extra_fields)
        user.set_password(password)  # Use set_password to hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, phone_number, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, default='' , unique=True, validators=[
        RegexValidator(
            regex=r'^[\d\s()+-]+$',
            message='Phone number should only contain numeric, +, space, -, ( and ) characters',
            code='invalid_phone_number'
        )
    ])
    password = models.CharField(max_length=128)  # Store password as is

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'password']

    objects = UserManager()

    def __str__(self):
        return self.email

    def clean(self):
        from django.core.exceptions import ValidationError

        # Check if the combination of email and phone number is unique
        if User.objects.filter(email=self.email, phone_number=self.phone_number).exists():
            raise ValidationError('A user with this email and phone number already exists')

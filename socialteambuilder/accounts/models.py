from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin
)
from django.db import models
from django.utils import timezone

from .utils import send_confirmation_email


class UserManager(BaseUserManager):
    def create_user(self, email, first_name, password=None, confirmed=False):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        print("using custom user manager")
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name
        )
        user.set_password(password)
        user.save()
        if not confirmed:
            send_confirmation_email(user)
        return user

    def create_superuser(self, email, first_name, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
            first_name=first_name,
            confirmed=True
        )
        user.is_active = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    about = models.TextField(
        max_length=2500, 
        default="A little about you"
    )
    avatar = models.ImageField()
    skills = models.ManyToManyField("Skill", related_name="users") # on delete issues?
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        if not self.first_name:
            return self.email
        return self.first_name + " " + self.last_name

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin


class Skill(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class PortfolioProject(models.Model):
    """Model representing a website that the user has built 
    """
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name="portfolio_projects"
    )
    name = models.CharField(max_length="255")
    url = models.URLField()

    def __str__(self):
        return self.name
        
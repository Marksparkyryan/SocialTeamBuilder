from django.conf import settings
from django.core.files.storage import default_storage
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)

from django.db import models


class UserManager(BaseUserManager):
    """Custom manager for the User model
    """

    def create_user(self, email, first_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name
        )
        user.set_password(password)
        user.save()
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
        )
        user.is_active = True
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser):
    """Custom model for users
    """
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    about = models.TextField(
        max_length=2500,
        default="Markdown available, preview below."
    )
    avatar = models.ImageField(
        default="default_avatars/blank.png", 
        upload_to="avatars"
    )
    skills = models.ManyToManyField(
        "Skill", related_name="users")  # on delete issues?
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', ]
    
    @property
    def get_avatar_url(self):
        path = settings.MEDIA_ROOT + '/' + self.avatar.name
        if default_storage.exists(path):
            return self.avatar.url
        else:
            return '/media/default_avatars/blank.png'

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
    """Model for a skill that can be shared by users and positions
    """
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super(Skill, self).save(*args, **kwargs)


class PortfolioProject(models.Model):
    """Model representing a website that the user has built
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolio_projects"
    )
    name = models.CharField(max_length=255, unique=True)
    url = models.URLField()

    def __str__(self):
        return self.name

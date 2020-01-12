from django.contrib.auth import get_user_model
from django.db import models

from accounts.models import Skill

User = get_user_model()


class Project(models.Model):
    """Model representing a development project that users can create 
    and/or join
    """
    STATUS = (
        ('A', 'Open'),
        ('B', 'Closed'),
        ('C', 'Complete'),
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name="projects"
    )
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=2000)
    time_estimate = models.IntegerField()
    applicant_requirements = models.TextField(max_length=2000)
    status = models.CharField(max_length=1, choices=STATUS)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Position(models.Model):
    """Model representing a single position within a developing project
    that users can apply to
    """
    STATUS = (
        ('E', 'Empty'),
        ('F', 'Filled')
    )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=2000)
    skills = models.ManyToManyField(Skill, related_name="positions")
    status = models.CharField(max_length=1, choices=STATUS)
    time_estimate = models.IntegerField()

    def __str__(self):
        return self.title


class Application(models.Model):
    """Model representing a user's application to a project's
    position
    """
    STATUS = (
        ('A', 'Accepted'),
        ('R', 'Rejected'),
        ('U', 'Undecided')
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    position = models.OneToOneField(
        Position,
        on_delete=models.CASCADE,
        related_name="applications"
    )
    status = models.CharField(max_length=1, choices=STATUS)

    def __str__(self):
        return "{} applied to {}".format(
            self.user.first_name,
            self.position.title
        )


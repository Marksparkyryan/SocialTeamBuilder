from django.contrib.auth import get_user_model
from django.db import models


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
    owner = models.ForeignKey(User, on_delete=models.PROTECT, related_name="projects")
    title = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=2000)
    time_estimate = models.IntegerField()
    applicant_requirements = models.TextField(max_length=2000)
    status = models.CharField(max_length=1, choices=STATUS)



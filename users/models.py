from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Userprofile(models.Model):
	firstname = models.CharField(max_length=200, null=True)
	lastname = models.CharField(max_length=200, null=True)
	title = models.CharField(max_length=200, null=True)
	tags = models.CharField(max_length=100, null=True)
	about = models.TextField(null=True)
	image = models.ImageField(upload_to='images', null=True)
	user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )
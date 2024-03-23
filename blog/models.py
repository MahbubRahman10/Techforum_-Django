from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Blogpost(models.Model):

	title = models.CharField(max_length=200)
	category = models.CharField(max_length=100, null=True)
	image = models.ImageField(upload_to='blog', null=True)
	description = models.TextField()
	datetime = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)


class Blogcomment(models.Model):

	name = models.CharField(max_length=200)
	email = models.CharField(max_length=100)
	description = models.TextField()
	datetime = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	blogpost = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
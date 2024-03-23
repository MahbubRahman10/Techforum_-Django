from django.db import models

from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Category(models.Model):
	name = models.CharField(max_length=100)
	datetime = models.DateTimeField(default=timezone.now)


class forum(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	bestreply = models.IntegerField(default=0)
	num_reply = models.IntegerField(default=0)
	visitor = models.IntegerField(default=0)
	datetime = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Reply(models.Model):
	description = models.TextField()
	best = models.BooleanField(default=False)
	like = models.IntegerField(default=0)
	datetime = models.DateTimeField(default=timezone.now)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	forum = models.ForeignKey(forum, on_delete=models.CASCADE)


class Userlike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	reply = models.ForeignKey(Reply, on_delete=models.CASCADE)
	datetime = models.DateTimeField(default=timezone.now)






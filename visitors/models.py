from django.db import models

from django.utils import timezone
from forum.models import forum 

# Create your models here.

class Questionvisitor(models.Model):
	visitor_ip = models.CharField(max_length=100)
	datetime = models.DateTimeField(default=timezone.now)
	forum = models.ForeignKey(forum, on_delete=models.CASCADE)
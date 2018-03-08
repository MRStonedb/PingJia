from django.db import models


# Create your models here.

class pingjia_info(models.Model):
    name = models.CharField(max_length=100)
    uname = models.CharField(max_length=100)
    content = models.CharField(max_length=1024)
    time = models.CharField(max_length=100)
    score = models.CharField(max_length=100)

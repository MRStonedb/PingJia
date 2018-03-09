from django.db import models

# Create your models here.

class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=60)
    uphone = models.CharField(max_length=30)
    isActive = models.BooleanField(default=False)
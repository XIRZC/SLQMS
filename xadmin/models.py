from django.db import models

# Create your models here.

class User(models.Model):
    uid = models.CharField(max_length=10)
    upwd = models.CharField(max_length=10)
from django.contrib.auth.models import User
from django.db import models

class Bio(models.Model):
    name = models.CharField(max_length=200)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)



# Create your models here.

from django.contrib.auth.models import User
from django.db import models

class Bio(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    username = models.ForeignKey(User, to_field="username", on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    address = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)

# Create your models here.

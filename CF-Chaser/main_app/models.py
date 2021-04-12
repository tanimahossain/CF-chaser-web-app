from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    cfHandle = models.CharField(max_length=50, default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return  self.cfHandle

class Friend(models.Model):
    cfHandle = models.CharField(max_length=50, default=None)
    friend_of = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return self.cfHandle
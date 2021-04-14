from django.db import models
from django.contrib.auth.models import User

class Friend(models.Model):
    cfHandle = models.CharField(max_length=50, default=None)
    friend_of = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.cfHandle
from django.db import models
from django.contrib.auth.models import User


class FileInfo(models.Model):
    name = models.CharField(max_length=200, null=False)
    path = models.CharField(max_length=500, null=True)
    size = models.IntegerField(null = False)
    hash_md5 = models.CharField(max_length=32,null=False)
    # user = models.ForeignKey(User.username,on_delete=models.CASCADE)
    user = models.CharField(max_length=100,null=False)

    def __str__(self):
        return self.name

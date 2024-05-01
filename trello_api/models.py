from datetime import datetime
from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name=models.CharField(max_length=50,null=True)
    joinDate=models.DateTimeField(default=datetime.now)
    mailId=models.CharField(max_length=50,null=True)
    password=models.CharField(max_length=50,null=True)
    isActive=models.BooleanField(null=True)
    

class Column(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    Date=models.DateTimeField(default=datetime.now)
    userId=models.ForeignKey(User,on_delete=models.CASCADE,null=True)

class Card(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    column = models.ForeignKey(Column, related_name='cards', on_delete=models.CASCADE)

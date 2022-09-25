from distutils.command.upload import upload
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    STATUS = (
        ('ONLINE','ONLINE'),
        ('OFFLINE','OFFLINE'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    status = models.CharField(max_length=100, null=True,default="Available")
    active = models.CharField(choices=STATUS,max_length=100,null=True)
    image = models.ImageField(upload_to="profileimage",null=True)

    def __str__(self):
        return self.user.username+" "+self.status

class FriendList(models.Model):
    user = models.ForeignKey(User,related_name='mainuser',on_delete=models.CASCADE)
    friend = models.ForeignKey(User,related_name='userfriend',on_delete=models.CASCADE)
    lastseen = models.DateTimeField(null=True)
    def __str__(self):
        return self.user.username+" "+self.friend.username+" "+str(self.lastseen)

class ChatRoom(models.Model):
    sender = models.ForeignKey(User,related_name='sender',on_delete=models.CASCADE)
    receiver = models.ForeignKey(User,related_name='receiver',on_delete=models.CASCADE)
    msg = models.CharField(max_length=200,null=True)
    status = models.BooleanField(null=True)
    sendtime = models.DateTimeField(null=True)
    def __str__(self):
        return self.sender.username+" "+self.receiver.username
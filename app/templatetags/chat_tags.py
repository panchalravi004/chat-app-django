from django import template
import math
from django.db.models import Sum
from app.models import *
register = template.Library()

@register.simple_tag
def getProfile(user):
    profile = UserProfile.objects.get(user=user)
    return profile

@register.simple_tag
def checkFriend(user,friend):
    profile = FriendList.objects.filter(user=user).filter(friend=friend)
    if profile.exists():
        return True
    return False

@register.simple_tag
def removeCurrentUser(user,friend):
    if user==friend:
        return True
    return False

@register.simple_tag
def getFriendData(friend):
    user = User.objects.get(id=friend)
    return user

@register.simple_tag
def checkOnline(friend):
    user = UserProfile.objects.get(user=friend)
    if user.active == "ONLINE":
        return True
    else:
        return False

@register.simple_tag
def checkUser(user,sender):
    
    if user == sender:
        return True
    else:
        return False

@register.simple_tag
def countUnseenMsg(friend,user):
    
    count = ChatRoom.objects.filter(sender=friend,receiver=user).filter(status=False).count()
    return count


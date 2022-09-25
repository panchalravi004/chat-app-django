from logging import lastResort
from django.shortcuts import redirect, render
from django.http import *
from django.contrib.auth.models import User
from datetime import datetime
from app.models import ChatRoom, FriendList, UserProfile
from django.template.loader import render_to_string

def BASE(request):
    return render(request,'base.html')

def HOME(request):
    if request.user.is_authenticated:
        user = request.user
        profile = UserProfile.objects.get(user=user)
        userlist = User.objects.all().order_by('-id')

        friendlist = FriendList.objects.filter(user=request.user).order_by('-lastseen')
        data = {
            'user':user,
            'userlist':userlist,
            'profile':profile,
            'friendlist':friendlist,
        }
        return render(request,'Main/home.html',data)
    else:
        return redirect('login')

def ADDFRIEND(request):
    if request.method == "GET":
        now = datetime.now()
        user = request.user
        friend = User.objects.get(id=request.GET.get('user'))

        main_friendlist = FriendList(
            user=user,
            friend=friend,
            lastseen=now,
        )
        main_friendlist.save()
        
        fd_friendlist = FriendList(
            user=friend,
            friend=user,
            lastseen=now,
        )
        fd_friendlist.save()

        return redirect('home')

def SEARCHUSER(request):
    search = request.GET.get('search')
    if search !="":
        users = User.objects.filter(username__icontains=search)
        profile = UserProfile.objects.get(user=request.user)
        friendlist = FriendList.objects.filter(user=request.user).order_by('-lastseen')

        data = {
            'user':request.user,
            'profile':profile,
            'friendlist':friendlist,
            'userlist':users
        }
        t = render_to_string('ajax/alluser.html',data)

        return JsonResponse({'data': t})

    else:
        users = User.objects.all().order_by('-id')
        profile = UserProfile.objects.get(user=request.user)
        friendlist = FriendList.objects.filter(user=request.user).order_by('-lastseen')

        data = {
            'user':request.user,
            'profile':profile,
            'friendlist':friendlist,
            'userlist':users
        }
        t = render_to_string('ajax/alluser.html',data)

        return JsonResponse({'data': t})

def CHATWINDOW(request):
    user_id = request.GET.get('friend_id')
    friend = User.objects.get(id=user_id)

    users = User.objects.all().order_by('-id')
    profile = UserProfile.objects.get(user=request.user)
    friendlist = FriendList.objects.filter(user=request.user).order_by('-lastseen')

    #get chats
    uchat = ChatRoom.objects.filter(sender=request.user,receiver=friend)
    fchat = ChatRoom.objects.filter(sender=friend,receiver=request.user)
    chat = uchat | fchat
    # print(chat.count())
    
    # seen the unseen messages
    unseenmsg = ChatRoom.objects.filter(sender=friend,receiver=request.user).filter(status=False)

    for msg in unseenmsg:
        m = ChatRoom.objects.get(id=msg.id)
        m.status=True
        m.save()

    data = {
        'friend':friend,
        'chat':chat.order_by('sendtime'),
        'user':request.user,
        'profile':profile,
        'friendlist':friendlist,
        'userlist':users
    }
    t = render_to_string('ajax/chat_window.html',data)

    return JsonResponse({'data': t})

def FETCHMESSAGE(request):
    friend = User.objects.get(id=request.GET.get('friend'))
    #get chats
    uchat = ChatRoom.objects.filter(sender=request.user,receiver=friend)
    fchat = ChatRoom.objects.filter(sender=friend,receiver=request.user)
    chat = uchat | fchat

    data = {
        'user':request.user,
        'friend':friend,
        'chat':chat.order_by('sendtime'),
    }
    t = render_to_string('ajax/fetch_messages.html',data)

    return JsonResponse({'data': t})

def SENDMESSAGE(request):
    # if request.method == "GET":
    user = User.objects.get(id=request.GET.get('user'))
    frd = User.objects.get(id=request.GET.get('friend'))
    msg = request.GET.get('msg')
    now = datetime.now()

    chat = ChatRoom(
        sender=user,
        receiver=frd,
        msg=msg,
        sendtime=now,
        status=False
    )
    chat.save()

    updatelastseen = FriendList.objects.filter(user=frd,friend=user).first()
    updatelastseen.lastseen=now
    updatelastseen.save()

    return redirect('home')

def CLEARCHAT(request,action,fdid):
    #get chats
    friend = User.objects.get(id=fdid)
    uchat = ChatRoom.objects.filter(sender=request.user,receiver=friend)
    fchat = ChatRoom.objects.filter(sender=friend,receiver=request.user)
    chat = uchat | fchat

    if action == "delete":
        getlist1 = FriendList.objects.filter(user=request.user,friend=friend).first()
        getlist2 = FriendList.objects.filter(user=friend,friend=request.user).first()

        one = FriendList.objects.get(id=getlist1.id)
        two = FriendList.objects.get(id=getlist2.id)
        one.delete()
        two.delete()

    elif action == "clear":
        for c in chat:
            getchat = ChatRoom.objects.get(id=c.id)
            getchat.delete()

    return redirect('home')

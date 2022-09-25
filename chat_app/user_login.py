from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from app.models import UserProfile

from chat_app import EmailBackend

from django.core.files.storage import FileSystemStorage

def REGISTER(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(email=email).exists():
            messages.warning(request,"Email are Already Exists !")
            return redirect('login')
        else:
            user = User(
                email=email,
                username=username
            )
            user.set_password(password)
            user.save()
            profile = UserProfile(
                user=user,
            )
            profile.save()
            messages.success(request,"Registration success !")
            return redirect('login')

def LOGIN(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackend.EmailBackEnd.authenticate(request,username=email,password=password)

        if user != None:
            login(request,user)
            profile = UserProfile.objects.get(user=request.user)
            profile.active="ONLINE"
            profile.save()
            return redirect('home')
        else:
            messages.error(request,'Email and Password Are Invalid !')
            return redirect('login')
    return None

def LOGOUT(request):
    profile = UserProfile.objects.get(user=request.user)
    profile.active="OFFLINE"
    profile.save()
    logout(request)
    return redirect('login')

def PROFILEUPDATE(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        status = request.POST.get('status')
        userid = request.user.id

        user = User.objects.get(id=userid)
        user.username = username
        user.email = email

        if password !="" and password != None:
            user.set_password(password)
        user.save()

        profile = UserProfile.objects.get(user=user)
        profile.status = status
        profile.save()

        return redirect('home')

def IMAGEUPLOAD(request):
    if request.method == "POST" and request.FILES['image']:
        image = request.FILES['image']
        fss = FileSystemStorage()
        file = fss.save('profileimage/ '+request.user.email+'.jpg',image)
        file_url = fss.url(file)

        user = UserProfile.objects.filter(user=request.user)
        if user.exists():
            userimg = UserProfile.objects.get(user=request.user)
            userimg.user = request.user
            userimg.image = file_url
            userimg.save()
            messages.success(request,"Image Uploaded !")
            return redirect('home')
        else:
            userimg = UserProfile(
                user=request.user,
                image=file_url,
            )
            userimg.save()
            messages.success(request,"Image Uploaded !")
            return redirect('home')


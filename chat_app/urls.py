"""chat_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include
from . import views, user_login

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base/', views.BASE,name='base'),
    path('', views.HOME,name='home'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/register/',user_login.REGISTER,name='register'),
    path('dologin/',user_login.LOGIN,name='dologin'),
    path('logout/',user_login.LOGOUT,name='logout'),
    path('accounts/profile/update/',user_login.PROFILEUPDATE,name='profile_update'),
    path('accounts/profile/imageupload/',user_login.IMAGEUPLOAD,name='image_upload'),
    path('addfriend/',views.ADDFRIEND,name='add_friend'),
    path('search-user', views.SEARCHUSER,name='search_user'),
    path('chat-window', views.CHATWINDOW,name='chat_window'),
    path('chat-window/send-message', views.SENDMESSAGE,name='send_message'),
    path('chat-window/fetch-message', views.FETCHMESSAGE,name='fetch_message'),
    path('chat-window/<action>/<fdid>', views.CLEARCHAT,name='clear_chat'),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

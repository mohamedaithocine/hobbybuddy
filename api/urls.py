"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.http import HttpResponse

from api import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.main_spa, name='main'),
    path('api/check-login/', views.check_login, name='check_login'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('users/', views.users_api, name='users'),
    path('edituser/', views.user_api, name='user'),
    path('hobbies/', views.hobbies_api, name='hobbies'),
    path('addhobby/', views.hobby_api, name='hobby'),
    path('users/<int:user_id>/friends/', views.friends, name='friends'),
    path('users/<int:user_id>/friend_requests_by_user/', views.friend_requests_by_user, name='friend_requests_by_user'),
    path('users/<int:user_id>/friend_requests_to_user/', views.friend_requests_to_user, name='friend_requests_to_user'),
    path('changepassword/', views.change_password, name='change_password'),
    path('get_similar_users/', views.get_similar_users, name='get_similar_users'),
    path('send_friend_request/<str:username>/', views.send_friend_request, name='send_friend_request'),
    path('friends/<int:friend_id>/accept/', views.accept_friend_request, name='accept_friend_request'),
    path('friends/<int:friend_id>/reject/', views.reject_friend_request, name='reject_friend_request'),
    path('friends/<int:friend_id>/remove/', views.remove_friend, name='remove_friend'),
    path('get-csrf-token/', views.get_csrf_token, name='get_csrf_token'),
]

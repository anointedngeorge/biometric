
from django.contrib import admin
from django.urls import path
from dashboard.views.authentication import *
# from django.conf.urls import url

auth_pattern = [
    path('index/', index, name='index'),
    path('login/', auth_login, name='login'),
    path('page/', page, name='page'),
    path('logout/', auth_logout, name='logout'),
]

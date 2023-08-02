
from django.contrib import admin
from django.urls import path
from dashboard.views.level import *
# from django.conf.urls import url

level_pattern = [
    path('levels/', LevelVIew.as_view(), name='levels'),
]


from django.contrib import admin
from django.urls import path
from dashboard.views.students import *
# from django.conf.urls import url

student_pattern = [
    path('student/', StudentView.as_view(), name='student'),
]

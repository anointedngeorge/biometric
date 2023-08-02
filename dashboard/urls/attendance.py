
from django.contrib import admin
from django.urls import path
from dashboard.views.attendance import *
# from django.conf.urls import url

attendance_pattern = [
    path('register_attendance/', AttendanceView.as_view(), name='register_attendance'),
]


from django.contrib import admin
from django.urls import path
from dashboard.views.courses import *
# from django.conf.urls import url

course_pattern = [
    path('courses/', CoursesView.as_view(), name='courses'),
    # path('courses/', CoursesListView.as_view(), name='courses'),
]

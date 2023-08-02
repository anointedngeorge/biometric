
from django.contrib import admin
from django.urls import path
from dashboard.views.lecturer import *
# from django.conf.urls import url

lecturer_pattern = [
    path('lecturer/', LecturerView.as_view(), name='lecturer'),
    path('lecturer/<str:new_data>', LecturerView.as_view(), name='lecturer'),
    # path('courses/', CoursesListView.as_view(), name='courses'),
]

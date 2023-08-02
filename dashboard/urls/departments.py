
from django.contrib import admin
from django.urls import path
from dashboard.views.departments import *
# from django.conf.urls import url

department_pattern = [
    path('department/', DepartmentVIew.as_view(), name='department'),
    # path('courses/', CoursesListView.as_view(), name='courses'),
]

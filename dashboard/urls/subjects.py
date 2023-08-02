
from django.contrib import admin
from django.urls import path
from dashboard.views.subjects import *
# from django.conf.urls import url

subject_pattern = [
    path('subjects/', SubjectView.as_view(), name='subjects'),
    path('subjects/register', StudentRegisterSubjectView.as_view(), name='subjectRegister'),
]

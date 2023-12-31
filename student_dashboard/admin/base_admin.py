from typing import Any, Dict, List, Optional
from django.http import HttpResponse
from django.contrib import messages as mesage
from django.contrib import admin
from django.urls.resolvers import URLResolver
from django.urls import path, include, re_path
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from student_dashboard.forms.authentication import (
    CustomAuthenticationForm,
    AuthenticationRegisterForm
)

from authuser.forms.student import (
    StudentForm,UpdateStudentForm
)
from authuser.models import *

import os


CURRENT_MAIN_TEMPLATE = 'student_dashboard'
DASHBOARD_NAME = 'student'
CURRENT_TEMPLATE = DASHBOARD_NAME
# student/logout/
# student/password_change/
# <form method="post" id="login-form" action="{% url 'admin:login' %}">
# <form method="post" id="login-form" action="{% url 'admin:login' %}?next={{ request.GET.next }}">

class StudentDashboard(admin.AdminSite):
    site_title = 'Student Admin'
    site_header = 'Student Dashboard'
    index_title = 'Student Dashboard'
    index_template = f'{CURRENT_TEMPLATE}/index.html'
    login_template = f'{CURRENT_TEMPLATE}/login.html'
    logout_template = f'{CURRENT_TEMPLATE}/logout.html'
    login_form = CustomAuthenticationForm
    
    


    def each_context(self, request):
        context = super().each_context(request)
        app_lists = self.get_app_list(request)
        
        context['title'] = self.site_title
        context['site_header'] = self.site_header
        context['index_title'] = self.index_title
        context['app_lists'] = app_lists
        # this will set the current adminsite app that is running
        context['adminsite'] = self.name
     
        return context
    
    def get_urls(self) -> List[URLResolver]:
        urls = super().get_urls()
        add_urls = [
            path('profile/', self.profile, name='profile'),
            path('test-fun1', self.profile, name='test-fun1'),
        ]
        return add_urls + urls


    def profile(self, request):
        context = self.each_context(request)
        student_instance = get_object_or_404(StudentModel, id=request.user.id)
        # Create the form instance using the fetched student instance
        student_dashboard_form = UpdateStudentForm(request.POST or None, instance=student_instance)
        context['student_dashboard_form'] = student_dashboard_form
       
        if request.method == 'POST':
            form = UpdateStudentForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
        return TemplateResponse(request, 'student/profile.html', context=context)
    
student_dashboard_site = StudentDashboard(name=f'{DASHBOARD_NAME}')

# student_dashboard_site.register(User)


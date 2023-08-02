from typing import Any, Dict, List, Optional
from django.http import HttpResponse
from django.contrib import messages as mesage
from django.contrib import admin
from django.urls.resolvers import URLResolver
from django.urls import path, include, re_path

from django.template.response import TemplateResponse

from lecturer_dashboard.forms.authentication import (
    CustomAuthenticationForm,
    AuthenticationRegisterForm
)
from authuser.models import *

import os

CURRENT_TEMPLATE = 'argon'
CURRENT_MAIN_TEMPLATE = 'lecturer_dashboard'
DASHBOARD_NAME = 'lecturer'

# student/logout/
# student/password_change/
# <form method="post" id="login-form" action="{% url 'admin:login' %}">
# <form method="post" id="login-form" action="{% url 'admin:login' %}?next={{ request.GET.next }}">

class LecturerDashboard(admin.AdminSite):
    site_title = 'Lecturer Admin'
    site_header = 'Lecturer Dashboard'
    index_title = 'Lecturer Dashboard'
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
            path('profile', self.profile, name='profile'),
            path('test-fun1', self.profile, name='test-fun1'),
        ]
        return add_urls + urls
    
    def profile(self, request):
        return HttpResponse('Loading')
    

lecturer_dashboard_site = LecturerDashboard(name=f'{DASHBOARD_NAME}')



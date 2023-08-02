from typing import List, Optional
from django.contrib import admin
from django.contrib.admin.sites import site
from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls.resolvers import URLPattern
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.html import format_html
from django.utils.safestring import mark_safe
# from etc.actions import *
from django.http import HttpResponseRedirect
from django import template
# from django.utils.translation import ugettext as _
import uuid
from authuser.models import *
from django.urls import path, include, re_path
from authuser.forms.student import StudentForm



@admin.register(StudentModel)
class StudentAdmin(admin.ModelAdmin):
    list_display = STUDENT_LIST_DISPLAY
    # form = StudentForm

    def response_add(self, request: HttpRequest, obj, post_url_continue=None) -> HttpResponse:
        filename = str(obj.picture_url).split('/')[1].split('.')[0] if obj.picture_url  else ''
        obj.picture_name = filename
        obj.save()
        return super().response_add(request, obj, post_url_continue)
    
    def response_change(self, request: HttpRequest, obj) -> HttpResponse:
        filename = str(obj.picture_url).split('/')[1].split('.')[0]
        obj.picture_name = filename
        obj.save()
        return super().response_change(request, obj)
    

    def get_urls(self) -> List[URLPattern]:
        # student-attendance
        urls = super().get_urls()
        add_urls = [
            path('student-attendance/<str:id>/<str:fullname>', self.student_attendance, name='student-attendance')
        ]
        return add_urls + urls
    
    def student_attendance(self, request, id=None, fullname=None):
        context = dict(self.admin_site.each_context(request),)
        stud =  self.model.objects.all().filter(id=id).get()
        context['id'] =  id
        context['fullname'] = fullname
        context['attendance'] = stud.get_student_courses
        return TemplateResponse(request, 'student_view_attendance.html', context=context)


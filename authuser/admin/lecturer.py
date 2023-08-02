from typing import Any, Optional, List
from django.contrib import admin
from django.contrib.admin.sites import site
from django.db.models.query import QuerySet
from django.http import request
from django.http.request import HttpRequest
from django.http.response import HttpResponse, HttpResponseBase, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls.resolvers import URLPattern
# from etc.actions import *
from django.http import HttpResponseRedirect
from django import template
# from django.utils.translation import ugettext as _
import uuid
from authuser.models import *


@admin.register(LecturerModel)
class LecturerAdmin(admin.ModelAdmin):
    list_display = LECTURER_ADMIN_DISPLAY
    list_display_links = ['salutation','first_name']
    list_filter = ['first_name','last_name']


    def get_urls(self) -> List[URLPattern]:
        # student-attendance
        urls = super().get_urls()
        add_urls = [
            path('lecturer-student-attendance/<str:id>/<str:fullname>', self.lecturer_student_attendance, name='lecturer-student-attendance')
        ]
        return add_urls + urls
    
    def lecturer_student_attendance(self, request, id=None, fullname=None):
        context = dict(self.admin_site.each_context(request),)
        stud =  self.model.objects.all().filter(id=id).get()
        context['id'] =  id
        context['title'] = 'Lecturer - details'
        context['fullname'] = fullname
        context['attendance'] = stud.get_student_courses
        return TemplateResponse(request, 'lecture_view_attendance.html', context=context)


    

from typing import Any
from django import http
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from authuser.models.lecturer import LecturerModel
from dashboard.forms.auth import *
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views import View
import datetime
import calendar
from django.views.generic import ListView
from authuser.models.user_model import User
from dashboard.models.courses import *
from dashboard.models.departments import Departments
from dashboard.models.student_courses import *
from dashboard.models import Levels
from dashboard.forms.courses import CourseForm

TEMPLATE = settings.ADMIN_DASHBOARD_TEMPLATE


class CoursesView(TemplateView):
    template_name = f"{TEMPLATE}/admin/courses.html"
    model = Courses
    forms =  CourseForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Welcome to My Template'
        context['courses'] = self.model.objects.all()
        context['levels'] = Levels.objects.all()
        context['subjects'] = Subjects.objects.all()
        context['lecturers'] = LecturerModel.objects.all()
        context['departments'] = Departments.objects.all()
        context['forms'] = self.forms()

        return context
    
    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        print('form loading...')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        fm = self.forms(request.POST)
        fm.save()
        return super().get(request, *args, **kwargs)
    

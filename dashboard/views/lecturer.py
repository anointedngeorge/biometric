from typing import Any
from django import http
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from dashboard.forms.auth import *
# Create your views here.
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.views import View
import datetime
import calendar
from django.views.generic import ListView
from authuser.models import LecturerModel, User
from authuser.forms import LecturerForm

TEMPLATE = settings.ADMIN_DASHBOARD_TEMPLATE


class LecturerView(TemplateView):
    template_name = f"{TEMPLATE}/admin/lecturer_table.html"
    model = LecturerModel
    forms =  LecturerForm
    list_display=['first_name']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Lecturer'
        context['course_obj'] = self.model.objects.all()
        return context
    
    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        print('form loading...')
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs) -> HttpResponse:
        req = request.POST.dict()
        email =  req.get('email')
        password =  req.get('password')
        username = req.get('surname')
        data, created = User.objects.get_or_create(email=email, username=username)
        if created:
            fm = self.forms(request.POST, user_id=data.id)
            data.set_password(password)
            data.save()
            if fm.is_valid():
                fm.save()
        return redirect(request.META['HTTP_REFERER'])
    

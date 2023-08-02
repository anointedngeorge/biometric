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
from authuser.models.user_model import User
from dashboard.forms.subjects import *
from dashboard.models import *



TEMPLATE = settings.ADMIN_DASHBOARD_TEMPLATE



class SubjectView(TemplateView):
    template_name = f"{TEMPLATE}/admin/subjects.html"
    model = Subjects
    forms = SubjectsForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Subject'
        context['form'] = self.forms()
        return context
    
    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        fm = self.forms(request.POST)
        fm.save()
        return redirect(request.META['HTTP_REFERER'])
    


class StudentRegisterSubjectView(TemplateView):
    template_name = f"{TEMPLATE}/admin/subjects.html"
    model = RegisterStudentSubject
    forms = None

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'Subject'
        context['form'] = self.forms()
        return context
    
    def get(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)
    
    def post(self, request, *args: Any, **kwargs: Any) -> HttpResponse:
        rq =  request.POST.dict()
        rq.pop('csrfmiddlewaretoken')
        self.model.objects.create(**rq)
        return redirect(request.META['HTTP_REFERER'])
    

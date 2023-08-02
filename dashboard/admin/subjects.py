from typing import Optional
from django.contrib import admin
from django.http.request import HttpRequest
from django.http.response import HttpResponse

from dashboard.models.student_courses import *

@admin.register(Subjects)
class SubjectsAdmin(admin.ModelAdmin):
    list_display = ['name','code','unit']


@admin.register(RegisterStudentSubject)
class StudentRegisterSubjectsAdmin(admin.ModelAdmin):
    list_display = STUDENT_SUBJECT_LIST_DISPLAY
    list_filter = ['subject', 'department', 'levels','code']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        qs = queryset.filter(lecturer_id=request.user.id)
        return qs

    def response_add(self, request: HttpRequest, obj=None, post_url_continue=None) -> HttpResponse:
        obj.code = obj.subject.code
        obj.unit = obj.subject.unit
        obj.save()
        return super().response_add(request, obj, post_url_continue)
    
    def response_change(self, request: HttpRequest, obj=None) -> HttpResponse:
        obj.code = obj.subject.code
        obj.unit = obj.subject.unit
        obj.save()
        return super().response_change(request, obj)
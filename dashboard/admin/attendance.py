from typing import Any, Optional
from django.contrib import admin
from django.db.models.query import QuerySet
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from dashboard.models.attendance import *
from dashboard.forms.attendance import *
import uuid
from django.db.models import Q


@admin.register(Attendance)
class Attendance_Admin(admin.ModelAdmin):
    list_display = ATTENDANCE_LIST_DISPLAY
    
    def has_add_permission(self, request: HttpRequest) -> bool:
        return False


@admin.register(CreateAttendance)
class RegisterAttendance(admin.ModelAdmin):
    list_display = CREATEATTENDANCE_LIST_DISPLAY
    form = AttendanceForm

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        if request.user.is_superuser:
            return queryset
        qs = queryset.filter(Q(student_id=request.user.id) | Q(lecturer_id=request.user.id))
        return qs

    def response_add(self, request: HttpRequest, obj=None, post_url_continue=None) -> HttpResponse:
        obj.code = f"#{uuid.uuid4().hex}"[:6]
        obj.save()
        return super().response_add(request, obj, post_url_continue)
    

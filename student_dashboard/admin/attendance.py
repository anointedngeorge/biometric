from typing import Any, Dict, List, Optional
from django.shortcuts import redirect, render
from django.contrib.admin.options import InlineModelAdmin
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.contrib import admin
from django.forms import formset_factory
from django.contrib.admin.views.main import ChangeList
from django.http.request import HttpRequest
from django.urls.resolvers import URLPattern
from django.utils.html import format_html
from django.urls import reverse_lazy
from django.urls.resolvers import URLResolver
from django.urls import path, include, re_path
from django.template.response import TemplateResponse
import os
from django.contrib import messages as mesage


from student_dashboard.forms.authentication import *


from dashboard.models import *

from student_dashboard.admin import (
    student_dashboard_site,
    CURRENT_MAIN_TEMPLATE,
    CURRENT_TEMPLATE,
    
)
# student/logout/
# student/password_change/
# <form method="post" id="login-form" action="{% url 'admin:login' %}">
# <form method="post" id="login-form" action="{% url 'admin:login' %}?next={{ request.GET.next }}">


MODEL =  Attendance


# Register your models here using the student_site
class AttendanceCustomAdminsite(admin.ModelAdmin):
    list_display = ['student','attendance','lecturer','subject','department','levels','status']
    # list_display_links = ['*']
    list_form = '__all__'

    m = MODEL._meta

    template_list = os.path.realpath(f'{CURRENT_MAIN_TEMPLATE}/templates/{CURRENT_TEMPLATE}/{m.app_label}/{m.model_name}/change_list.html')
    template_form = os.path.realpath(f'{CURRENT_MAIN_TEMPLATE}/templates/{CURRENT_TEMPLATE}/{m.app_label}/{m.model_name}/change_form.html')

    delete_confirmation_template = template_list if os.path.exists(template_list) else f'{CURRENT_TEMPLATE}/delete_confirmation_template.html'
    # this will change the  change_list according to  apps
    change_list_template = template_list if os.path.exists(template_list) else f'{CURRENT_TEMPLATE}/change_list.html'
    # for change form
    change_form_template = template_form if os.path.exists(template_form) else f'{CURRENT_TEMPLATE}/change_form.html'


    def get_urls(self) -> List[URLResolver]:
        
        urls = super().get_urls()
        add_urls = [
            path('test-fun1/<int:user_id>', self.profile, name='test-fun1'),
            path('attendance/', self.Attendenceindex, name='attendance'),
        ]
        return add_urls + urls



    def Attendenceindex(self, request):
        from dashboard.models.attendance import Attendance, CreateAttendance
        from plugins.pilImage import pil_image_file, load_image_dir
        import os
        from plugins.face_recognition_script import (
            VideoCaptureFrame,
            load_photo_file,
            VIDEO_TITLE,
            load_photo_file_storage,
            video1
        )
        image_url = f"{settings.MEDIA_ROOT}/photo"
        CURRENT_DATE =  timezone.now()
        TEMPLATE = 'front'

        try:
            
            if request.method == 'POST':
                # video1()
                data = {}
                attendance_code = request.POST.get('attendance_code')
                attendance_code_ = ''.join(attendance_code.split())
                
                attendance = CreateAttendance.objects.all().filter(code=attendance_code_, status='started')

                if attendance.exists():
                    attend =  attendance.get()
                    title =  f"{attend.lecturer} - {attend.subject} - {attend.department} - {attend.levels}"
        
                    known_face_encodings , known_face_names = load_photo_file(photo_path_directory=image_url)
                
                    frame_capture = VideoCaptureFrame(known_face_encodings, known_face_names, title, delay=10)
                
                    # check if frame capture don't return None as a value.
                    if frame_capture != None:
                        is_true = frame_capture[0]
                        student_id =  frame_capture[1]
                        # update the data dictionary
                        data['student_id'] = uuid.UUID(student_id)
                        data['attendance_id'] = attend.id
                        data['code'] = attend.code
                        data['lecturer_id'] = attend.lecturer.id
                        data['subject_id'] = attend.subject.id
                        data['department_id'] = attend.department.id
                        data['levels_id'] = attend.levels.id
                        # print(data)
                        all_attend = Attendance.objects.all()
                        # if not all_attend.filter(attendance_date=CURRENT_DATE, subject=attend.subject.id).exists():
                        if not all_attend.filter(
                            code=attendance_code,
                            attendance_date=CURRENT_DATE, subject=attend.subject.id).exists():
                            all_attend.create(**data)
                            mesage.success(request, 'Present')
                        else:
                            mesage.warning(request, 'Fraud!!! Duplicate attendance dedictated')
                            
                else:
                    mesage.error(request, 'This attendance has ended')
                    
            return render(request, f"{TEMPLATE}/frontend_attendance.html" )
        except Exception as e:
            print("Loading eee")
            return HttpResponse(f"{e}")
        


    def profile(self, request, user_id=None):
    
        return HttpResponse(str(user_id))

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        qs = super().get_queryset(request)
        return qs.filter(student_id=request.user.id)
   
    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        from django.forms import modelform_factory
        # to import model form
        form = modelform_factory(self.model, fields=self.list_form, exclude=self.exclude)
        queryset =  self.get_queryset(request)
        
        if extra_context is None:
            extra_context = {}

        extra_context['referer'] = request.META.get('HTTP_REFERER')
        extra_context['form'] = form(request.POST or 
                                None, instance=queryset 
                                .filter(id=object_id).get()) if object_id else form
        
        return super().changeform_view(request, object_id, form_url, extra_context)





    def changelist_view(self, request, extra_context=None):
        model = self.model
        ModelFormSet = formset_factory(self.get_changelist_formset(request), extra=0)
        formset = ModelFormSet()

        sortable_by = self.get_sortable_by(request) 
        search_help_text = self.get_search_fields(request)
        
        for form in formset:
            form.queryset = model.objects.all()
        
        cl = ChangeList(request, self.model, self.list_display, self.list_display_links, self.list_filter,
                        self.date_hierarchy, self.search_fields, self.list_select_related,
                        self.list_per_page, self.list_max_show_all, self.list_editable, model_admin=self, sortable_by=sortable_by, search_help_text=search_help_text)
        
        opts =  cl.model._meta
        if extra_context is None:
            extra_context = {}
        extra_context['referer'] = request.META.get('HTTP_REFERER')
        extra_context['cl'] = cl
        extra_context['formset'] = formset
        extra_context['opts'] = opts
        extra_context['page_title'] = opts.verbose_name
        
        return super().changelist_view(request, extra_context=extra_context)


student_dashboard_site.register(MODEL, AttendanceCustomAdminsite)

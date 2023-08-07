
from django.contrib import admin
# from django.conf.urls import url
from django.views.static import serve
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path


from lecturer_dashboard.admin import lecturer_dashboard_site
from student_dashboard.admin import student_dashboard_site


urlpatterns = [
    # path('grappelli/', include('grappelli.urls')), # grappelli URLS
    path('admin/', admin.site.urls, name='admin'),
    path('lecturer/', lecturer_dashboard_site.urls, name='lecturer'),
    path('student/', student_dashboard_site.urls, name='student'),
    path('', include('frontend.urls')),
    # path('dashboard/', include('dashboard.urls')),
    
    re_path(r'^media/(?P<path>.*)$', serve,  {'document_root': settings.MEDIA_ROOT}),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
]

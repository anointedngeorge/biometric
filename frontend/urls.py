
from django.contrib import admin
from django.urls import path

# from frontend.views.take_attendance import takeAttendance
from frontend.views import *

app_name = 'frontend'

urlpatterns = [
    path('', homepage , name='home'),
    path('q/<str:pagename>', homepage, name='home'),

    path('attendance/', Attendenceindex, name='attendance'),
    path('lecturer_register/', lecturerRegistration, name='lecturer_register'),
    path('student_register/', studentRegistration, name='student_register'),
    path('test', test, name='test'),
    path('video/', video_stream, name='video_stream'),
    
]

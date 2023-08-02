from django.utils import timezone
from django.views.decorators import gzip
from django.http import StreamingHttpResponse
from django.shortcuts import redirect, render
from django.conf import settings
from django.http import HttpResponse
from django.contrib import messages as mesage
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
import uuid
from datetime import datetime
from decouple import config

from plugins.boto_plugins import *
# media/photo
CURRENT_DATE =  timezone.now()
TEMPLATE = 'front'

image_url = f"{settings.MEDIA_ROOT}/photo"



def homepage(request, pagename=''):
    context = {}
    try:
        REAL_TEMPLATE_PATH = ''       
        if pagename != '':
            REAL_TEMPLATE_PATH = f"front/{pagename}.html"
        else:
            REAL_TEMPLATE_PATH = f"front/index.html"
            
        return render(request=request, template_name=REAL_TEMPLATE_PATH, context=context)
    except Exception as e:
        return render(request=request, template_name=f"front/index.html", context=context)


def lecturerRegistration(request):
    from authuser.forms import LecturerForm
    if request.method == 'POST':
        fm = LecturerForm(request.POST)
        fm.save()
        mesage.success(request, 'New Form Data')
    mesage.error(request, 'Failed to create new form data')
    return redirect('frontend:home')




def studentRegistration(request):
    from authuser.forms import StudentForm
    if request.method == 'POST':

        fm = StudentForm(request.POST, request.FILES)
        if fm.is_valid():
            # If the form is valid, save the data to the database
            fm.save()
            # Redirect to a success page or return a success response
            mesage.success(request, 'New Form Data')
        else:
            mesage.error(request, 'Failed to create new form data')

    return redirect('frontend:home')




def Attendenceindex(request):
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

        return HttpResponse(f"{e}")
    




# Example usage:
# absolute_url = "https://bucketeer-67381f08-9445-4469-87fb-4ea24093de1e.s3.amazonaws.com/photo/f69e42a6-fb19-4ce2-a0d2-f7a1fe7dab06.jpg?AWSAccessKeyId=AKIARVGPJVYVMVW3EN4T&Signature=HuM%2F%2BAvVapqyTltsjEUKYLvVUUg%3D&Expires=1690423891"
base_url = "https://bucketeer-67381f08-9445-4469-87fb-4ea24093de1e.s3.amazonaws.com/"

def test(request):
    container = []

    try:
        from django.core.files.storage import default_storage
        import face_recognition
        from authuser.models import StudentModel
        students =  StudentModel.objects.all()


        if students.exists:
            for student in students:
                relative_path = get_relative_path(student.picture_url.url, base_url)
                # file_path = 'path/to/your/file.txt'
                known_face_encodings, known_face_names = read_from_s3(relative_path)

                if known_face_encodings:
                    container.extend(known_face_encodings)
                    container.extend(known_face_names)
                else:
                    container.append('File not found')

    except Exception as e :
        print("Database: %s " %e)
    

    return HttpResponse(container)




@gzip.gzip_page
def video_stream(request):
    from video_camera import VideoCamera, gen
    try:
        cam =  VideoCamera()
        print(cam)
        return StreamingHttpResponse(gen(cam), content_type='multipart/x-mixed-replace;boundary=frame')
    except:
        pass
    return render(request, 'front/frontend_attendance.html')



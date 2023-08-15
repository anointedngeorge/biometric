
from django.utils import timezone
from datetime import timedelta
from django.db import models
from core.core import CoreDb

import json
import uuid



ATTENDANCE_LIST_DISPLAY = ['student','code','lecturer','subject','department',
                           'levels','status','attendance_time','attendance_date']
class Attendance(CoreDb):
    student = models.ForeignKey("authuser.StudentModel", on_delete=models.CASCADE, null=True, 
                                   related_name='attendance_taken_student')
    attendance = models.ForeignKey("dashboard.CreateAttendance", on_delete=models.CASCADE, null=True, 
                                   related_name='create_attendance_rel')
    code = models.CharField(max_length=50, null=True)
    lecturer = models.ForeignKey("authuser.LecturerModel", on_delete=models.CASCADE, null=True, 
                                 related_name='attendance_lecturer_related')
    subject = models.ForeignKey("dashboard.subjects", on_delete=models.CASCADE, null=True, related_name='attendance_subject_related')
    department = models.ForeignKey("dashboard.DepartmentListing", on_delete=models.CASCADE, null=True, related_name='attendance_department_related')
    levels = models.ForeignKey("dashboard.Levels", on_delete=models.CASCADE, null=True, related_name='attendance_level_rel')
    status =  models.CharField(max_length=50, null=True, blank=True, choices=[
        ('start', 'Started'),
        ('end','Ended'),
        ('retake', 'Retake')
    ])

    attendance_time = models.DateTimeField(auto_now=False,default=timezone.now, editable=False)
    attendance_date = models.DateField(auto_now=False,default=timezone.now, editable=False)

    class Meta:
        verbose_name = 'Attendance'
        verbose_name_plural = 'View Attendances'

    def __str__(self) -> str:
        return f"{self.student}"

    


CREATEATTENDANCE_LIST_DISPLAY = ['lecturer', 'code', 'subject', 'department', 'levels','status','time_elapsed']
class CreateAttendance(CoreDb):
    code = models.CharField(max_length=500, editable=False, unique=True, null=True)
    attributes = models.CharField(max_length=50, null=True, help_text='month/day/month_name')
    lecturer = models.ForeignKey("authuser.LecturerModel", on_delete=models.CASCADE, null=True, related_name='lecturer_related')
    subject = models.ForeignKey("dashboard.subjects",
                                verbose_name='Courses',
                                on_delete=models.CASCADE, null=True, related_name='subject_related')
    department = models.ForeignKey("dashboard.DepartmentListing", on_delete=models.CASCADE, null=True, related_name='department_related')
    levels = models.ForeignKey("dashboard.Levels", on_delete=models.CASCADE, null=True, related_name='level_rel')
    status = models.CharField(max_length=250, default='pending', choices=[('started','started'), 
                                                                          ('finished','finished'),
                                                                          ('retake','retake'),  ])
    total_number_students = models.IntegerField(default=0)
    time_elapsed = models.IntegerField(default=5)
    time_elapsed2 = models.IntegerField(default=5)

    class Meta:
        verbose_name = 'Create Attendance'
        verbose_name_plural = 'Create Attendance'
    
    # career.algoridmacademy@gmail.com

    def __str__(self) -> str:
        return f"Attendance: {self.lecturer}"
    
    def get_attribute(self):
        data = eval(self.attributes)
        return data
    
    def get_students(self) -> str:
        # print('Loading...')
        # subject_related
        data = self.subject.student_subjects.all()
        return data
    
    def get_level(self):
        data = self.levels.course_level_rel.all().filter(levels_id='75440ed9-ca97-4210-9f67-d0f1fc2add6c')
        return '----'


    def current_date(self):
        return 'date'
    
    def check_duration(self):
        threshold_duration = timedelta(hours=1)  # Set the threshold duration to 1 hour

        if self.time_elapsed >= threshold_duration:
            pass
        else:
            # The duration is less than the threshold duration
            # Do something else...
                return 0
        


class TestTaskOnHeroku(models.Model):
    data = models.CharField(max_length=500)
    
from django.db import models
from core.core import CoreDb
from django.utils.html import format_html
from django.utils.functional import lazy
from django.utils.safestring import mark_safe
import uuid
import os
from django.urls import reverse
from django.urls import reverse_lazy

from authuser.models.user_model import User

def generate_filename(instance, filename):
    # Generate a unique filename using a UUID
    filename = str(uuid.uuid4()) + os.path.splitext(filename)[1]
    # Return the path where the file should be uploaded
    return os.path.join('photo', filename)


STUDENT_LIST_DISPLAY = ['surname','first_name','last_name','gender','phone','dob','reg_no',
                        'picture_name','username','get_attendance']
class StudentModel(User):
    surname =  models.CharField(max_length=150, null=True, blank=True)
    gender =  models.CharField(max_length=150, null=True, blank=True, 
                               choices=[("M","Male"),("F","Female")])
    dob = models.CharField(max_length=150, null=True, blank=True)
    state_of_origin = models.CharField(max_length=150, null=True, blank=True)
    first_name = models.CharField(max_length=350, null=True)
    last_name = models.CharField(max_length=350, null=True)
    reg_no = models.CharField(max_length=300, blank=True, null=True)
    phone = models.CharField(max_length=300, blank=True, null=True)
    address = models.CharField(max_length=300, blank=True, null=True)
    picture_url = models.ImageField(upload_to=generate_filename, null=True, blank=True)
    picture_name = models.CharField(max_length=550, null=True, blank=True, editable=False)


    class Meta:
        verbose_name = 'Students'
        verbose_name_plural = 'Students'

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_attendance(self):
        fullname = f"{self.first_name} {self.last_name}"
        return format_html('<a href="{}">View Attendance</a>',
                reverse_lazy("admin:student-attendance", 
                    args=[self.pk, fullname])
            )

    def get_student_courses(self):
        container = []
        obj =  self.student_courses.all().filter(user=self.pk)
        for x in obj:
            obj2 =  self.attendance_taken_student.all().filter(
                            student=self.pk,
                            subject=x.subject.id
                        ).count()
            container.append( {'subject':x.subject, 'count':obj2})
            # container.append( {'subject':x.subject.name, 'count':obj2})
        # print(container)
        return container


    def save(self, *args, **kwargs):
        # this will prevent overriding of the password
        if not len(self.password) > 20:
            super().set_password(self.password)  # Set the password using super()
        
        self.is_active = True
        self.account_type = "student"
        self.is_staff = True
        # self.role_name = self.Roles.STUDENT  # Assign the student role
        return super().save(*args, **kwargs)  # Call the parent's save method using super()

    

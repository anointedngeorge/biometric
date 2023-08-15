from django.db import models
from core.core import CoreDb
from django.utils.encoding import force_bytes
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.urls import reverse_lazy

from authuser.models.user_model import User

SALUTATION = [
    ('---','Choose'),
    ('mr','Mr'),
    ('Mrs','Mrs'),
    ('miss','Miss'),
    ('dr','Dr'),
    ('sir','Sir'),
    ('madam','Madam')
]

LECTURER_ADMIN_DISPLAY = ['salutation','first_name','last_name','attendance_count','get_attendance']

class LecturerModel(User):
    # user = models.ForeignKey("authuser.User", 
    #     on_delete=models.CASCADE, 
    #     null=True, 
    #     blank=True,
    #     related_name='lecturer_related_field'
    # )
    salutation = models.CharField(max_length=300, choices=SALUTATION, default='---')
    first_name = models.CharField(max_length=300, blank=True, null=True)
    last_name = models.CharField(max_length=300, blank=True, null=True)
    surname = models.CharField(max_length=300, blank=True, null=True)
    picture_url = models.CharField(max_length=300, blank=True, null=True)

    class Meta:
        verbose_name = 'Lecturer'
        verbose_name_plural = 'Lecturers'

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
    
    def get_attendance(self):
        fullname = f"{self.first_name} {self.last_name}"
        param = 'admin'
        return format_html('<a href="{}">View Attendance</a>',
                reverse_lazy(f"{param}:lecturer-student-attendance", 
                    args=[self.pk, fullname])
            )
   

    def get_student_courses(self):
        container = []
        obj =  self.lecturer_courses.all().filter(lecturer=self.pk)     
        return obj
    

    def attendance_count(self):
        container = []
        obj =  self.attendance_lecturer_related.all().filter(lecturer=self.pk).count()
        return obj
    

    def save(self, *args, **kwargs):
        # this will prevent overriding of the password
        if not len(self.password) > 20:
            super().set_password(self.password)  # Set the password using super()
        self.is_active = True
        self.account_type = 'lecturer'
        self.is_staff = True
        # self.role_name = self.Roles.STUDENT  # Assign the student role
        return super().save(*args, **kwargs)  # Call the parent's save method using super()
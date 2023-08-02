from django.db import models
from core.core import CoreDb


COURSE_LIST_DISPLAY = ['lecturer','subject','department','levels', 'semester']

class Courses(CoreDb):
    lecturer = models.ForeignKey("authuser.LecturerModel", on_delete=models.CASCADE, 
                                 null=True, related_name='lecturer_courses')
    subject = models.ForeignKey("dashboard.Subjects", on_delete=models.CASCADE, 
                                null=True, related_name='subject_courses', verbose_name='Courses')
    department = models.ForeignKey("dashboard.DepartmentListing", on_delete=models.CASCADE, 
                                   null=True, related_name='department_courses')
    levels = models.ForeignKey("dashboard.Levels", on_delete=models.CASCADE, 
                               null=True, related_name='course_level_rel')
    
    semester =  models.CharField(max_length=500, default='first', choices=[
                                            ('first','First Semester'), 
                                            ('second', 'Second Semester'),
                                            ('third', 'Third Semester'),
                                        ], null=True)

    class Meta:
        verbose_name = 'Lecturer Course'
        verbose_name_plural = 'Lecturer Courses'
    
    def __str__(self) -> str:
        return f"{self.lecturer} - {self.subject} - {self.department} - {self.levels}"

